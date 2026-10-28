"""
Dual-Custody Approval Service and State Machine Orchestrator (REQ-F-008).
"""

from typing import Dict, Any, Optional
from app.db.connection import get_db


class DualCustodyApprovalService:
    @staticmethod
    def process_decision(approval_id: str, manager_name: str,
                         action: str, reason: Optional[str] = None) -> Dict[str, Any]:
        with get_db() as conn:
            target = conn.execute(
                "SELECT * FROM approvals WHERE approval_id = ?", (approval_id,)).fetchone()
            if not target:
                return {"success": False, "error": "Not Found"}

            status_val = "APPROVED" if action == "APPROVE" else "REJECTED"
            conn.execute(
                "UPDATE approvals SET status = ?, processed_by = ?, reason = ? WHERE approval_id = ?",
                (status_val,
                 manager_name,
                 reason or f"Action {action}",
                 approval_id)
            )
            return {"success": True, "approval_id": approval_id,
                    "status": status_val}
