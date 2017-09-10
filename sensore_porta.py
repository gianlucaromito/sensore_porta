# aggiunto supporto domoticz
import RPi.GPIO as GPIO
import time
import logging
import logging.handlers
import sys
import datetime
import os
import subprocess
import urllib2
import json
import base64
import ssl


#logging, max 2M a file e ne tengo solo 5
LOG_FILENAME = '/home/pi/python/sensore_porta/sensore_porta.log'
logger = logging.getLogger('sensore_porta')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s (%(threadName)-10s) %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler(
			  LOG_FILENAME, maxBytes=2097152, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)


# Settings for the domoticz server
domoticzserver="server:porta"
domoticzusername = "nome"
domoticzpassword = "pass"
domoticzpasscode = "pass"
base64string = base64.encodestring('%s:%s' % (domoticzusername, domoticzpassword)).replace('\n', '')

def mail(sub):
	import smtplib
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
 
 
	fromaddr = "gianluca.romito@gmail.com"
	toaddr ="gianluca.romito@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = sub
 
	body = ""
	msg.attach(MIMEText(body, 'plain'))
 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "pass")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def domoticzrequest (url):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	request = urllib2.Request(url)
	request.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(request, context=ctx)
	return response.read()


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
stato_prec = True #True se chiuso False se aperto
while True:
	input_state = GPIO.input(18)
	if input_state == True and stato_prec == False :
		mail('Porta via Sacchi aperta')
		try:
			domoticzrequest("https://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=12&switchcmd=On&level=0" + "&passcode=" + domoticzpasscode)
		except:
			logger.error('Non sono riuscito ad inserire il dato di porta Aperta in domoticz')
		logger.info('Porta via Sacchi aperta')
		stato_prec = True
	elif input_state == False and stato_prec == True:
		mail('Porta via Sacchi chiusa')
		try:
			domoticzrequest("https://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=12&switchcmd=Off&level=0" + "&passcode=" + domoticzpasscode)
		except:
			logger.error('Non sono riuscito ad inserire il dato di porta Chiusa in domoticz')
		logger.info('Porta Via Sacchi chiusa')
		stato_prec = False
	
	time.sleep(0.2)
