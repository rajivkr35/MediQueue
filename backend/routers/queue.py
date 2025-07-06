# backend/routers/queue.py

from fastapi import APIRouter, Depends, HTTPException
from backend.auth_utils import verify_token
from backend.database import db
from bson import ObjectId

router = APIRouter()
queue_collection = db["patient_queue"]

# Add patient
@router.post("/add_patient")
def add_patient(patient: dict, user: str = Depends(verify_token)):
    patient["added_by"] = user
    result = queue_collection.insert_one(patient)
    return {"message": "Patient added", "id": str(result.inserted_id)}

# Get current queue
@router.get("/get_queue")
def get_queue(user: str = Depends(verify_token)):
    patients = list(queue_collection.find({"added_by": user}))
    for p in patients:
        p["_id"] = str(p["_id"])
    return {"queue": patients}

# Remove patient by ID
@router.delete("/remove_patient/{patient_id}")
def remove_patient(patient_id: str, user: str = Depends(verify_token)):
    result = queue_collection.delete_one({
        "_id": ObjectId(patient_id),
        "added_by": user
    })
    if result.deleted_count == 1:
        return {"message": "Patient removed"}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
