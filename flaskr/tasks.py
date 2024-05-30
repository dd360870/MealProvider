import logging
from celery import shared_task
from flask import current_app, render_template
from flask_mail import Mail, Message
from flaskr.model import Bill
from datetime import date, timedelta

@shared_task()
def save_bill():
    """Save bill of last month
    """
    last_month = date.today().replace(day=1) - timedelta(days=1)
    Bill.save_bills(last_month.year, last_month.month)

@shared_task()
def send_bill_mail():
    user_bills = Bill.get_user_bills()

    for row in user_bills:
        if row['user'].email is None or row['user'].email == '':
            # 沒有設定 email 暫時跳過
            continue

        logging.info("send mail to " + row['user'].email)

        txt_content = ''
        html_content = render_template('email_template/bill_notify.html', user=row['user'], details=row['detail'])

        send_email.delay(row['user'].email, '結帳通知', txt_content, html_content)

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b

@shared_task(ignore_result=False)
def send_email(recipient, subject, body, html):
    msg = Message(
        subject=subject,
        recipients=[recipient],
        body=body,
        html=html
    )
    mail:Mail = current_app.extensions['mail']
    mail.send(msg)
    return 'Email sent succesfully!'