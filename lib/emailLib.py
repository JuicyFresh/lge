# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def sendMsg(FROM, TO, TITLE=None, MSG=None, CC=None):
	# 예시) CC = 'sangwoo.ahn@lge.com, dls-gn@hanmail.net'
	# TLS 사용
	smtp_host = 'lgekrhqmh01.lge.com'
	smtp_port = 25  # 587
	smtp = smtplib.SMTP()
	smtp.connect(smtp_host, smtp_port)
	smtp.ehlo()
	server = MIMEMultipart("alternative")
	server['Subject'] = Header(s=TITLE, charset='utf-8')
	server["From"] = FROM
	server['Cc'] = CC
	server['To'] = TO
	server.attach(MIMEText(MSG, 'html', 'utf-8'))  # 내용 인코딩
	if CC:
		TO = TO.split(',') + CC.split(',')
	print('An e-mail was sent from :', FROM, ' / to: ', TO)
	smtp.sendmail('sangwoo.ahn@lge.com', TO, server.as_string())  # 수신자, 받는사람 e-mail 주소.
#smtp.sendmail(FROM, 'sangwoo.ahn@lge.com', server.as_string())  # 수신자, 받는사람 e-mail 주소.
	smtp.close()

