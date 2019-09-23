#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from subprocess import check_output
import traceback
import sys
import json
import hermes_notify
from datetime import datetime
import socket
from jinja2 import Template
from configparser import ConfigParser

def read_config():

    import os
    if not os.path.exists('config.ini'):
        print("Error: config file is not found!!!", file=sys.stderr)
        sys.exit(1)

    config = ConfigParser(allow_no_value=True)
    config.read('config.ini')
    send_email = config['default'].getboolean('send_email')

    ip_address = [ip for ip in config['ip_address']]

    to_address = []
    for address in config['email_to_address']:
        to_address.append(address)

    email_config = {
        'to_address': to_address,
        'mail_user': config['email']['user'],
        'mail_pwd': config['email']['password'],
        'smtp': config['email']['smtp'],
        'smtp_port': config['email']['port']
    }

    return {
        'config': config,
        'email_config': email_config,
        'send_email': send_email
    }

def main(all_config):
    endResult = []
    config = all_config['config']

    for serverIp in config['ip_address']:
        try:
            rt = checkIp(serverIp, all_config)
            if rt is not None:
                endResult.append(rt)
        except Exception as err:
            print(traceback.format_exc())
            endResult.append({"ip": serverIp,
                              "status": "error"})

    hasBlacklisted=False

    for result in endResult:
        if result["status"]=="listed":
            hasBlacklisted=True

    if hasBlacklisted:
        notify(endResult, all_config)
    else:
        sendRelief(all_config)

def notify(result, all_config):

    send_email = all_config['send_email']
    email_config = all_config['email_config']

    template = Template(open('layout.html', 'r').read())
    rst = template.render(results=result)
    if send_email:
        hermes_notify.warn_html(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" MAIL SERVER IPS CHECK", rst, email_config)
    else:
        print(rst)

def sendRelief(all_config):

    send_email = all_config['send_email']
    email_config = all_config['email_config']

    if send_email:
        hermes_notify.warn(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" MAIL SERVER IPS CHECK", "HOORAY!! NONE OF THE IPs LISTED!!!", email_config)
    else:
        print("HOORAY!! NONE OF THE IPs LISTED!!!")


def checkIp(serverIp, all_config):

    config = all_config['config']

    reverseIp=getReversedIp(serverIp)
    markedLists=[]

    for dnsbl in config['blacklists']:
        try:
            # print("dig +short {}.{}".format(reverseIp, dnsbl))
            answer = check_output(["dig" ,"+short", reverseIp + "." + dnsbl])

            answer=answer.decode().strip()

            if answer.startswith('127'):
                markedLists.append({"answer":answer,"bl":dnsbl})

        except:
            pass

    if len(markedLists)!=0:
        try:
            ptr = socket.gethostbyaddr(serverIp)[0]
        except:
            ptr = 'No Reverse'

        return {"ip":serverIp,
                "status":"listed",
                "markedLists":markedLists,
                "ptr": ptr}

def getReversedIp(serverIp):
    return ".".join(serverIp.split(".")[::-1])


if __name__ == '__main__':
    config = read_config()
    main(config)
