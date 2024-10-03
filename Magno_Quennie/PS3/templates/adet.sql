-- Create the database if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'adet')
BEGIN
    CREATE DATABASE adet;
END;

-- Use the newly created database
USE adet;

-- Create the table if it doesn't exist
DROP TABLE IF EXISTS 'adet_user';
    CREATE TABLE adet_user (
        id INT(11) NOT NULL AUTO_INCREMENT,
        first_name NVARCHAR(255) NOT NULL,
        middle_name NVARCHAR(255) NULL,
        last_name NVARCHAR(255) NOT NULL,
        contact_number NVARCHAR(20) NOT NULL,
        `address` text DEFAULT NULL,
        `timestamp` datetime DEFAULT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
        