import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, DictLoader, select_autoescape
from cryptography.fernet import Fernet, InvalidToken
import base64
import time
import json
import pymysql
import threading
from typing import Optional, Dict, Tuple, Any, Callable

class OTCAuthSystem:
    def __init__(self,
                 smtp_server: Optional[str] = None,
                 smtp_port: Optional[int] = None,
                 smtp_username: Optional[str] = None,
                 smtp_password: Optional[str] = None,
                 login_link_base_url: Optional[str] = None,
                 reply_to_addr: Optional[str] = None,
                 fernet_key: Optional[str] = None,
                 expiration_time: Optional[int] = None,
                 json_file_path: Optional[str] = None,
                 db_host: Optional[str] = None,
                 db_port: Optional[int] = None,
                 db_user: Optional[str] = None,
                 db_password: Optional[str] = None,
                 db_name: Optional[str] = None,
                 db_table: Optional[str] = None,
                 email_template: Optional[str] = None,
                 db_connection_factory: Optional[Callable[[], pymysql.connections.Connection]] = None,
                 smtp_factory: Optional[Callable[[], Any]] = None):
        # Load environment variables from the main project's .env file
        load_dotenv()
        
        # SMTP configuration
        self.smtp_server: str = smtp_server or os.getenv("SMTP_SERVER")
        self.smtp_port: int = smtp_port or int(os.getenv("SMTP_PORT", 587))  # default to 587 if not provided
        self.smtp_username: str = smtp_username or os.getenv("SMTP_USERNAME")
        self.smtp_password: str = smtp_password or os.getenv("SMTP_PASSWORD")
        self.login_link_base_url: str = login_link_base_url or os.getenv("LOGIN_LINK_BASE_URL")

        # Optional Reply-To address
        self.reply_to_addr: Optional[str] = reply_to_addr or os.getenv("REPLY_TO_ADDR")

        # Encryption key for Fernet
        key: str = fernet_key or os.getenv("FERNET_KEY")
        if not key:
            raise ValueError("FERNET_KEY environment variable is required")
        self.fernet: Fernet = Fernet(base64.urlsafe_b64encode(key.encode()))

        # Expiration time for codes in seconds (e.g., 600 seconds = 10 minutes)
        self.expiration_time: int = expiration_time or int(os.getenv("EXPIRATION_TIME", 600))

        # JSON file for storing codes
        self.json_file_path: str = json_file_path or os.getenv("JSON_FILE_PATH", "auth_codes.json")

        # Database configuration
        self.db_host: str = db_host or os.getenv("DB_HOST")
        self.db_port: int = db_port or int(os.getenv("DB_PORT", 3306))  # default to 3306 if not provided
        self.db_user: str = db_user or os.getenv("DB_USER")
        self.db_password: str = db_password or os.getenv("DB_PASSWORD")
        self.db_name: str = db_name or os.getenv("DB_NAME")
        self.db_table: str = db_table or os.getenv("DB_TABLE")

        # Email template configuration
        self.email_template: Optional[str] = email_template

        # Factories for creating connections and clients (can be mocked in tests)
        self.db_connection_factory = db_connection_factory or self._default_db_connection_factory
        self.smtp_factory = smtp_factory or self._default_smtp_factory

        # Start the background thread for cleaning up expired codes
        self.cleanup_interval: int = 6 * 3600  # 6 hours in seconds
        self._start_cleanup_thread()

    def _start_cleanup_thread(self) -> None:
        """Start a background thread to remove expired codes every cleanup_interval seconds."""
        def run_cleanup() -> None:
            while True:
                time.sleep(self.cleanup_interval)
                self._remove_expired_codes()

        thread = threading.Thread(target=run_cleanup, daemon=True)
        thread.start()

    def _read_file(self) -> Dict[str, float]:
        """Read and decrypt the JSON file storing codes and timestamps."""
        try:
            with open(self.json_file_path, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data)
        except (FileNotFoundError, InvalidToken):
            return {}

    def _write_file(self, data: Dict[str, float]) -> None:
        """Encrypt and write data to the JSON file."""
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.json_file_path, 'wb') as f:
            f.write(encrypted_data)

    def _default_db_connection_factory(self) -> pymysql.connections.Connection:
        """Default factory for creating database connections."""
        return pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name,
            port=self.db_port
        )

    def _default_smtp_factory(self) -> Any:
        """Default factory for creating an SMTP client."""
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)
        return server

    def get_user_info(self, email: str) -> Optional[Tuple[str, str]]:
        """Retrieve user information from the database by email."""
        connection = self.db_connection_factory()
        try:
            with connection.cursor() as cursor:
                query = f"SELECT FirstName, EmailAddress FROM {self.db_table} WHERE EmailAddress = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                if result:
                    first_name, email_address = result
                    return first_name, email_address
                return None
        finally:
            connection.close()

    def generate_code(self, email: str) -> str:
        """Encrypt the email address and timestamp to generate a one-time code."""
        timestamp = str(time.time())
        data = f"{email}|{timestamp}"
        encrypted_data = self.fernet.encrypt(data.encode()).decode()
        return encrypted_data

    def send_login_email(self, email: str, code: str, first_name: str) -> None:
        """Send a login email with a one-time link."""
        login_link = f"{self.login_link_base_url}/{code}"

        # Setup Jinja2 environment
        if self.email_template:
            # Use the provided email template string
            env = Environment(
                loader=DictLoader({'otc_email.html': self.email_template}),
                autoescape=select_autoescape(['html', 'xml'])
            )
        else:
            # Load templates from the 'templates' folder
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
        msg["From"] = self.smtp_username
        msg["To"] = email

        # Set the Reply-To address if provided
        if self.reply_to_addr:
            msg.add_header('Reply-To', self.reply_to_addr)

        # Attach the HTML content
        msg.attach(MIMEText(html_content, "html"))

        # Send the email
        with self.smtp_factory() as server:
            server.send_message(msg)

    def generate_and_send_email(self, email: str) -> Optional[str]:
        """Generate a one-time code, send it via email, and store it, if the email exists in the database."""
        user_info = self.get_user_info(email)
        if user_info:
            first_name, email_address = user_info
            code = self.generate_code(email_address)
            self.send_login_email(email_address, code, first_name)
            self.store_code(code)
            return code
        else:
            print("Email not found in the database.")
            return None

    def store_code(self, code: str) -> None:
        """Store the code and timestamp in the encrypted JSON file."""
        data = self._read_file()
        timestamp = time.time()
        data[code] = timestamp
        self._write_file(data)

    def validate_code(self, code: str) -> Optional[str]:
        """Validate the given code by checking if it has expired."""
        data = self._read_file()
        timestamp = data.get(code, None)
        if timestamp:
            current_time = time.time()
            decrypted_data = self.fernet.decrypt(code.encode()).decode()
            email, code_timestamp = decrypted_data.split('|')
            if current_time - float(code_timestamp) > self.expiration_time:
                print("Code has expired.")
                return None
            return email
        print("Invalid or expired code.")
        return None

    def purge_valid_codes(self) -> None:
        """Purge all valid codes from the encrypted JSON file."""
        self._write_file({})

    def _remove_expired_codes(self) -> None:
        """Remove expired codes from the encrypted JSON file."""
        data = self._read_file()
        current_time = time.time()
        updated_data = {
            code: timestamp
            for code, timestamp in data.items()
            if current_time - timestamp <= self.expiration_time
        }
        self._write_file(updated_data)