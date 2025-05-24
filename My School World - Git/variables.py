import secrets
class DB_VARS:
    SECRET_KEY = secrets.token_hex(32)  # Replace with a secure key
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"  # Replace with your MySQL username
    MYSQL_PASSWORD = "jaya"  # Replace with your MySQL password
    MYSQL_DB = "myschoolworld"