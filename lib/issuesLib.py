# -*- coding: utf-8 -*-

from datetime import date
import datetime
import calendar

class _issues(object):
	def __init__(self, issues):
		self.issues = issues

	def chekEmptyDue(self):
		return [issue for issue in self.issues if issue.fields.duedate == None]
	def checkOverDue(self):
		return [issue for issue in self.issues if issue.fields.duedate if issue.fields.duedate < str(date.today())]
	def checkTodayDue(self):
		return [issue for issue in self.issues if issue.fields.duedate if issue.fields.duedate == str(date.today())]
	def notMatcDueWithWeek(self, weekList):
		return [issue for issue in self.issues if issue.fields.duedate if calendar.day_name[datetime.datetime \
			(int(issue.fields.duedate.split('-')[0]), int(issue.fields.duedate.split('-')[1]), int(issue.fields.duedate.split('-')[2])).weekday()] not in weekList]
	def checkLabel(self, label):
		return [issue for issue in self.issues if label not in issue.fields.labels]
	def uploadLabel(self, target, label):
		for issue in target:
			try:
				print(issue, label, 'label was updated')
				issue.fields.labels.append(label)
				issue.update(fields={"labels": issue.fields.labels})
			except Exception as e:
				print('error 발생 / {0}'.format(e))