#!/usr/bin/python
from os import system
from smtplib import SMTP
from datetime import datetime
from time import time,sleep
from sys import argv,exit

# make sure you enter your email details here
mailfrom = ''
mailto = ['']
smtpserver = 'smtp.gmail.com:587'
smtpuser = ''
smtppass = ''

if len(argv) < 2:
    print("Usage: {} <openvpn-config-file>".format(argv[0]))
    exit(1)



def send_mail(msg):
        smtpsock = SMTP(smtpserver)
        smtpsock.ehlo()
        smtpsock.starttls()
        smtpsock.login(smtpuser,smtppass)
        msg = ("From: %s\r\nTo: %s\r\n\r\n" % (mailfrom, ", ".join(mailto))) + msg
        smtpsock.sendmail(mailfrom,mailto,msg)
        smtpsock.quit()

vpn_cmd = 'openvpn --config {}'.format(argv[1])
backoff = 1
while(True):
    prev_time = time()
    status = system(vpn_cmd)
    connected_time = time() - prev_time
    if backoff == 1:
        send_mail("{} died with exit status {}, was connected for {} minutes.".format(argv[1],status,int(connected_time/60)))
    if (connected_time < 60):
            sleep(2**backoff)
            backoff += 1
    else:
        backoff = 1
