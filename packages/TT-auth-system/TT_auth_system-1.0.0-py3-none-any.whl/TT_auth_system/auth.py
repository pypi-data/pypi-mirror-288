import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pymysql

# Load environment variables from the main project's .env file
load_dotenv()

# SMTP configuration
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # default to 587 if not provided
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
LOGIN_LINK_BASE_URL = os.getenv("LOGIN_LINK_BASE_URL")

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # default to 3306 if not provided
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_TABLE = os.getenv("DB_TABLE")

# Simple in-memory store for valid codes (could be replaced with a database)
valid_codes = {}

def get_user_info(email):
    """Retrieve user information from the database by email."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    try:
        with connection.cursor() as cursor:
            query = f"SELECT FirstName, EmailAddress FROM {DB_TABLE} WHERE EmailAddress = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result:
                first_name, email_address = result
                return first_name, email_address
            return None
    finally:
        connection.close()

def generate_code(length=10):
    """Generate a random code of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_login_email(email, code, first_name):
    """Send a login email with a one-time link."""
    login_link = f"{LOGIN_LINK_BASE_URL}/{code}"

    # Setup Jinja2 environment to load templates from the 'templates' folder
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Load and render the template
    template = env.get_template('otc_email.html')
    html_content = template.render(login_link=login_link, first_name=first_name)

    # Create the email message
    msg = MIMEMultipart()
    msg["Subject"] = "Your Login Link"
    msg["From"] = SMTP_USERNAME
    msg["To"] = email

    # Attach the HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Use TLS
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def generate_and_send_email(email, length=10):
    """Generate a random code, send it via email, and store it, if the email exists in the database."""
    user_info = get_user_info(email)
    if user_info:
        first_name, email_address = user_info
        code = generate_code(length)
        send_login_email(email_address, code, first_name)
        store_code(code, email_address)
        return code
    else:
        print("Email not found in the database.")
        return None

def store_code(code, email):
    """Store the code associated with the email."""
    valid_codes[code] = email

def validate_code(code):
    """Validate the given code."""
    return valid_codes.pop(code, None)

def purge_valid_codes():
    """Purge all valid codes from in-program memory."""
    valid_codes.clear()