import smtplib ,ssl


def email_notification(_request_):
	print ("$$$$$$$$$In email Notification$$$$$$$$")
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "smriti.swtsmi@gmail.com"  # Enter your address
	receiver_email = _request_['email']  # Enter receiver address
	password = "@n$@l136"
	message = f"""\
	From: {sender_email}
	To: {receiver_email}
	Subject: "Service Notification"

	Hi {_request_["firstname"]},\n{_request_['message']}"""
	
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)