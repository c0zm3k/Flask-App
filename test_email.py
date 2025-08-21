from app import create_app
from app.emailing.mailer import send_mail

app = create_app()

with app.app_context():
    print('Sending test email...')
    send_mail('Test Email', ['test@example.com'], 'This is a test email from the Flask application.')
    print('Email sent!')