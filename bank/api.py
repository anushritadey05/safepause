

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from datetime import datetime, timezone
import uuid
import requests

app = FastAPI(
    title="SafePause Mock Bank",
    description="Simulated bank service for SafePause",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


RISK_ENGINE_URL = "http://127.0.0.1:8001/score"


class PaymentRequest(BaseModel):
    amount: float = Field(gt=0, le=1000000)
    payee_name: str = Field(min_length=1, max_length=100)
    payee_vpa: str = Field(min_length=3, max_length=150)

    # Simulated risk signals for the prototype
    on_call: bool = False
    remote_access_active: bool = False
    screen_share_active: bool = False
    payee_first_time: bool = False
    payee_on_mule_list: bool = False
    vpa_lookalike_score: float = Field(default=0.0, ge=0.0, le=1.0)
    is_collect: bool = False
    hour_odd: bool = False
    amount_zscore: float = 0.0
    retry_count: int = Field(default=0, ge=0)
    device_or_sim_change_72h: bool = False


@app.get("/")
def home():
    return {
        "message": "SafePause Mock Bank is running",
        "simulation_only": True,
    }


@app.post("/event")
def process_payment(payment: PaymentRequest):
    signals = payment.model_dump(
        exclude={"amount", "payee_name", "payee_vpa"}
    )

    # Ask the risk engine to evaluate this payment
    try:
        response = requests.post(
            RISK_ENGINE_URL,
            json=signals,
            timeout=3,
        )
        response.raise_for_status()
        risk = response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Risk engine unavailable. Payment was not processed.",
        )

    # Simulate the bank's response to the risk tier
    if risk["tier"] == "RED":
        status = "PAUSED_FOR_REVIEW"
    elif risk["tier"] == "AMBER":
        status = "CONFIRM_WITH_USER"
    else:
        status = "SIMULATED_APPROVED"

    return {
        "transaction_id": str(uuid.uuid4()),
        "amount": payment.amount,
        "payee_name": payment.payee_name,
        "status": status,
        "risk": risk,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "simulation_only": True,
    }
