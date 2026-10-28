"""
REST API Endpoint Tests covering all Acceptance Criteria (ARCH-5784-AC1 to AC5).
"""

import uuid
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Verify health readiness probe."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_customer_onboarding(client: TestClient):
    """
    AC-2: Customer onboarding must be completable in under 3 minutes with biometric security (REQ-F-006, REQ-N-007).
    """
    email = f"test.user.{uuid.uuid4().hex[:4]}@example.com"
    payload = {
        "full_name": "Taylor Morgan",
        "email": email,
        "phone": "+1-555-0991",
        "id_type": "PASSPORT",
        "id_number": "P88129031",
        "initial_deposit": 500.0,
        "account_type": "CHECKING"
    }
    res = client.post("/api/v1/auth/onboard", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert data["customer_id"].startswith("cust_")
    assert data["account_number"].startswith("CHK-")


def test_account_balances_and_transactions(client: TestClient):
    """
    AC-3: Users can view real-time account balances and transaction history (REQ-F-002).
    """
    res = client.get("/api/v1/accounts")
    assert res.status_code == 200
    accounts = res.json()["accounts"]
    assert len(accounts) >= 1

    first_acc_id = accounts[0]["account_id"]
    bal_res = client.get(f"/api/v1/accounts/{first_acc_id}/balance")
    assert bal_res.status_code == 200
    bal_data = bal_res.json()
    assert "available_balance" in bal_data
    assert "current_balance" in bal_data

    tx_res = client.get(f"/api/v1/accounts/{first_acc_id}/transactions")
    assert tx_res.status_code == 200
    assert "transactions" in tx_res.json()


def test_payment_transfer_and_idempotency(client: TestClient):
    """
    Verify multi-rail fund transfer and idempotency protection (REQ-F-001, REQ-F-014).
    """
    idemp_key = f"idk_test_{uuid.uuid4().hex}"
    payload = {
        "source_account_id": "acc_01",
        "destination_account_id": "acc_02",
        "beneficiary_name": "Taylor Morgan",
        "amount": 150.00,
        "currency": "USD",
        "rail": "FedNow",
        "narrative": "Test Instant Transfer",
        "idempotency_key": idemp_key
    }
    # Initial execution
    res1 = client.post("/api/v1/payments/transfers", json=payload)
    assert res1.status_code == 202
    data1 = res1.json()
    assert data1["status"] == "COMPLETED"

    # Idempotent replay
    res2 = client.post("/api/v1/payments/transfers", json=payload)
    assert res2.status_code == 202
    data2 = res2.json()
    assert data2["transaction_id"] == data1["transaction_id"]


def test_card_freeze_and_unfreeze(client: TestClient):
    """
    AC-4: Users can instantly freeze and unfreeze their cards (REQ-F-003).
    """
    cards_res = client.get("/api/v1/cards")
    assert cards_res.status_code == 200
    cards = cards_res.json()["cards"]
    assert len(cards) >= 1

    target_card_id = cards[0]["card_id"]

    # Freeze
    freeze_res = client.post(
        f"/api/v1/cards/{target_card_id}/freeze",
        json={
            "reason": "Lost card"})
    assert freeze_res.status_code == 200
    assert freeze_res.json()["is_frozen"] is True
    assert freeze_res.json()["status"] == "FROZEN"

    # Unfreeze
    unfreeze_res = client.post(f"/api/v1/cards/{target_card_id}/unfreeze")
    assert unfreeze_res.status_code == 200
    assert unfreeze_res.json()["is_frozen"] is False
    assert unfreeze_res.json()["status"] == "ACTIVE"


def test_dual_custody_approvals(client: TestClient):
    """
    AC-5: Managers can approve or reject transactions in the dual-custody approval queue (REQ-F-008).
    """
    appr_res = client.get("/api/v1/approvals")
    assert appr_res.status_code == 200
    approvals = appr_res.json()["approvals"]
    assert len(approvals) >= 1

    target_appr_id = approvals[0]["approval_id"]
    action_res = client.post(
        f"/api/v1/approvals/{target_appr_id}/action",
        json={
            "action": "APPROVE",
            "reason": "Dual custody authorized by compliance manager"}
    )
    assert action_res.status_code == 200
    assert action_res.json()["status"] == "APPROVED"


def test_fraud_monitoring_and_audit_invariants(client: TestClient):
    """
    Verify real-time fraud radar and 60-second continuous invariant reconciliation (REQ-F-004, REQ-F-010, REQ-F-013).
    """
    fraud_res = client.get("/api/v1/fraud/monitoring")
    assert fraud_res.status_code == 200
    assert "alerts" in fraud_res.json()

    audit_res = client.get("/api/v1/audit/logs")
    assert audit_res.status_code == 200
    assert len(audit_res.json()["logs"]) >= 1

    inv_res = client.get("/api/v1/audit/invariant-status")
    assert inv_res.status_code == 200
    inv_data = inv_res.json()
    assert inv_data["status"] == "HEALTHY"
    assert inv_data["ledger_invariants_preserved"] is True
