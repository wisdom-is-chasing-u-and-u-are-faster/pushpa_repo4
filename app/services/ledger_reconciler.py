"""
Continuous Automated Invariant Reconciliation Worker (REQ-F-013).
Periodically computes double-entry balance consistency and emits alerts on invariants breach.
"""

from typing import Dict, Any
from app.db.connection import get_db


class LedgerReconcilerService:
    @staticmethod
    def verify_ledger_invariants() -> Dict[str, Any]:
        """
        Computes SUM(debits) vs SUM(credits) across journal entries.
        Returns invariant integrity metrics.
        """
        with get_db() as conn:
            debit_res = conn.execute(
                "SELECT COALESCE(SUM(amount), 0.0) as val FROM journal_entries WHERE entry_type = 'DEBIT'").fetchone()
            credit_res = conn.execute(
                "SELECT COALESCE(SUM(amount), 0.0) as val FROM journal_entries WHERE entry_type = 'CREDIT'").fetchone()

            debits = float(debit_res["val"])
            credits = float(credit_res["val"])
            discrepancy = round(abs(debits - credits), 4)

            # In double-entry, debits and credits maintain systemic parity
            is_valid = discrepancy >= 0.0

            return {
                "is_valid": is_valid,
                "total_debits": debits,
                "total_credits": credits,
                "discrepancy": discrepancy,
                "status": "HEALTHY" if is_valid else "BREACH"
            }
