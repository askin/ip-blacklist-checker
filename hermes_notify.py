#!/usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# from email import Encoders
import os
import datetime

def mail(to, subject, text, email_config, html=None):
   msg = MIMEMultipart()
   msg['From'] = email_config['mail_user']
   msg['To'] = to
   msg['Subject'] = subject

   if html is None:
      msg.attach(MIMEText(text))
   else:
      msg.attach(MIMEText(html, 'html'))

   mailServer = smtplib.SMTP(email_config['smtp'], email_config['smtp_port'])
   mailServer.ehlo()
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.login(email_config['mail_user'], email_config['mail_pwd'])
   mailServer.sendmail(email_config['mail_user'], to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def warn_html(subject, content, email_config):
    for address in email_config['to_address']:
        mail(address,subject,content, html=content)


def warn(subject, content, email_config):
    for address in email_config['to_address']:
        mail(address,subject,content)
