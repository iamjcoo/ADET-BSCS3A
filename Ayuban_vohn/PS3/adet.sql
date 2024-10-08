-- Create the database
CREATE DATABASE adet;

-- Use the database
USE adet;

-- Create the table
CREATE TABLE adet_user (
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    contact_number VARCHAR(20),
    email_address VARCHAR(255),
    address TEXT
);
