import os
import sys
from app import create_app

# Check if we should start the mail server
if os.environ.get('START_MAIL_SERVER', 'false').lower() == 'true':
    try:
        from start_mail_server import start_mail_server
        mail_process = start_mail_server()
        if mail_process:
            print("Mail server started successfully!")
    except ImportError:
        print("Warning: start_mail_server.py not found. Mail server not started.")
    except Exception as e:
        print(f"Error starting mail server: {e}")

app = create_app()
