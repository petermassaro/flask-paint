from twilio.rest import Client
from flask import current_app
from threading import Thread 


def sendSMS(recipientNumber, messageContent):
	client = Client(
		current_app.config['TWILIO_ACCOUNT_SID'],
		current_app.config['TWILIO_AUTH_TOKEN']
		)
	message = client.api.account.messages.create(
		to='+1{}'.format(recipientNumber),
		from_=current_app.config['TWILIO_NUMBER'],
		body=messageContent)



