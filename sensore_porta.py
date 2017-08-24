
import RPi.GPIO as GPIO
import time
import logging
import logging.handlers

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
	server.login(fromaddr, "ghcgnwkqmgpfageb")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
stato_prec = True #True se chiuso False se aperto
while True:
	input_state = GPIO.input(18)
	if input_state == True and stato_prec == False :
		mail('Porta via Sacchi aperta')
		logger.info('Porta via Sacchi aperta')
		stato_prec = True
	elif input_state == False and stato_prec == True:
		mail('Porta via Sacchi chiusa')
		logger.info('Porta Via Sacchi chiusa')
		stato_prec = False
	
	time.sleep(0.2)
