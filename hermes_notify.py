#!/usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# from email import Encoders
import os
import datetime

from configparser import ConfigParser
config = ConfigParser(allow_no_value=True)
config.read('config.ini')

mail_user = config['email']['user']
mail_pwd = config['email']['password']
to_address = []
for address in config['email_to_address']:
   to_address.append(address)

def mail(to, subject, text, html=None):
   msg = MIMEMultipart()
   msg['From'] = mail_user
   msg['To'] = to
   msg['Subject'] = subject

   if html is None:
      msg.attach(MIMEText(text))
   else:
      msg.attach(MIMEText(html, 'html'))

   mailServer = smtplib.SMTP(config['email']['smtp'], config['email']['port'])
   mailServer.ehlo()
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.login(mail_user, mail_pwd)
   mailServer.sendmail(mail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def warn_html(subject,content):
    for address in to_address:
        mail(address,subject,content, html=content)


def warn(subject,content):
    for address in to_address:
        mail(address,subject,content)
