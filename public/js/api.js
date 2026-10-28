/**
 * Client API SDK for Next-Generation Digital Banking Platform
 * Implements asynchronous fetch bindings for all REST endpoints in api_contract.json
 */

const API_BASE = '/api/v1';

const BankingAPI = {
    // Health Probe
    async getHealth() {
        const res = await fetch('/health');
        return res.json();
    },

    // Auth & Onboarding
    async login(email, password = null, biometricToken = null) {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, biometric_token: biometricToken })
        });
        return res.json();
    },

    async onboard(payload) {
        const res = await fetch(`${API_BASE}/auth/onboard`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        return res.json();
    },

    async getCurrentUser() {
        const res = await fetch(`${API_BASE}/auth/me`);
        return res.json();
    },

    // Accounts & Balance Servicing
    async getAccounts() {
        const res = await fetch(`${API_BASE}/accounts`);
        return res.json();
    },

    async getAccountBalance(accountId) {
        const res = await fetch(`${API_BASE}/accounts/${accountId}/balance`);
        return res.json();
    },

    async getAccountTransactions(accountId) {
        const res = await fetch(`${API_BASE}/accounts/${accountId}/transactions`);
        return res.json();
    },

    // Multi-Rail Payments & Transfers
    async submitTransfer(payload) {
        const idempotencyKey = payload.idempotency_key || 'idemp_' + Math.random().toString(36).substr(2, 9);
        const res = await fetch(`${API_BASE}/payments/transfers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Idempotency-Key': idempotencyKey
            },
            body: JSON.stringify({ ...payload, idempotency_key: idempotencyKey })
        });
        if (!res.ok) {
            const err = await res.json();
            throw err;
        }
        return res.json();
    },

    // Card Management & Instant Freeze
    async getCards() {
        const res = await fetch(`${API_BASE}/cards`);
        return res.json();
    },

    async freezeCard(cardId, reason = 'User requested instant freeze') {
        const res = await fetch(`${API_BASE}/cards/${cardId}/freeze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reason })
        });
        return res.json();
    },

    async unfreezeCard(cardId) {
        const res = await fetch(`${API_BASE}/cards/${cardId}/unfreeze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        return res.json();
    },

    // Commercial SME Banking
    async getSMEDashboard() {
        const res = await fetch(`${API_BASE}/sme/dashboard`);
        return res.json();
    },

    // Dual-Custody Approval Queue
    async getApprovals() {
        const res = await fetch(`${API_BASE}/approvals`);
        return res.json();
    },

    async executeApproval(approvalId, action, reason = '') {
        const res = await fetch(`${API_BASE}/approvals/${approvalId}/action`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action, reason })
        });
        return res.json();
    },

    // Real-Time Fraud Streaming
    async getFraudAlerts() {
        const res = await fetch(`${API_BASE}/fraud/monitoring`);
        return res.json();
    },

    // Immutable Audit Logs & Invariant Status
    async getAuditLogs() {
        const res = await fetch(`${API_BASE}/audit/logs`);
        return res.json();
    },

    async getInvariantStatus() {
        const res = await fetch(`${API_BASE}/audit/invariant-status`);
        return res.json();
    }
};

window.BankingAPI = BankingAPI;
