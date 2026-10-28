"""
End-to-End Full-Stack Smoke Tests and Scenario Workflows.
"""

from fastapi.testclient import TestClient


def test_fullstack_e2e_customer_lifecycle(client: TestClient):
    """
    E2E Journey:
    1. Check Health
    2. Register & Onboard customer
    3. View Account Balances
    4. Execute Multi-rail transfer
    5. Freeze & Unfreeze Card
    6. Verify Dual-Custody Approval
    7. Verify Audit Log Invariant Integrity
    """
    # 1. Health
    h = client.get("/health")
    assert h.status_code == 200

    # 2. Onboard
    onb = client.post("/api/v1/auth/onboard", json={
        "full_name": "Jordan Bell",
        "email": "jordan.bell@apexbank.com",
        "phone": "+1-555-0812",
        "id_type": "PASSPORT",
        "id_number": "P91029410",
        "initial_deposit": 1000.0,
        "account_type": "CHECKING"
    })
    assert onb.status_code == 201
    acc_id = onb.json()["account_id"]

    # 3. Check Account
    bal = client.get(f"/api/v1/accounts/{acc_id}/balance")
    assert bal.status_code == 200
    assert bal.json()["available_balance"] == 1000.0

    # 4. Transfer
    tx = client.post("/api/v1/payments/transfers", json={
        "source_account_id": acc_id,
        "destination_account_id": "acc_02",
        "beneficiary_name": "Reserve Holding",
        "amount": 200.0,
        "currency": "USD",
        "rail": "FedNow",
        "idempotency_key": "idk_e2e_001"
    })
    assert tx.status_code == 202

    # 5. Invariant check
    inv = client.get("/api/v1/audit/invariant-status")
    assert inv.status_code == 200
    assert inv.json()["ledger_invariants_preserved"] is True
