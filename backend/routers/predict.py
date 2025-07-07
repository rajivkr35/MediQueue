# backend/routers/predict.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth_utils import verify_token
from ml import predict_wait_time

router = APIRouter()

class WaitTimeInput(BaseModel):
    age: int
    gender: int  # 0 = Male, 1 = Female
    problem_code: int  # 1 to 5
    queue_length: int
    hour: int  # 0–23

@router.post("/predict_wait_time")
def get_wait_time(input: WaitTimeInput, user: str = Depends(verify_token)):
    features = [
        input.age,
        input.gender,
        input.problem_code,
        input.queue_length,
        input.hour,
    ]
    wait_time = predict_wait_time(features)
    return {"predicted_wait_time": wait_time}
