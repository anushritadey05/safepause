
from fastapi import FastAPI
from pydantic import BaseModel, Field
from engine.rules import score_rules

app = FastAPI(
    title="SafePause Risk Engine",
    description="A simulated UPI payment risk-scoring API",
    version="1.0.0",
)


class PaymentSignals(BaseModel):
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
        "message": "SafePause Risk Engine is running",
        "simulation_only": True,
    }


@app.post("/score")
def score_payment(signals: PaymentSignals):
    result = score_rules(signals.model_dump())
    return result
