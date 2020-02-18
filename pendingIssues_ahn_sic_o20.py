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
f = open("/home/bi/work/macro/private/private.txt", 'r')
# f = open("/home/bi/work/macro/README.md", 'r')
ID = f.readline()[:-1]
PW = f.readline()[:-1]
f.close()
LOG = logLib.log(ID)
OFFSET = '14' # pendding day

class soc(object):
	def __init__(self, name, server, filter, platform, manager=''):
		self.name = name
		self.server = server
		self.jira = jiraLib.jira(server, ID, PW, LOG)
		self.filter = 'created < "-'+ OFFSET + 'd" and status != FixReady and filter=' + filter
		self.platform = platform
		self.manager = manager


ADDRESS = {'QTRACKER':jiraLib.ISSUE_ADDRESS[0], 'HARMONY':jiraLib.ISSUE_ADDRESS[1], 'DEVTRACKER':jiraLib.ISSUE_ADDRESS[2]}



def main():
	LIST = [soc('SIC','QTRACKER', 'SIC.WEBOS50.PENDDING','O20' ,'SPT-PL@lge.com'),]
	for SOC in LIST:
		TIME = datetime.datetime.now()
		LOG.info(SOC.filter)
		issues = SOC.jira.searchIssues(SOC.filter)
		# LOG.info(issues)
		html = htmlLib.html()
		html.insertText('<p style = "font-size:11px"> This e-mail will be sent automatically at 9 AM every day.</p>')
		html.insertText('<br></br>')
		html.insertText('<p style = "font-size:16px"><strong> Issues that have not improved for more than ' + OFFSET + ' days on ' + SOC.platform + '</strong></p>')
		html.insertText('<p style = "font-size:13px">Date : ' + TIME.strftime("%Y-%m-%d %H:%M") + '</p>')
		html.insertText('<p style = "font-size:13px">Range : webOS5.0 </p>')
		html.insertText('<p style = "font-size:13px">Filter : ' + SOC.filter + '</p>')
		if issues in ([], None):
			html.insertText('<p>없음.</p>')
		else:
			html.insertTable(['Key', 'Summary', 'Status', 'Assignee', 'Partner', 'Created', 'Due', 'Chip'])
			# issueTuple = collections.namedtuple('issue', 'key due assignee status chip created model')
			issueList = []
			ASSIGNEE = []
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
				# print(issue.fields.assignee.emailAddress)
				ASSIGNEE.append(issue.fields.assignee.emailAddress)
			issueList = sorted(issueList, key=lambda tmp: tmp[3])
			issueList = sorted(issueList, key=lambda tmp: tmp[7])
			for k in issueList:
				html.insertRow(k, 0)
			html.endOftable()
		TITLE = 'Old issues of ' + SOC.name
		FROM = 'sangwoo.ahn@lge.com'
		TO = SOC.manager
		CC = 'tsi-bi@lge.com, inuk.park@lge.com, yongjoo.kim@lge.com,'
		ASSIGNEE = list(set(ASSIGNEE)) # assignee 중복 제거.
		for person in ','.join(ASSIGNEE):
			CC += person
		LOG.info(CC)


		emailLib.sendMsg(FROM=FROM, TO=TO, TITLE=TITLE, MSG=html.getMsg(), CC=CC)


if __name__ == '__main__':
	main()

