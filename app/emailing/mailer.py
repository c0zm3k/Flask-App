from flask_mail import Message

_mail = None

def init_mail(mail):
    global _mail
    _mail = mail

def send_mail(subject, recipients, body):
    if _mail is None:
        print('[MAIL] Mail not initialized.')
        return
    try:
        msg = Message(subject=subject, recipients=recipients, body=body)
        _mail.send(msg)
    except Exception as e:
        # Dev-friendly fallback
        print(f"[MAIL-DEV] To: {recipients} | Subject: {subject}\n{body}\n(Exception: {e})")
