from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Inställningar för din databas
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'botato123', 
    'database': 'theproject'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return """
        <h1>HappyJumpy API - Alla data</h1>
        <p><a href="/getall">Klicka här för att hämta ALL mysql-data (JSON)</a></p>
    """

@app.route('/getall', methods=['GET'])
def get_all_data():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        cursor.execute("SELECT * FROM Employee;")
        employees = cursor.fetchall()

        cursor.execute("SELECT * FROM Company;")
        companies = cursor.fetchall()

        cursor.execute("SELECT * FROM Product;")
        products = cursor.fetchall()

        cursor.execute("SELECT * FROM Store;")
        stores = cursor.fetchall()

        cursor.execute("SELECT * FROM Receipt;")
        receipts = cursor.fetchall()

        cursor.execute("""
            SELECT Employee.EmployeeID, Employee.Role_profile, Company.Employment_Status
            FROM Employee
            JOIN Company ON Employee.EmployeeID = Company.EmployeeID;
        """)
        employee_company_join = cursor.fetchall()

        cursor.execute("""
            SELECT 
                Store.Location, 
                Store.Quantity, 
                CalculateTax(Product.Price) * Store.Quantity AS inventory_value_with_tax
            FROM Store
            JOIN Product ON Store.ProductID = Product.ProductID
            WHERE Store.ProductID = 1;
        """)
        inventory_valuation = cursor.fetchall()

        cursor.execute("""
            SELECT Receipt.ReceiptID,
                   Product.Name,
                   Store.Location
            FROM Receipt
            JOIN Product ON Receipt.ProductID = Product.ProductID
            JOIN Store ON Receipt.StoreID = Store.StoreID;
        """)
        sold_products_by_store = cursor.fetchall()

        cursor.execute("""
            SELECT StoreID,
                   COUNT(*) AS TotalSales
            FROM Receipt
            GROUP BY StoreID;
        """)
        sales_per_store = cursor.fetchall()

        return jsonify({
            "status": "success",
            "database_structure": {
                "tables_found": tables
            },
            "raw_tables": {
                "employees": employees,
                "companies": companies,
                "products": products,
                "stores": stores,
                "receipts": receipts
            },
            "custom_queries": {
                "employee_assignments": employee_company_join,
                "stock_valuation_happyjumpy": inventory_valuation
            },
            "custom_queries": {
                "employee_assignments": employee_company_join,
                "stock_valuation_happyjumpy": inventory_valuation,
                "sold_products_by_store": sold_products_by_store,
                "sales_per_store": sales_per_store
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        con.close()

if __name__ == '__main__':
    app.run(debug=True)