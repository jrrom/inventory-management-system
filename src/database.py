# Script to setup database for program use.

# Import MySQL Connector and get environment variables for database connection
import mysql.connector
from dotenv import dotenv_values

# Get environment values from .env
config = dotenv_values()

# Connect to database
db_connection = mysql.connector.connect(
    host     = config["host"],
    user     = config["user"],
    password = config["password"],
    database = config["database"]
)

# Create "Cursor" to execute MySQL commands
db_cursor = db_connection.cursor()

# Return all products
def fetch_products():
    db_cursor.execute("SELECT * FROM products")
    return db_cursor.fetchall()

# Return specific product from id
def fetch_product(id: int):
    db_cursor.execute(f"SELECT * FROM products WHERE id = {id}")
    return db_cursor.fetchone()

# Return all logs from most recent to least recent
def fetch_logs():
    db_cursor.execute("SELECT * FROM logs ORDER BY date DESC")
    return db_cursor.fetchall()

# Return specific log from id
def fetch_log(id: int):
    db_cursor.execute(f"SELECT * FROM logs WHERE id = {id}")
    return db_cursor.fetchall()

# Insert product into database
def insert_product(name: str, quantity: int, retail_price: float, wholesale_price: float):
    db_cursor.execute(f"""
        INSERT INTO products (name, quantity, retail_price, wholesale_price) 
        VALUES('{name}', {quantity}, {retail_price}, {wholesale_price})
    """)
    db_connection.commit()

# Insert log into logs
def insert_log(message):
    db_cursor.execute(f"INSERT INTO logs (message) VALUES('{message}')")
    db_connection.commit()

# Edit existing product
def edit_product(id: int, name: str, quantity: int, retail_price: float, wholesale_price: float):
    db_cursor.execute(f"""
        UPDATE products
        SET name = '{name}', quantity = {quantity}, retail_price = {retail_price}, wholesale_price = {wholesale_price} 
        WHERE id = {id}
    """)
    db_connection.commit()

# Delete product from products
def delete_product(id: int):
    db_cursor.execute(f"DELETE FROM products WHERE id = {id}")
    db_connection.commit()

# Delete log from logs
def delete_log(id):
    db_cursor.execute(f"DELETE FROM logs WHERE id = {id}")
    db_connection.commit()