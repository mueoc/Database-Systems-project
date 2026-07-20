import os
import mysql.connector
from flask import Flask, render_template, render_template_string
from dotenv import load_dotenv

# 1. Läs in miljövariabler från .env-filen
load_dotenv()

app = Flask(__name__)

# def get_db_connection():
#     return mysql.connector.connect(
#         host=os.getenv('DB_HOST'),
#         user=os.getenv('DB_USER'),
#         password=os.getenv('DB_PASSWORD'),
#         database=os.getenv('DB_NAME')
#     )

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="botato123",
        database="theproject"
    )

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Happy Jumpy database </title>
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
    </div>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
    </style>
    
"""

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as db_err:
        return render_template_string("""
            <div style="font-family:sans-serif; padding:40px; border:2px solid red; background:#fff5f5; border-radius:8px;">
                <h2 style="color:red; margin-top:0;">can't connect to database</h2>            
                <p>control assignment <strong>.env</strong>-file is correctly configured.</p>
                <p><strong>Error message:</strong> {{ err }}</p>
            </div>
        """, err=str(db_err))

    Unique_Sell_Countries = []
    All_managers = []
    The_calulations_tax_revenue = []
    tax_revenue = []
    name_key = []
    sql_error = None

    try:
        cursor.execute("""
            SELECT * FROM Unique_Sell_Countries;
        """)
        Unique_Sell_Countries = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM All_managers;
        """)
        All_managers = cursor.fetchall()
        
        cursor.execute("""
            SELECT * FROM The_calulations_tax_revenue;
        """)
        The_calulations_tax_revenue = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM tax_revenue;
        """)
        tax_revenue = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM name_key;
        """)
        name_key = cursor.fetchall()

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
                <p><em>Tip: Check if your tables or column names are spelled exactly like this in your database.</em></p>
            </div>
        """, err=sql_error)

    try:
        # Försök ladda din HTML-sida
        return render_template_string(HTML_TEMPLATE, Unique_Sell_Countries=Unique_Sell_Countries,
                                tax_revenue=tax_revenue, name_key=name_key,
                                All_managers=All_managers,
                                The_calulations_tax_revenue=The_calulations_tax_revenue)
    except Exception as template_err:

        return render_template_string("""
            <div style="font-family:sans-serif; padding:40px; border:2px solid blue; background:#f0f5ff; border-radius:8px;">
                <h2 style="color:blue; margin-top:0;">html Not Found!</h2>
                <p>Flask cannot find your HTML template. Make sure you have created a folder named exactly <strong>templates</strong> in the same directory as your Python file, and that <strong>index.html</strong> is inside it.</p>
                <p><strong>Technical error:</strong> {{ err }}</p>
            </div>
        """, err=str(template_err))

if __name__ == '__main__':
    app.run(debug=True)