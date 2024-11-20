
DROP TABLE IF EXISTS adet_hya;

CREATE TABLE adet_hya (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    address VARCHAR(255)
);


INSERT INTO adet_hya (first_name, middle_name, last_name, contact_number, email_address, address) VALUES ('munay', 'penales', 'blazado', '09203013212', 'fionapenales@gmail.com', 'La Trinidad');
