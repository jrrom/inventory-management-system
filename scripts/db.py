# Script to setup database for program use.

# Import MySQL Connector and get environment variables for database connection
import mysql.connector
from dotenv import dotenv_values

# Get environment values from .env
config = dotenv_values()

try:
    # Connect to MySQL 
    cnx = mysql.connector.connect(user=config["user"], password=config["password"])
    # Create "Cursor" to execute MySQL commands
    cnx_cursor = cnx.cursor()
    # Create database 
    cnx_cursor.execute("""
        CREATE DATABASE IF NOT EXISTS inventory;
        USE inventory;
    """)
    cnx_cursor.close()
    cnx.close()

    # Connect to table
    db = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )
    # Create "Cursor" to execute MySQL commands
    db_cursor = db.cursor()
    # Create products and logs tables
    db_cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS products(
                id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
                name VARCHAR(255) NOT NULL,
                quantity INT SIGNED NOT NULL,
                retail_price FLOAT NOT NULL,
                wholesale_price FLOAT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS logs(
                id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                message TEXT(65532) NOT NULL
            );
        """
    )
    db.close()
    db_cursor.close()

# Print error if there is error
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)