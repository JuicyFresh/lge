# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
from jiraLib import jira
import jiraLib
from issuesLib import _issues
import logLib
import getpass

# filter
filterO18     = 'filter = SIC.WEBOS45.O18.NOTCLOSED.ALLEVENT'
filterM16P3   = 'filter = SIC.WEBOS45.M16P3.NOTCLOSED.ALLEVENT'
Q_FILTER = [filterM16P3, filterO18]
Q_LABEL = ['CAT_LV1_M16P3_ONLY', 'CAT_LV1_O18_ONLY']

filterK5Lp  = 'filter=k5lp.total.rtk.open'
filterM3R   = 'filter=M3R.Event'
HAR_FILTER = [filterK5Lp, filterM3R]
HAR_LABEL = ['CAT_LV1_K5LP_ONLY', 'CAT_LV1_M3R_ONLY']

filterO18HDMI21   = 'filter = O18.Hawlk2.Event'
filterM16P3HDMI21 = ''
HDMI21_FILTER = [filterM16P3HDMI21, filterO18HDMI21]

def main():
	#f = open("/home/bi/work/macro/private/private.txt",'r')
	# f = open("D:\업무\python\private\private.txt",'r')
	#ID = f.readline()[:-1]
	#PW = f.readline()[:-1]
	ID = 'gold.keum'
	PW = getpass.getpass()
	#f.close()
	LOG = logLib.log(ID)

	# SIC
	qJira = jira('QTRACKER', ID, PW, LOG)
	for i in range(Q_FILTER.__len__()):
		issues = _issues(qJira.searchIssues(Q_FILTER[i]))
		target = issues.checkLabel(Q_LABEL[i])
		LOG.info('target: {0}'.format(target))
		issues.uploadLabel(target, Q_LABEL[i])

	# RTK, MStar
	harJira = jira('HARMONY', ID, PW, LOG)
	for i in range(HAR_FILTER.__len__()):
		issues = _issues(harJira.searchIssues(HAR_FILTER[i]))
		target = issues.checkLabel(HAR_LABEL[i])
		LOG.info('target: {0}'.format(target))
		issues.uploadLabel(target, HAR_LABEL[i])

	# HDMI2.1 Switch / MStar인원에게 전달된 O18, M16P3이슈
	for i in range(HDMI21_FILTER.__len__()):
		if HDMI21_FILTER[i]:
			issues = _issues(harJira.searchIssues(HDMI21_FILTER[i]))
			target = issues.checkLabel(Q_LABEL[i])
			LOG.info('target: {0}'.format(target))
			issues.uploadLabel(target, Q_LABEL[i])

if __name__ == '__main__':
	main()
