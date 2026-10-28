/**
 * Application Interactivity & DOM Event Listeners
 */

document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Active Nav Link Highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') && currentPath.includes(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });

    // Handle Transfer Form Submission if present
    const transferForm = document.getElementById('transfer-form');
    if (transferForm) {
        transferForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertBox = document.getElementById('transfer-alert');
            const submitBtn = document.getElementById('btn-submit-transfer');

            const payload = {
                source_account_id: document.getElementById('source-account').value,
                destination_account_id: document.getElementById('dest-account').value,
                beneficiary_name: document.getElementById('beneficiary-name').value,
                amount: parseFloat(document.getElementById('transfer-amount').value),
                currency: 'USD',
                rail: document.getElementById('transfer-rail').value,
                narrative: document.getElementById('transfer-memo').value || 'Fund Transfer',
                idempotency_key: 'idk_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5)
            };

            try {
                if (submitBtn) submitBtn.disabled = true;
                const result = await BankingAPI.submitTransfer(payload);
                if (alertBox) {
                    alertBox.className = 'alert alert-success';
                    alertBox.style.display = 'block';
                    alertBox.innerHTML = `<strong>Transfer Accepted!</strong> Txn ID: <code>${result.transaction_id}</code> | Rail: ${result.rail} | Settlement: ${result.estimated_settlement}`;
                }
                transferForm.reset();
            } catch (err) {
                if (alertBox) {
                    alertBox.className = 'alert alert-danger';
                    alertBox.style.display = 'block';
                    alertBox.innerHTML = `<strong>Transfer Failed:</strong> ${err.detail?.title || err.detail || 'Transaction rejected.'}`;
                }
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }

    // Handle Card Freeze/Unfreeze Buttons
    document.querySelectorAll('.btn-toggle-freeze').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const cardId = btn.dataset.cardId;
            const isFrozen = btn.dataset.isFrozen === 'true';
            btn.disabled = true;

            try {
                if (isFrozen) {
                    await BankingAPI.unfreezeCard(cardId);
                } else {
                    await BankingAPI.freezeCard(cardId, 'Cardholder mobile freeze');
                }
                window.location.reload();
            } catch (err) {
                alert('Card action failed: ' + err.message);
            } finally {
                btn.disabled = false;
            }
        });
    });

    // Handle Dual-Custody Approval Actions
    document.querySelectorAll('.btn-approval-action').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const approvalId = btn.dataset.approvalId;
            const action = btn.dataset.action;
            btn.disabled = true;

            try {
                await BankingAPI.executeApproval(approvalId, action, 'Manager portal action');
                window.location.reload();
            } catch (err) {
                alert('Approval decision failed: ' + err.message);
            } finally {
                btn.disabled = false;
            }
        });
    });
});
