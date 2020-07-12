import smtplib ,ssl


def email_notification(_request_):
	print ("$$$$$$$$$In email Notification$$$$$$$$4")
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "smriti.swtsmi@gmail.com"  # Enter your address
	receiver_email = "rituag2015@gmail.com"  # Enter receiver address
	password = "@n$@l136"
	message = """\
	Subject: Service Notification

	Hi """+ _request_["firstname"] + """ """ +  _request_["lastname"] + """,\n""" + """
	The current status of your service """ + _request_['service'] + """of """+ _request_['app_name']+"""is """+ _request_["value"]+ """."""

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)