"""
Pydantic Schemas for API Requests, Responses, and DTOs.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

# Health Schema


class HealthResponse(BaseModel):
    status: str = "ok"
    timestamp: str

# Auth & Onboarding Schemas


class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None
    biometric_token: Optional[str] = None


class UserInfo(BaseModel):
    user_id: str
    name: str
    email: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserInfo


class OnboardRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    id_type: str
    id_number: str
    initial_deposit: float = Field(default=100.0, ge=0.0)
    account_type: str = "CHECKING"


class OnboardResponse(BaseModel):
    customer_id: str
    account_id: str
    account_number: str
    status: str
    message: str

# Accounts & Balances Schemas


class AccountItem(BaseModel):
    account_id: str
    account_number: str
    account_type: str
    currency: str
    available_balance: float
    current_balance: float
    status: str


class AccountsListResponse(BaseModel):
    accounts: List[AccountItem]


class BalanceDetailResponse(BaseModel):
    account_id: str
    available_balance: float
    current_balance: float
    pending_holds: float
    overdraft_limit: float
    currency: str


class TransactionItem(BaseModel):
    entry_id: str
    transaction_id: str
    entry_type: str
    amount: float
    currency: str
    balance_after: float
    narrative: str
    posted_at: str
    status: str


class TransactionsResponse(BaseModel):
    transactions: List[TransactionItem]

# Fund Transfers Schemas


class TransferRequest(BaseModel):
    source_account_id: str
    destination_account_id: str
    beneficiary_name: str
    amount: float = Field(..., gt=0.0)
    currency: str = "USD"
    rail: str = "FedNow"
    narrative: Optional[str] = "Fund Transfer"
    idempotency_key: str


class TransferResponse(BaseModel):
    transaction_id: str
    saga_correlation_id: str
    status: str
    amount: float
    rail: str
    estimated_settlement: str

# Card Management Schemas


class CardItem(BaseModel):
    card_id: str
    account_id: str
    card_number_masked: str
    cardholder_name: str
    card_type: str
    expiry: str
    status: str
    spend_limit: float
    is_frozen: bool


class CardsListResponse(BaseModel):
    cards: List[CardItem]


class CardFreezeRequest(BaseModel):
    reason: Optional[str] = "User requested instant freeze"


class CardActionResponse(BaseModel):
    card_id: str
    is_frozen: bool
    status: str
    updated_at: str

# SME Operations


class SMEDashboardResponse(BaseModel):
    total_liquidity: float
    monthly_inflow: float
    monthly_outflow: float
    pending_approvals_count: int
    payroll_batch_status: str

# Dual-Custody Approval Queue Schemas


class ApprovalItem(BaseModel):
    approval_id: str
    transaction_id: str
    initiator: str
    amount: float
    currency: str
    recipient: str
    rail: str
    status: str
    created_at: str


class ApprovalsListResponse(BaseModel):
    approvals: List[ApprovalItem]


class ApprovalActionRequest(BaseModel):
    action: str = Field(..., pattern="^(APPROVE|REJECT)$")
    reason: Optional[str] = None


class ApprovalActionResponse(BaseModel):
    approval_id: str
    status: str
    processed_by: str
    timestamp: str

# Real-time Fraud Monitoring Schemas


class FraudAlertItem(BaseModel):
    alert_id: str
    transaction_id: str
    risk_score: float
    rule_triggered: str
    severity: str
    flagged_at: str
    status: str


class FraudMonitoringResponse(BaseModel):
    alerts: List[FraudAlertItem]

# Immutable Audit Explorer & Invariant Status Schemas


class AuditLogItem(BaseModel):
    log_id: str
    actor: str
    action: str
    entity_type: str
    entity_id: str
    ip_address: str
    timestamp: str
    status: str
    state_diff: Optional[str] = None


class AuditLogsResponse(BaseModel):
    logs: List[AuditLogItem]


class InvariantStatusResponse(BaseModel):
    status: str
    total_debits: float
    total_credits: float
    discrepancy: float
    last_reconciled_at: str
    ledger_invariants_preserved: bool
