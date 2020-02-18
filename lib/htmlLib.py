# -*- coding: utf-8 -*-




class html(object):

	def __init__(self):
		self.msg_title = '[webOS4.5] TBC팀 due date 관리 메일'
		self.html_head = '<!DOCTYPE html><html><head><meta charset="utf-8" />'
		self.css = '<style type="text/css">\
		   .table {border-spacing:20; border-collapse:collapse; font-family:Arial, sans-serif;padding:10px;}\
		   .table .title{font-size:13pt; font-family:Arial, Helvetica, sans-serif; weight:bold; color:#B4045F;background-color:#F6CED8; text-align:center}\
		   .table th{border-style:solid; border-width:1px; border-color:#B4045F;}\
		   .table td{border-style:solid; border-width:1px; border-color:#B4045F;}\
		   </style></head><body>'
		self.msg_address_head = '<tr><td class="value"> <a href="http://hlm.lge.com/qi/browse/'
		self.msg_tail = '</body></html>'
		self.message = self.html_head + self.css

	def insertText(self, msg):
		self.message += msg

	def insertTable(self, title): #insertTable() -> insertRow() -> endOftable() 순서로 다 호출해야함.
		text = '<table class="table"><tr class="title">'
		for value in title:
			text += '<th>' + value + '</th>'
		text += '</tr>'
		self.message += text

	def insertRow(self, LIST, linkNo):
		for i in range(LIST.__len__()):
			if i == linkNo:
				address = str(LIST[i]).rsplit('/')
				address = address[len(address)-1]
				self.message += '<tr><td class="value"> <a href="' + str(LIST[i]) + '" target="_blank">' + address + '</a> </td>'
			else:
				self.message += '<td class="value">' + str(LIST[i]) + '</td>'
		self.message += '</tr>'

	def endOftable(self):
		self.message += '</table>'

	def getMsg(self):
		return (self.message + self.msg_tail)

def printhtml(text, level=0):
	import xml.etree.ElementTree as ET
	from bs4 import BeautifulSoup
	text = str(text)
	XML = '<?xml version="1.0"?>'
	XML += text
	text = BeautifulSoup(XML, 'html.parser')
	elem = ET.fromstring(str(text))
	print(elem)
	i = '\n' + level*' '
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + ' '
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			printhtml(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i
