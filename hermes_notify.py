#!/usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email import Encoders

class HermesNotify:

    def __init__(self, to_address, mail_user, mail_pwd, smtp, smtp_port):
        self.__to_address = to_address
        self.__mail_user = mail_user
        self.__mail_pwd = mail_pwd
        self.__smtp = smtp
        self.__smtp_port = smtp_port


    def mail(self, to, subject, text, html=None):
        msg = MIMEMultipart()
        msg['From'] = self.__mail_user
        msg['To'] = to
        msg['Subject'] = subject

        if html is None:
            msg.attach(MIMEText(text))
        else:
            msg.attach(MIMEText(html, 'html'))

        mailServer = smtplib.SMTP(self.__smtp, self.__smtp_port)
        mailServer.ehlo()
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.login(self.__mail_user, self.__mail_pwd)
        mailServer.sendmail(self.__mail_user, to, msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()


    def warn_html(self, subject, content):
        for address in self.__to_address:
            self.mail(address, subject, content, html=content)


    def warn(self, subject, content):
        for address in self.__to_address:
            self.mail(address, subject, content)
