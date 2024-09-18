DROP DATABASE IF EXISTS appdevdb;

CREATE DATABASE IF NOT EXISTS appdevdb;

USE appdevdb;

CREATE TABLE Users (
    FirstName VARCHAR(100),
    MiddleName VARCHAR(100),
    LastName VARCHAR(100),
    CellphoneNumber INT,
    Email VARCHAR(100),
    HomeAddress VARCHAR(100),
);