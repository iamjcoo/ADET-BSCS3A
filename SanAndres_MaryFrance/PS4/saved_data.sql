CREATE TABLE adet_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    email_address VARCHAR(100) NOT NULL UNIQUE,
    address TEXT,
    password VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);