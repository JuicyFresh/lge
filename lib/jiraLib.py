# -*- coding: utf-8 -*-
from jira import JIRA
import time
import logLib
#서버 주소
qTracker_server = 'http://hlm.lge.com/qi'
dev_server      = 'http://hlm.lge.com/issue'
harmony_server  = 'https://harmony.lge.com:8443/issue'
SERVER = {'QTRACKER':qTracker_server, 'HARMONY':harmony_server, 'DEVTRACKER': dev_server,}
ISSUE_ADDRESS = ['http://hlm.lge.com/qi/browse/', 'https://harmony.lge.com:8443/issue/browse/', 'http://hlm.lge.com/issue/browse/']

DEFAULT_DELAY = 1

class jira(object):
	def __init__(self, server, ID, PW, LOG=None):
		self.jira = JIRA(SERVER[server], basic_auth=(ID, PW))
		if LOG == None:
			self.LOG = print
		else:
			self.LOG = LOG.info

	def searchIssues(self, filter): # filter가 비어있는 경우에 jira는 모든 이슈를 검색해버린다. 주의할것.
		time.sleep(DEFAULT_DELAY)
		# if 'None' in filter:
		# 	return None
		if 'None' in filter:
			self.LOG('필터없음')
			# print('필터없음')
			return None
		try:
			self.LOG('서치 시작')
			# print('서치 시작')
			issues = self.jira.search_issues(filter,maxResults=400) # default 갯수는 50임/ 400이상으로 늘리는건 error발생하는 듯
		except Exception:
			self.LOG('searchIssues restart')
			# print('searchIssues restart')
			time.sleep(10)
			return self.searchIssues(filter)
		return issues


	def findIssue(self, issueNo):
		time.sleep(DEFAULT_DELAY)
		try:
			issue = self.jira.issue(issueNo)
		except:
			time.sleep(10)
			return self.findIssue(issueNo)
		return issue

	def addComment(self, issue, cmt):
		time.sleep(DEFAULT_DELAY)
		try:
			self.jira.add_comment(issue, cmt)
			# issue.update(notify=False, comment=cmt)
			# pass
		except:
			time.sleep(10)
			self.addComment(issue, cmt)
		# pass

	def uploadComment(self, issue, cmt, no=0):
		comments = issue.fields.comment.comments
		if len(comments) > 0:
			time.sleep(DEFAULT_DELAY)
			try:
				comments[len(comments) - 1 - no].update(body=cmt)
			except Exception as e:
				self.LOG('error 발생, comment 수정권한 문제일 수 있습니다.', e)
		else:
			self.LOG('{0}이슈에는 comment가 없습니다.'.format(issue.key))
			return None

	def deleteComment(self, issue, no=0):
		comments = issue.fields.comment.comments
		if len(comments) > 0:
			time.sleep(DEFAULT_DELAY)
			try:
				comments[len(comments) - 1 - no].delete()
			except Exception as e:
				self.LOG('error 발생, comment 수정권한 문제일 수 있습니다.', e)
		else:
			self.LOG('{0}comment가 없습니다.'.format(issue.key))
			return None
	def readComment(self, issue, no=0): # no는 마지막에서 몇번째 커멘트인지를 나타냄, 0이면 마지막 커멘트, 음수이면 모든 커멘트를 리턴함.
		comments = issue.fields.comment.comments
		if len(comments) > 0:
			if no < 0:
				return comments
			else:
				return comments[len(comments) - 1 - no]
		else:
			self.LOG('{0}이슈에는 comment가 없습니다.'.format(issue.key))
			return None

	def getAssignee(self, issue):
		time.sleep(DEFAULT_DELAY)
		try:
			assignee = self.jira.issue(issue.key, fields='assignee').fields.assignee
		except:
			time.sleep(10)
			return self.getAssignee(issue)
		return assignee

	def getReporter(self, issue):
		time.sleep(DEFAULT_DELAY)
		try:
			reporter = self.jira.issue(issue.key, fields='reporter').fields.reporter
		except:
			time.sleep(10)
			return self.getReporter(issue)
		return reporter
