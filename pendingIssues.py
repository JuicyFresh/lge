# -*- coding: utf-8 -*-

import sys
sys.path.append('./lib')
sys.path.append('./private')
import jiraLib
import emailLib
import htmlLib
import datetime
import collections
import logLib

# f = open("D:\업무\python\private\private.txt",'r')
f = open("/home/sangwoo_ahn/macro/private/private.txt", 'r')
ID = f.readline()[:-1]
PW = f.readline()[:-1]
f.close()
LOG = logLib.log(ID)
OFFSET = '14'

class soc(object):
	def __init__(self, name, server, filter, manager=''):
		self.name = name
		self.server = server
		self.jira = jiraLib.jira(server, ID, PW, LOG)
		self.filter = 'created < "-'+ OFFSET + 'd" and status != FixReady and filter=' + filter
		self.manager = manager

ADDRESS = {'QTRACKER':jiraLib.ISSUE_ADDRESS[0], 'HARMONY':jiraLib.ISSUE_ADDRESS[1], 'DEVTRACKER':jiraLib.ISSUE_ADDRESS[2]}

def main():
	LIST = [soc('SIC','QTRACKER', 'SIC.WEBOS45.ALLCHIP.NOTCLOSED.ALLEVENT', 'SPT-PL@lge.com'),
	        soc('RTK','HARMONY', 'k5lp.total.notresolved', 'andy.park@realtek.com,james.park@realtek.com,jy.lee@realtek.com,gilbert.jang@realtek.com,kevin.baek@realtek.com,hj.lee@realtek.com,Leo.Lee@realtek.com,peter.park@realtek.com' ),
	        soc('MSTAR','HARMONY', 'M3R.Event', 'mkb.lge@mstarsemi.com')]
	for SOC in LIST:
		TIME = datetime.datetime.now()
		LOG.info(SOC.filter)
		issues = SOC.jira.searchIssues(SOC.filter)
		LOG.info(issues)
		html = htmlLib.html()
		html.insertText('<p style = "font-size:11px"> This e-mail will be sent automatically at 8 AM every day.</p>')
		html.insertText('<br></br>')
		html.insertText('<p style = "font-size:16px"><strong> Issues that have not improved for more than ' + OFFSET + ' days in ' + SOC.name + '</strong></p>')
		html.insertText('<p style = "font-size:13px">Date : ' + TIME.strftime("%Y-%m-%d %H:%M") + '</p>')
		html.insertText('<p style = "font-size:13px">Range : webOS4.5 </p>')
		html.insertText('<p style = "font-size:13px">Filter : ' + SOC.filter + '</p>')
		if issues in ([], None):
			html.insertText('<p>없음.</p>')
		else:
			html.insertTable(['Key', 'Summary', 'Status', 'Assignee', 'Partner', 'Created', 'Due', 'Chip'])
			# issueTuple = collections.namedtuple('issue', 'key due assignee status chip created model')
			issueList = []
			for issue in issues:
				LOG.info("{0} was sent".format(issue.key))
				try: # q-tracker
					if(issue.fields.customfield_13802[0]): chip = issue.fields.customfield_13802[0] # 이슈들중에 chip정보가 없는 경우가 있다.
					else: chip = 'Empty'
				except Exception: # harmony
					if (issue.fields.customfield_13827[0]): chip = issue.fields.customfield_13827[0]
					else: chip = 'Empty'
				try :
					if (issue.fields.customfield_10810): parter = issue.fields.customfield_10810  # parter
					else: parter = 'Empty'
				except Exception:
					parter = 'Empty'
				issueList.append([ADDRESS[SOC.server] + issue.key, issue.fields.summary, issue.fields.status.name, issue.fields.assignee.displayName, parter, issue.fields.created.split('T')[0], issue.fields.duedate, chip])
			issueList = sorted(issueList, key=lambda tmp: tmp[3])
			issueList = sorted(issueList, key=lambda tmp: tmp[7])
			for k in issueList:
				html.insertRow(k, 0)
			html.endOftable()
		TITLE = 'Pending Issues of ' + SOC.name
		# TO = 'sangwoo.ahn@lge.com'
		FROM = 'sangwoo.ahn@lge.com'
		# CC = None
		TO = SOC.manager
		CC = 'tbc-bi@lge.com'

		emailLib.sendMsg(FROM=FROM, TO=TO, TITLE=TITLE, MSG=html.getMsg(), CC=CC)


if __name__ == '__main__':
	main()

