"""
Accounts & Balance Servicing API endpoints (REQ-F-002).
"""

from fastapi import APIRouter, HTTPException, status
from app.db.connection import get_db
from app.models.schemas import (
    AccountsListResponse,
    AccountItem,
    BalanceDetailResponse,
    TransactionsResponse,
    TransactionItem
)

router = APIRouter(prefix="/accounts", tags=["Accounts & Balance Servicing"])


@router.get("", response_model=AccountsListResponse)
def list_accounts():
    """
    List real-time retail and commercial accounts (REQ-F-002).
    """
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM accounts ORDER BY created_at DESC").fetchall()
        accounts = [
            AccountItem(
                account_id=r["account_id"],
                account_number=r["account_number"],
                account_type=r["account_type"],
                currency=r["currency"],
                available_balance=float(r["available_balance"]),
                current_balance=float(r["current_balance"]),
                status=r["status"]
            )
            for r in rows
        ]
        return AccountsListResponse(accounts=accounts)


@router.get("/{account_id}/balance", response_model=BalanceDetailResponse)
def get_account_balance(account_id: str):
    """
    Fetch granular real-time balances, pending holds, and overdraft limits (REQ-F-002).
    """
    with get_db() as conn:
        r = conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?",
            (account_id,
             )).fetchone()
        if not r:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {account_id} not found")
        return BalanceDetailResponse(
            account_id=r["account_id"],
            available_balance=float(r["available_balance"]),
            current_balance=float(r["current_balance"]),
            pending_holds=float(r["pending_holds"]),
            overdraft_limit=float(r["overdraft_limit"]),
            currency=r["currency"]
        )


@router.get("/{account_id}/transactions", response_model=TransactionsResponse)
def get_account_transactions(account_id: str):
    """
    Retrieve double-entry journal transaction records and ledger history (REQ-F-002, REQ-F-010).
    """
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM journal_entries WHERE account_id = ? ORDER BY posted_at DESC",
            (account_id,)
        ).fetchall()
        transactions = [
            TransactionItem(
                entry_id=r["entry_id"],
                transaction_id=r["transaction_id"],
                entry_type=r["entry_type"],
                amount=float(r["amount"]),
                currency=r["currency"],
                balance_after=float(r["balance_after"]),
                narrative=r["narrative"],
                posted_at=str(r["posted_at"]),
                status=r["status"]
            )
            for r in rows
        ]
        return TransactionsResponse(transactions=transactions)
