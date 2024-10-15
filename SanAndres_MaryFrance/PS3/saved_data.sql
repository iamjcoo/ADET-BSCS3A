-- Create database if it does not exist
CREATE DATABASE IF NOT EXISTS adet;

-- Use the newly created database
USE adet;

-- Create adet_user table
CREATE TABLE IF NOT EXISTS adet_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    email_address VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
