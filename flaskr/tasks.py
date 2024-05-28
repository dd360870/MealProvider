from celery import shared_task
from flask import current_app
from flask_mail import Mail, Message

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b

@shared_task(ignore_result=False)
def send_email():
  msg = Message(
    subject='Hello',
    recipients=['marvin.cs12@nycu.edu.tw'],
    body='This is a test email sent from Flask-Mail!'
  )
  mail:Mail = current_app.extensions['mail']
  mail.send(msg)
  return 'Email sent succesfully!'