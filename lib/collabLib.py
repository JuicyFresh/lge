from bs4 import BeautifulSoup
import requests
import time
import logLib




class collab(object):
	def __init__(self, ID, PW, LOG=None):
		self.ID = ID
		self.PW = PW
		if LOG == None:
			self.LOG = print
		else:
			self.LOG = LOG.info

	def readData(self, PID):
	# PID를 입력받으면 [제목, 내용] 으로 리턴 한다.
		URL = 'http://collab.lge.com/main/rest/api/content/' + PID + '?expand=body.view'
		try:
			request_data = requests.get(URL, params={'os_username': self.ID, 'os_password': self.PW})
			# collab_data = requests.get(collab_url, auth=(ID, PW))
			# print(request_data)
			title = request_data.json()['title']
			body  = request_data.json()['body']['view']['value']
		except Exception:
			self.LOG('재시도 (request.get) ')
			time.sleep(10)
			data = self.readData(PID)
			return [data[0],data[1]]
		return [title, body]
