INSERT IGNORE INTO item (name, description, price, type)
VALUES ('Test Item', 'Test Description', 10.5, 'Test Type');
INSERT IGNORE INTO user (email, password, role)
VALUES ('admin', 'Test $argon2id$v=19$m=65536,t=3,p=4$cCPvPDT/vC7YWv9WiqkjWw$trRMSRLvpOTr45i/wQhO24EKbiQ+HSUIuFb4EfsYiRM', 'admin');

