CREATE DATABASE IF NOT EXISTS nairobi_real_estate;
USE nairobi_real_estate;


DROP TABLE IF EXISTS valuations;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS locations;


CREATE TABLE locations (
location_id INT AUTO_INCREMENT PRIMARY KEY,
county VARCHAR(50) NOT NULL,
sub_county VARCHAR(100) NOT NULL,
city VARCHAR(50) DEFAULT 'Nairobi',
UNIQUE KEY uq_location (county,sub_county)
);


CREATE TABLE properties (
property_id VARCHAR(50) PRIMARY KEY,
location_id INT NOT NULL,
property_type VARCHAR(50) NOT NULL,
bedrooms INT NOT NULL,
size_sqm INT NOT NULL,
FOREIGN KEY (location_id) REFERENCES locations(location_id)
ON UPDATE CASCADE
ON DELETE RESTRICT
);

CREATE TABLE valuations (
valuation_id INT AUTO_INCREMENT PRIMARY KEY,
property_id VARCHAR(50) NOT NULL,
monthly_rent_kes DECIMAL(12,2) NOT NULL,
purchase_price_kes DECIMAL(15,2) NOT NULL,
calculated_rental_yield_pct DECIMAL(5,2) NOT NULL,
recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(property_id) REFERENCES properties(property_id)
ON UPDATE CASCADE
ON DELETE CASCADE
);



