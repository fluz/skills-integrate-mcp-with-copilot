"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Database-backed activities
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends

from .db import init_db, get_db
from .models import Activity, Registration


class ActivityCreate(BaseModel):
    name: str
    description: str | None = None
    schedule: str | None = None
    max_participants: int | None = None


@app.on_event("startup")
def on_startup():
    # create DB tables if they don't exist
    init_db()


@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)) -> List[dict]:
    db_activities = db.query(Activity).all()
    result = []
    for a in db_activities:
        participants = [r.email for r in a.registrations]
        result.append({
            "name": a.name,
            "description": a.description,
            "schedule": a.schedule,
            "max_participants": a.max_participants,
            "participants": participants
        })
    return result


@app.post("/activities", status_code=201)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db)):
    existing = db.query(Activity).filter(Activity.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Activity already exists")
    activity = Activity(
        name=payload.name,
        description=payload.description,
        schedule=payload.schedule,
        max_participants=payload.max_participants
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return {"message": "Created", "name": activity.name}


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # check existing registration
    exists = db.query(Registration).filter(
        Registration.activity_id == activity.id,
        Registration.email == email
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # check capacity
    if activity.max_participants is not None:
        current = db.query(Registration).filter(Registration.activity_id == activity.id).count()
        if current >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

    reg = Registration(email=email, activity_id=activity.id)
    db.add(reg)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    reg = db.query(Registration).filter(
        Registration.activity_id == activity.id,
        Registration.email == email
    ).first()
    if not reg:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    db.delete(reg)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
