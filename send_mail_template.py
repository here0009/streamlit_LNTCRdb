# -*- coding: UTF-8 -*-
# reference: https://www.runoob.com/python/python-email.html
# reference: https://www.liaoxuefeng.com/wiki/1016959663602400/1017790702398272
# reference: https://docs.python.org/zh-cn/3/library/smtplib.html


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.header import Header
import os

mail_host="****"
mail_user="****"
mail_pass="****"
mail_port=465
sender_name = '****'
sender_email = '****'

maintainer_receviers = ['****','****']
email_subject = 'Download Request From {}'
email_content = 'Download Request Information:\n{}\nIf download request is approved, send the following temporary download link  to the email address\n{}'
valid_download_link = '****'
test_receviers = ['****']


def send_email(receviers, subject, content, attachment_file=None):
    """
    send email from sender to receviers with content and attachment files
    """
    try:
        message = MIMEMultipart()
        message['From'] = Header(f"{sender_name}<{sender_email}>", 'utf-8')
        message['To'] =  Header('; '.join(receviers), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(f'{content}', 'plain', 'utf-8'))
        if not attachment_file is None:
            att_file = MIMEText(open(attachment_file, 'rb').read(), 'base64', 'utf-8')
            att_file_name = os.path.basename(attachment_file)
            att_file["Content-Type"] = 'application/octet-stream'
            att_file["Content-Disposition"] = f'attachment; filename={att_file_name}'
            message.attach(att_file)
        server = smtplib.SMTP_SSL(mail_host, mail_port)
        # server.set_debuglevel(1)
        server.login(mail_user, mail_pass)
        server.sendmail(sender_email, receviers, message.as_string())
        server.quit()
        response = f"Send mail successefully. Your download request has been submitted. You will receive a download link via email upon approval"
        return response
    except:
        response = f"Could not send mail for now. Please Try later or contact us for solution"
        return response

def send_email_multiple_attachment_file(receviers, subject, content, attachment_files=None):
    """
    send email from sender to receviers with content and attachment files, multiple attachment_files
    """
    try:
        message = MIMEMultipart()
        message['From'] = Header(f"{sender_name}<{sender_email}>", 'utf-8')
        message['To'] =  Header('; '.join(receviers), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(f'{content}', 'plain', 'utf-8'))
        if attachment_files is not None:
            for attachment_file in attachment_files:
                if not attachment_file:
                    continue
                att_file = MIMEText(open(attachment_file, 'rb').read(), 'base64', 'utf-8')
                att_file_name = os.path.basename(attachment_file)
                att_file["Content-Type"] = 'application/octet-stream'
                att_file["Content-Disposition"] = f'attachment; filename={att_file_name}'
                message.attach(att_file)
        server = smtplib.SMTP_SSL(mail_host, mail_port)
        # server.set_debuglevel(1)
        server.login(mail_user, mail_pass)
        server.sendmail(sender_email, receviers, message.as_string())
        server.quit()
        print (f"Send mail successefully to {'; '.join(receviers)}")
    except:
        print (f"Could not send mail to {'; '.join(receviers)}")