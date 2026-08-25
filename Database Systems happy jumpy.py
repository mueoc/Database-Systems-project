import os
import mysql.connector
from flask import Flask, render_template, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy Jumpy database</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            color: #333;
            margin: 0;
            padding: 40px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 40px;
        }
        .section {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }
        h2 {
            color: #2980b9;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
            margin-top: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        tr:hover {
            background-color: #f1f2f6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Database Information</h1>

        {% if receipt %}
        <div class="section">
            <h2>Receipts</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in receipt[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in receipt %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if Company %}
        <div class="section">
            <h2>Company</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in Company[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in Company %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if Department %}
        <div class="section">
            <h2>Department</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in Department[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in Department %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if Employee %}
        <div class="section">
            <h2>Employee</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in Employee[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in Employee %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if Region_Tax %}
        <div class="section">
            <h2>Region Tax</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in Region_Tax[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in Region_Tax %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if Store %}
        <div class="section">
            <h2>Store</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in Store[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in Store %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if Unique_Sell_Countries %}
        <div class="section">
            <h2>Unique Sell Countries</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in Unique_Sell_Countries[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}    
                </tr>
                {% for row in Unique_Sell_Countries %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table> 
        </div>
        {% endif %}

        {% if All_managers %}
        <div class="section">
            <h2>All Managers</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in All_managers[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in All_managers %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}    
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if The_calulations_tax_revenue %}
        <div class="section">
            <h2>The Calculations Tax Revenue</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in The_calulations_tax_revenue[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in The_calulations_tax_revenue %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}    
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if tax_revenue %}
        <div class="section">
            <h2>Tax Revenue</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in tax_revenue[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in tax_revenue %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}    
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {% if name_key %}
        <div class="section">
            <h2>Name Key</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    {% for column in name_key[0].keys() %}
                        <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for row in name_key %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}    
                    </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

    </div>
</body>
</html>
"""
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as db_err:
        return render_template_string("""
            <div style="font-family:sans-serif; padding:40px; border:2px solid red; background:#fff5f5; border-radius:8px;">
                <h2 style="color:red; margin-top:0;">Can't connect to database</h2>            
                <p>Check that your <strong>.env</strong> file is correctly configured.</p>
                <p><strong>Error message:</strong> {{ err }}</p>
            </div>
        """, err=str(db_err))

    receipt = []
    Unique_Sell_Countries = []
    All_managers = []
    The_calulations_tax_revenue = []
    tax_revenue = []
    name_key = []
    Company = []
    Department = []
    Employee = []
    Region_Tax = []
    Store = []
    sql_error = None

    try:
        cursor.execute("SELECT * FROM Receipt;")
        receipt = cursor.fetchall()
    
        cursor.execute("SELECT DISTINCT CountryName FROM Region_Tax;")
        Unique_Sell_Countries = cursor.fetchall()

        cursor.execute("SELECT * FROM Employee WHERE Is_Manager = 1;")
        All_managers = cursor.fetchall()
        
        cursor.execute("SELECT * FROM The_calulations_tax_revenue;")
        The_calulations_tax_revenue = cursor.fetchall()

        cursor.execute("SELECT * FROM tax_revenue;")
        tax_revenue = cursor.fetchall()

        cursor.execute("SELECT * FROM name_key;")
        name_key = cursor.fetchall()

        cursor.execute("SELECT * FROM Company;")
        Company = cursor.fetchall()

        cursor.execute("SELECT * FROM Department;")
        Department = cursor.fetchall()

        cursor.execute("SELECT * FROM Employee;")
        Employee = cursor.fetchall()

        cursor.execute("SELECT * FROM Region_Tax;")
        Region_Tax = cursor.fetchall()

        cursor.execute("SELECT * FROM Store;")
        Store = cursor.fetchall()

    except mysql.connector.Error as err:
        sql_error = str(err)
    finally:
        cursor.close()
        conn.close()

    if sql_error:
        return render_template_string("""
            <div style="font-family:sans-serif; padding:40px; border:2px solid orange; background:#fffaf0; border-radius:8px;">
                <h2 style="color:orange; margin-top:0;">SQL Error Occurred!</h2>
                <p>One of your tables or columns in the database does not match the SQL code in the Python file.</p>
                <p><strong>Error message from MySQL:</strong> {{ err }}</p>
            </div>
        """, err=sql_error)

    return render_template_string(HTML_TEMPLATE, 
                                  receipt=receipt,
                                  Unique_Sell_Countries=Unique_Sell_Countries,
                                  tax_revenue=tax_revenue, 
                                  name_key=name_key,
                                  All_managers=All_managers,
                                  The_calulations_tax_revenue=The_calulations_tax_revenue,
                                  Company=Company,
                                  Department=Department,
                                  Employee=Employee,
                                  Region_Tax=Region_Tax,
                                  Store=Store)

if __name__ == '__main__':
    app.run(debug=True)