CREATE DATABASE mydatabase;
USE mydatabase;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    contact_number VARCHAR(15),
    email VARCHAR(100),
    address TEXT
);
