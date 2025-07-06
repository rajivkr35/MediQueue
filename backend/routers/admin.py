from fastapi import APIRouter, Header, HTTPException
from backend.auth_utils import verify_token
from backend.database import users_collection
from bson import ObjectId

router = APIRouter(prefix="/admin")

@router.get("/patients")
def get_all_patients(Authorization: str = Header(None)):
    email = verify_token(Authorization)
    user = users_collection.find_one({"email": email})

    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    patients = []
    for p in users_collection.find({"role": "patient"}):
        p["_id"] = str(p["_id"])  # ✅ Convert ObjectId to string
        p.pop("password", None)   # 🚫 Remove password
        patients.append(p)

    return {"patients": patients}


from fastapi import Path
from bson import ObjectId

@router.delete("/remove_patient/{patient_id}")
def remove_patient(
    patient_id: str = Path(...),
    Authorization: str = Header(None)
):
    user_email = verify_token(Authorization)
    user = users_collection.find_one({"email": user_email})

    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can remove patients")

    result = users_collection.delete_one({"_id": ObjectId(patient_id), "role": "patient"})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"message": "Patient removed successfully"}
