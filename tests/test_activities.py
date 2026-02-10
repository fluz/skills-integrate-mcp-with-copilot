import os
import sys
import tempfile

# ensure project root is on sys.path for imports during tests
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app import app, get_db
from src.db import Base
from src import models


# Use a single temporary SQLite DB for the test session
db_fd, db_path = tempfile.mkstemp()
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_list_activities():
    # Create activities by directly using endpoints (we'll use the DB through tests)
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_signup_and_unregister_flow():
    # create a new activity first
    payload = {
        "name": "Test Activity",
        "description": "Desc",
        "schedule": "Now",
        "max_participants": 10
    }
    r = client.post("/activities", json=payload)
    assert r.status_code == 201

    # sign up
    r = client.post(f"/activities/{payload['name']}/signup", params={"email": "student@example.com"})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # duplicate signup should fail
    r = client.post(f"/activities/{payload['name']}/signup", params={"email": "student@example.com"})
    assert r.status_code == 400

    # unregister
    r = client.delete(f"/activities/{payload['name']}/unregister", params={"email": "student@example.com"})
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # unregister again should fail
    r = client.delete(f"/activities/{payload['name']}/unregister", params={"email": "student@example.com"})
    assert r.status_code == 400
