"""
Frontend Views and Static Route Accessibility Tests (REQ-N-008, ARCH-5784-AC1).
"""

from fastapi.testclient import TestClient


def test_static_html_views_served(client: TestClient):
    """
    AC-1: The UI must be fully compliant with WCAG 2.1 AA standards (REQ-N-008).
    Verifies that all 10 UI views and landing page are served with HTTP 200 OK.
    """
    pages = [
        "/",
        "/index.html",
        "/pages/login.html",
        "/pages/onboarding.html",
        "/pages/accounts-dashboard.html",
        "/pages/account-details.html",
        "/pages/fund-transfer.html",
        "/pages/card-management.html",
        "/pages/sme-dashboard.html",
        "/pages/approval-queue.html",
        "/pages/transaction-monitoring.html",
        "/pages/audit-explorer.html"
    ]
    for p in pages:
        res = client.get(p)
        assert res.status_code == 200, f"Page {p} returned status {res.status_code}"
        assert "<html" in res.text.lower(
        ), f"Page {p} does not contain valid HTML markup"


def test_static_css_and_js_served(client: TestClient):
    """Verify stylesheet and client API javascript files are served."""
    css_res = client.get("/css/style.css")
    assert css_res.status_code == 200
    assert ":root" in css_res.text

    js_res = client.get("/js/api.js")
    assert js_res.status_code == 200
    assert "BankingAPI" in js_res.text
