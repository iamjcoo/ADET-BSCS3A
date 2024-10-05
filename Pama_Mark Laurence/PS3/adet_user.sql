-- SQL to create the database and table
CREATE DATABASE IF NOT EXISTS adet;

USE adet;

CREATE TABLE IF NOT EXISTS adet_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    contact_number VARCHAR(15),
    email_address VARCHAR(100),
    address TEXT
);
