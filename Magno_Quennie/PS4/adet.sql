-- Create the 'adet' database if it doesn't exist
CREATE DATABASE IF NOT EXISTS adet;

-- Use the 'adet' database
USE adet;

-- Create the 'adet_user' table to store user information
CREATE TABLE IF NOT EXISTS adet_user (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- Primary key, auto-incremented ID
    first_name VARCHAR(100) NOT NULL,            -- User's first name
    middle_name VARCHAR(100),                    -- User's middle name (optional)
    last_name VARCHAR(100) NOT NULL,             -- User's last name
    contact_number VARCHAR(15) NOT NULL,         -- Contact number
    email_address VARCHAR(255) NOT NULL,         -- Email address
    address TEXT,                                -- Address field
    password VARCHAR(255) NOT NULL,              -- Password (hashed in production for security)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of the record creation
);

-- Create a unique index on the email_address column to prevent duplicate entries
CREATE UNIQUE INDEX idx_email_address ON adet_user (email_address);
