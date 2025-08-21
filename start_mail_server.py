import subprocess
import sys
import os
import time

def start_mail_server():
    print("Starting development mail server on localhost:1025...")
    try:
        # Check Python version to determine which mail server to use
        if sys.version_info >= (3, 12):
            # For Python 3.12+, use aiosmtpd
            try:
                import aiosmtpd
                mail_server_cmd = [sys.executable, '-m', 'aiosmtpd', '-n', '-l', 'localhost:1025']
            except ImportError:
                print("aiosmtpd not found. Installing...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'aiosmtpd'])
                mail_server_cmd = [sys.executable, '-m', 'aiosmtpd', '-n', '-l', 'localhost:1025']
        else:
            # For Python 3.11 and earlier, use built-in smtpd
            mail_server_cmd = [sys.executable, '-m', 'smtpd', '-n', '-c', 'DebuggingServer', 'localhost:1025']
        
        # Start the mail server as a subprocess
        mail_process = subprocess.Popen(
            mail_server_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Give the server a moment to start
        time.sleep(1)
        
        if mail_process.poll() is None:
            print("Mail server started successfully!")
            print("Emails will be captured and displayed in this console.")
            return mail_process
        else:
            print("Failed to start mail server.")
            return None
    except Exception as e:
        print(f"Error starting mail server: {e}")
        return None

if __name__ == "__main__":
    mail_process = start_mail_server()
    if mail_process:
        try:
            # Keep the script running to see mail server output
            while True:
                output = mail_process.stdout.readline()
                if output:
                    print(output.strip())
                if mail_process.poll() is not None:
                    break
        except KeyboardInterrupt:
            print("Stopping mail server...")
            mail_process.terminate()
            mail_process.wait()
            print("Mail server stopped.")