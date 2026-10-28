-- Initial Realistic Seed Data for Digital Banking Platform

INSERT OR IGNORE INTO users (id, email, password_hash, full_name, role) VALUES
('usr_01', 'alex.mercer@apexbank.com', 'pbkdf2:sha256:mock_hash_alex', 'Alex Mercer', 'retail_customer'),
('usr_02', 'elena.rostova@techventures.io', 'pbkdf2:sha256:mock_hash_elena', 'Elena Rostova', 'sme_owner'),
('usr_03', 'marcus.vance@apexbank.com', 'pbkdf2:sha256:mock_hash_marcus', 'Marcus Vance', 'compliance_manager');

INSERT OR IGNORE INTO customers (id, user_id, full_name, email, phone, id_type, id_number, kyc_status, biometric_enrolled) VALUES
('cust_01', 'usr_01', 'Alex Mercer', 'alex.mercer@apexbank.com', '+1-555-0192', 'PASSPORT', 'P98124019', 'APPROVED', 1),
('cust_02', 'usr_02', 'Elena Rostova (TechVentures LLC)', 'elena.rostova@techventures.io', '+1-555-0841', 'EIN_BUSINESS', 'EIN-84910284', 'APPROVED', 1);

INSERT OR IGNORE INTO accounts (account_id, customer_id, account_number, account_type, currency, available_balance, current_balance, overdraft_limit, pending_holds, status) VALUES
('acc_01', 'cust_01', 'CHK-8921-4820', 'CHECKING', 'USD', 24580.50, 24580.50, 5000.00, 0.0, 'ACTIVE'),
('acc_02', 'cust_01', 'SAV-3104-9122', 'SAVINGS', 'USD', 142000.00, 142000.00, 0.0, 0.0, 'ACTIVE'),
('acc_03', 'cust_02', 'BUS-7741-0021', 'COMMERCIAL_CHECKING', 'USD', 850240.00, 850240.00, 50000.00, 12000.0, 'ACTIVE');

INSERT OR IGNORE INTO journal_entries (entry_id, transaction_id, account_id, entry_type, amount, currency, balance_after, narrative, posted_at, status) VALUES
('ent_01', 'txn_init_01', 'acc_01', 'CREDIT', 25000.00, 'USD', 25000.00, 'Initial Opening Deposit via FedNow Rail', datetime('now', '-2 days'), 'POSTED'),
('ent_02', 'txn_pay_01', 'acc_01', 'DEBIT', 419.50, 'USD', 24580.50, 'Amazon POS Merchant Settlement', datetime('now', '-1 day'), 'POSTED'),
('ent_03', 'txn_init_02', 'acc_02', 'CREDIT', 142000.00, 'USD', 142000.00, 'High-Yield Reserve Allocation', datetime('now', '-3 days'), 'POSTED'),
('ent_04', 'txn_init_03', 'acc_03', 'CREDIT', 850240.00, 'USD', 850240.00, 'Commercial Capital Injection', datetime('now', '-5 days'), 'POSTED');

INSERT OR IGNORE INTO cards (card_id, account_id, card_number_masked, cardholder_name, card_type, expiry, is_frozen, spend_limit, status) VALUES
('crd_01', 'acc_01', '•••• •••• •••• 4129', 'ALEX MERCER', 'PHYSICAL', '12/28', 0, 7500.00, 'ACTIVE'),
('crd_02', 'acc_01', '•••• •••• •••• 9840', 'ALEX MERCER', 'VIRTUAL', '08/27', 0, 2500.00, 'ACTIVE'),
('crd_03', 'acc_03', '•••• •••• •••• 7712', 'ELENA ROSTOVA', 'CORPORATE_PHYSICAL', '10/29', 0, 25000.00, 'ACTIVE');

INSERT OR IGNORE INTO approvals (approval_id, transaction_id, initiator, amount, currency, recipient, rail, status, created_at) VALUES
('appr_01', 'txn_corp_881', 'Elena Rostova', 48500.00, 'USD', 'Apex Cloud Solutions Inc.', 'FedNow', 'PENDING', datetime('now', '-2 hours')),
('appr_02', 'txn_corp_882', 'Elena Rostova', 125000.00, 'USD', 'Global Logistics Ltd', 'SWIFT_ISO20022', 'PENDING', datetime('now', '-5 hours'));

INSERT OR IGNORE INTO fraud_alerts (alert_id, transaction_id, risk_score, rule_triggered, severity, flagged_at, status) VALUES
('flt_01', 'txn_anom_992', 0.88, 'Velocity Spike: > 5 transfers within 60s', 'HIGH', datetime('now', '-10 minutes'), 'FLAGGED'),
('flt_02', 'txn_anom_993', 0.65, 'Geographical Impossible Travel Anomaly', 'MEDIUM', datetime('now', '-45 minutes'), 'FLAGGED');

INSERT OR IGNORE INTO audit_logs (log_id, actor, action, entity_type, entity_id, ip_address, timestamp, status, state_diff) VALUES
('aud_01', 'SYSTEM', 'BOOTSTRAP', 'LEDGER', 'acc_01', '127.0.0.1', datetime('now', '-2 days'), 'SUCCESS', '{"status":"INITIALIZED"}'),
('aud_02', 'usr_01', 'LOGIN', 'SESSION', 'usr_01', '192.168.1.45', datetime('now', '-1 hour'), 'SUCCESS', '{"auth_type":"FAPI_BIOMETRIC"}');
