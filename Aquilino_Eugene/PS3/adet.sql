DROP DATABASE IF EXISTS adet;

CREATE DATABASE IF NOT EXISTS adet;

USE adet;

CREATE TABLE adet_user (
    FirstName VARCHAR(100),
    MiddleName VARCHAR(100),
    LastName VARCHAR(100),
    CellphoneNumber VARCHAR(20),
    Email VARCHAR(100),
    HomeAddress VARCHAR(100)
);