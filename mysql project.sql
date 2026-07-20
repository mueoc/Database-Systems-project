USE theproject;

DROP TRIGGER IF EXISTS BeforeReceiptInsert;
DROP FUNCTION IF EXISTS CalculateTax;
DROP FUNCTION IF EXISTS ConvertToSEK;

DROP TABLE IF EXISTS Receipt;
DROP TABLE IF EXISTS Game_Key;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Store;
DROP TABLE IF EXISTS Region_Tax;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Product;

CREATE TABLE IF NOT EXISTS Company (
    Company_id INT PRIMARY KEY AUTO_INCREMENT,
    Company_Name VARCHAR(100) NOT NULL,
    HQ_Location VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Department (
    Department_id INT PRIMARY KEY AUTO_INCREMENT,
    Occupations VARCHAR(100) NOT NULL UNIQUE,
    Company_id INT,
    FOREIGN KEY (Company_id) REFERENCES Company(Company_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Employee (
    Employee_id INT PRIMARY KEY AUTO_INCREMENT,
    Role VARCHAR(50) NOT NULL,
    Location VARCHAR(50) NOT NULL,
    Is_Manager TINYINT DEFAULT 0, 
    Department_id INT,
    FOREIGN KEY (Department_id) REFERENCES Department(Department_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Region_Tax (
    CountryCode VARCHAR(3) PRIMARY KEY, 
    CountryName VARCHAR(100) NOT NULL,
    Currency VARCHAR(3) NOT NULL,
    TaxRate DECIMAL(4, 2) NOT NULL,
    Price INT NOT NULL 
);

CREATE TABLE IF NOT EXISTS Store (
    Store_id INT PRIMARY KEY AUTO_INCREMENT,
    City VARCHAR(50) NOT NULL,
    CountryCode VARCHAR(3),
    FOREIGN KEY (CountryCode) REFERENCES Region_Tax(CountryCode)
);

CREATE TABLE IF NOT EXISTS Customer (
    Customer_id INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(100) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    CountryCode VARCHAR(3),
    FOREIGN KEY (CountryCode) REFERENCES Region_Tax(CountryCode)
);

CREATE TABLE IF NOT EXISTS Product (
    Product_key_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    Name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Game_Key (
    Key_id INT PRIMARY KEY AUTO_INCREMENT,
    CD_Key VARCHAR(50) NOT NULL UNIQUE,
    Product_key_id INT,
    FOREIGN KEY (Product_key_id) REFERENCES Product(Product_key_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Receipt (
    Receipt_id INT PRIMARY KEY AUTO_INCREMENT,
    Date_Time DATETIME DEFAULT CURRENT_TIMESTAMP,
    Tax_Paid DECIMAL(10,2) NOT NULL,
    TotalPrice DECIMAL(10,2) NOT NULL,
    Customer_id INT,
    Product_key_id INT,
    Key_id INT UNIQUE,
    Store_id INT,
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id),
    FOREIGN KEY (Product_key_id) REFERENCES Product(Product_key_id),
    FOREIGN KEY (Key_id) REFERENCES Game_Key(Key_id),
    FOREIGN KEY (Store_id) REFERENCES Store(Store_id)
);

INSERT INTO Company (Company_Name, HQ_Location) VALUES ("HappyJumpy Studios", "Gothenburg");

INSERT INTO Department (Occupations, Company_id) VALUES ("Economics", 1), ("Engineering", 1), ("Sales", 1);

INSERT INTO Region_Tax (CountryCode, CountryName, Currency, TaxRate, Price) VALUES 
('SE', 'Sweden', 'SEK', 0.25, 100),
('NO', 'Norway', 'NOK', 0.25, 101),
('DK', 'Denmark', 'DKK', 0.25, 67),
('IS', 'Iceland', 'ISK', 0.24, 1290),
('FI', 'Finland', 'EUR', 0.255, 9);

INSERT INTO Store (City, CountryCode) VALUES 
("Stockholm", "SE"),
("Oslo", "NO"),
("Copenhagen", "DK"),
("Reykjavík", "IS"),
("Helsinki", "FI");

INSERT INTO Employee (Role, Location, Is_Manager, Department_id) VALUES 
("Economics Analyst", 'Gothenburg', 0, 1),
("Economics Analyst", 'Gothenburg', 0, 1),
("Economics Analyst", 'Gothenburg', 0, 1),
("Software Engineer", 'Gothenburg', 0, 2),
("Software Engineer", 'Gothenburg', 0, 2),
("Software Engineer", 'Gothenburg', 0, 2),

("Regional Manager", 'Stockholm', 1, 3),
("Cashier", 'Stockholm', 0, 3),
("Regional Manager", 'Oslo', 1, 3),
("Cashier", 'Oslo', 0, 3),
("Regional Manager", 'Copenhagen', 1, 3),
("Cashier", 'Copenhagen', 0, 3),
("Regional Manager", 'Reykjavík', 1, 3),
("Cashier", 'Reykjavík', 0, 3),
("Regional Manager", 'Helsinki', 1, 3),
("Cashier", 'Helsinki', 0, 3);

INSERT INTO Product (Name) VALUES ('Happy Jumpy');

INSERT INTO Customer (Username, Email, CountryCode) VALUES 
('starMan', 'star@se.com', 'SE'),
('nordic_gamer', 'gamer@no.com', 'NO'),
('finnish_gamer', 'gamer@fi.com', 'FI'),
('ISLAND_gamer', 'gamer@IS.com', 'IS'),
('boring_gamer', 'boring@IS.com', 'IS');

DELIMITER //
CREATE FUNCTION CalculateTax(price INT, tax_rate DECIMAL(4,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN price * tax_rate;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER BeforeReceiptInsert
BEFORE INSERT ON Receipt
FOR EACH ROW
BEGIN
    DECLARE v_TaxRate DECIMAL(4,2);
    DECLARE v_BasePrice INT;
    DECLARE v_CountryCode VARCHAR(3);

    SELECT CountryCode INTO v_CountryCode 
    FROM Customer 
    WHERE Customer_id = NEW.Customer_id;

    SELECT TaxRate, Price INTO v_TaxRate, v_BasePrice 
    FROM Region_Tax 
    WHERE CountryCode = v_CountryCode;

    SET NEW.Tax_Paid = CalculateTax(v_BasePrice, v_TaxRate);
    
    SET NEW.TotalPrice = v_BasePrice + NEW.Tax_Paid;
END //
DELIMITER ;


DELIMITER //
CREATE FUNCTION ConvertToSEK(amount DECIMAL(10,2), currency_code VARCHAR(3))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_ConvertedAmount DECIMAL(10,2);

    CASE currency_code
        WHEN 'EUR' THEN SET v_ConvertedAmount = amount * 11.03;
        WHEN 'NOK' THEN SET v_ConvertedAmount = amount * 1.01;
        WHEN 'ISK' THEN SET v_ConvertedAmount = amount * 0.077;
        WHEN 'DKK' THEN SET v_ConvertedAmount = amount * 0.68;
        WHEN 'SEK' THEN SET v_ConvertedAmount = amount; 
        ELSE SET v_ConvertedAmount = amount; 
    END CASE;

    RETURN v_ConvertedAmount;
END //
DELIMITER ;

INSERT INTO Game_Key (CD_Key, Product_key_id) VALUES ('HAPPY-JUMP-SWEDEN-KEY-2026', 1),
('HAPPY-JUMP-FINLAND-KEY-2026', 1),('HAPPY-JUMP-ISLAND-KEY-2026', 1),
('HAPPY-JUMP-ISLAND-KEY-2026-2', 1);

INSERT INTO Receipt (Customer_id, Product_key_id, Key_id, Store_id, Tax_Paid, TotalPrice) 
VALUES (1, 1, 1, 1, 0.00, 0.00), (3, 1, 2, 5, 0.00, 0.00),(4, 1, 3, 4, 0.00, 0.00),
(4, 1, 4, 4, 0.00, 0.00);
SELECT * FROM Receipt;

CREATE OR REPLACE VIEW Unique_Sell_Countries AS
SELECT 
    rt.CountryName AS Country,
    rt.Currency AS Currency,
    COUNT(r.Receipt_id) AS amountSold,
    SUM(r.Tax_Paid) AS tax,
    SUM(r.TotalPrice) AS totalPrice
FROM Receipt r
JOIN Customer c ON r.Customer_id = c.Customer_id
JOIN Region_Tax rt ON c.CountryCode = rt.CountryCode
GROUP BY rt.CountryName, rt.Currency;
SELECT * FROM Unique_Sell_Countries;

CREATE OR REPLACE VIEW All_managers AS
SELECT 
	e.Employee_id as Employee,
    e.Role as Role,
	d.Occupations as Occpations,
    e.Location as Cites
from employee e inner join Department d ON e.Department_id = d.Department_id WHERE Is_Manager = 1;
SELECT * FROM All_managers;

CREATE OR REPLACE VIEW The_calulations_tax_revenue AS
SELECT
	rt.CountryName AS Country,
	r.Tax_Paid as tax,
	ConvertToSEK(r.Tax_Paid, rt.Currency) AS Tax_To_SEK,
    r.TotalPrice as price,
    ConvertToSEK(r.TotalPrice, rt.Currency) AS Price_To_SEK
FROM Receipt r JOIN Customer c ON r.Customer_id = c.Customer_id
JOIN Region_Tax rt ON c.CountryCode = rt.CountryCode;
select * from The_calulations_tax_revenue;

CREATE OR REPLACE VIEW tax_revenue AS
SELECT 
	COUNT(r.Receipt_id) AS Amount_sales,
    SUM(ConvertToSEK(r.TotalPrice, rt.Currency)) AS Total_Global_Revenue_SEK,
	SUM(ConvertToSEK(r.Tax_Paid, rt.Currency)) AS Total_Global_Tax_SEK
FROM Receipt r
JOIN Customer c ON r.Customer_id = c.Customer_id
JOIN Region_Tax rt ON c.CountryCode = rt.CountryCode;
select * from tax_revenue;

CREATE OR REPLACE VIEW name_key AS
SELECT 
	c.Username as username,
    c.Email as email,
    gk.CD_Key as cd_key
FROM Receipt r
JOIN Customer c ON r.Customer_id = c.Customer_id
JOIN Game_Key gk ON r.Key_id = gk.Key_id;
select * from name_key;

SELECT * FROM Company;
SELECT * FROM Department;
SELECT * FROM Employee;
SELECT * FROM Region_Tax;
SELECT * FROM Store;
SELECT * FROM Product;


