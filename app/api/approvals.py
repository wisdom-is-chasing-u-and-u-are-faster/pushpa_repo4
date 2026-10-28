"""
Dual-Custody Approval Queue API endpoints (REQ-F-008).
Allows authorized managers to approve or reject designated high-value commercial transactions.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.db.connection import get_db
from app.models.schemas import (
    ApprovalsListResponse,
    ApprovalItem,
    ApprovalActionRequest,
    ApprovalActionResponse
)

router = APIRouter(prefix="/approvals", tags=["Dual-Custody Approvals"])


@router.get("", response_model=ApprovalsListResponse)
def list_approvals():
    """
    List all pending and processed dual-custody approval requests (REQ-F-008).
    """
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM approvals ORDER BY created_at DESC").fetchall()
        approvals = [
            ApprovalItem(
                approval_id=r["approval_id"],
                transaction_id=r["transaction_id"],
                initiator=r["initiator"],
                amount=float(r["amount"]),
                currency=r["currency"],
                recipient=r["recipient"],
                rail=r["rail"],
                status=r["status"],
                created_at=str(r["created_at"])
            )
            for r in rows
        ]
        return ApprovalsListResponse(approvals=approvals)


@router.post("/{approval_id}/action", response_model=ApprovalActionResponse)
def execute_approval_action(approval_id: str, payload: ApprovalActionRequest):
    """
    Approve or reject a transaction in the dual-custody queue (REQ-F-008).
    """
    with get_db() as conn:
        item = conn.execute("SELECT * FROM approvals WHERE approval_id = ?", (approval_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Approval request {approval_id} not found")

        now_str = datetime.utcnow().isoformat()
        final_status = "APPROVED" if payload.action == "APPROVE" else "REJECTED"

        conn.execute(
            """UPDATE approvals SET status = ?, processed_by = 'Marcus Vance (Compliance Manager)',
               processed_at = CURRENT_TIMESTAMP, reason = ? WHERE approval_id = ?""",
            (final_status, payload.reason or f"Manager action {payload.action}", approval_id)
        )

        # Audit logging with unique UUID
        conn.execute(
            """INSERT INTO audit_logs (log_id, actor, action, entity_type, entity_id, status, state_diff)
               VALUES (?, 'COMPLIANCE_MANAGER', 'DUAL_CUSTODY_DECISION', 'APPROVAL', ?, 'SUCCESS', ?)""",
            (f"aud_{uuid.uuid4().hex[:8]}", approval_id, f'{{"action": "{payload.action}", "decision": "{final_status}"}}')
        )

        return ApprovalActionResponse(
            approval_id=approval_id,
            status=final_status,
            processed_by="Marcus Vance (Compliance Manager)",
            timestamp=now_str
        )
