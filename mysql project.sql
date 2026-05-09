USE theproject;

SELECT * FROM Employee;

SELECT * FROM Company;

SELECT * FROM Product;

SELECT * FROM Store;

SELECT * FROM Receipt;



SELECT Employee.EmployeeID, Employee.Role_profile, Company.Employment_Status
FROM Employee
JOIN Company ON Employee.EmployeeID = Company.EmployeeID;


SELECT 
    Store.Location, 
    Store.Quantity, 
    CalculateTax(Product.Price) * Store.Quantity AS inventory_value_with_tax
FROM Store
JOIN Product ON Store.ProductID = Product.ProductID
WHERE Store.ProductID = 1;


SELECT Receipt.ReceiptID,
       Product.Name,
       Store.Location
FROM Receipt
JOIN Product ON Receipt.ProductID = Product.ProductID
JOIN Store ON Receipt.StoreID = Store.StoreID;


SELECT StoreID, COUNT(*) AS TotalSales
FROM Receipt
GROUP BY StoreID;
    
show tables;


