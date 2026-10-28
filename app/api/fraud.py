"""
Real-time Streaming Fraud Evaluation & Alerts API (REQ-F-004, REQ-F-009).
Powered by simulated Flink anomaly rules engine.
"""

from fastapi import APIRouter
from app.db.connection import get_db
from app.models.schemas import FraudMonitoringResponse, FraudAlertItem

router = APIRouter(
    prefix="/fraud",
    tags=["Real-time Fraud Evaluation & Alerts"])


@router.get("/monitoring", response_model=FraudMonitoringResponse)
def get_fraud_monitoring():
    """
    Stream real-time evaluated transactions and flagged fraud anomalies (REQ-F-004).
    """
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM fraud_alerts ORDER BY flagged_at DESC").fetchall()
        alerts = [
            FraudAlertItem(
                alert_id=r["alert_id"],
                transaction_id=r["transaction_id"],
                risk_score=float(r["risk_score"]),
                rule_triggered=r["rule_triggered"],
                severity=r["severity"],
                flagged_at=str(r["flagged_at"]),
                status=r["status"]
            )
            for r in rows
        ]
        return FraudMonitoringResponse(alerts=alerts)
