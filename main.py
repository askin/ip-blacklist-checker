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

config = ConfigParser(allow_no_value=True)
config.read('config.ini')
send_email = config['default'].getboolean('send_email')

def main():
    endResult = []

    for serverIp in config['ip_address']:
        try:
            rt = checkIp(serverIp)
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
        notify(endResult)
    else:
        sendRelief()

def notify(result):
    template = Template(open('layout.html', 'r').read())
    rst = template.render(results=result)
    if send_email:
        hermes_notify.warn_html(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" MAIL SERVER IPS CHECK", rst)
    else:
        print(rst)

def sendRelief():
    if send_email:
        hermes_notify.warn(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" MAIL SERVER IPS CHECK", "HOORAY!! NONE OF THE IPs LISTED!!!")
    else:
        print("HOORAY!! NONE OF THE IPs LISTED!!!")


def checkIp(serverIp):
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
    main()
