# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
import collabLib
import jiraLib
import logLib

from bs4 import BeautifulSoup
import time
import re
import getpass
import datetime


## gloabl
BM_STAMP = '[SW Integration]'

def _reMakeComment(assignee, comment, server, log):
	try:
		if 'HARMONY' == str(server):
			newComment = 'Dear [~' + assignee + ']\n' + BM_STAMP + str(comment)
		else:
			newComment = '[~' + assignee + ']님\n' + BM_STAMP + str(comment)
		return newComment
	except Exception as e:
		log.error('error 발생 / {0}'.format(e))

def _parseValidData(rawData, LOG):
	data = {}
	for SERVER in jiraLib.SERVER:
		try:
			qRawData = rawData.find('section', attrs={'id': SERVER}).find_all('article')
			dataList = []
			for unit in qRawData:
				dataList.append((':'.join(unit.find('li', attrs={'class': 'comment'}).text.split(':')[1:][0:]),
				                 ':'.join(unit.find('li', attrs={'class': 'filter'}).text.split(':')[1:][0:])))
			data[SERVER] = dataList
		except Exception as e:
			data[SERVER] = []
			LOG.error(e)
	return data

def _uploadCmt(jira, issue, cmt, SERVER, LOG):
	comments = jira[SERVER].readComment(issue, -1)
	if comments == None:
		LOG.info('{0} comment 추가'.format(issue))
		jira[SERVER].addComment(issue, cmt)
	else:
		cmtLen = len(comments)
		for i in range(0, cmtLen - 1):
			if BM_STAMP in comments[i].body:
				LOG.info('{0} 중복 comment 삭제'.format(issue))
				time.sleep(1)
				jira[SERVER].deleteComment(issue, cmtLen - 1 - i)
		if BM_STAMP not in comments[cmtLen - 1].body:
			LOG.info('{0}comment 추가'.format(issue))
			time.sleep(1)
			jira[SERVER].addComment(issue, cmt)
		else:
			if comments[cmtLen-1].body.strip() == cmt.strip():
				LOG.info('{0} 중복 comment에 . 추가'.format(issue))
				cmt += '.'
			LOG.info('{0} comment 수정'.format(issue))
			time.sleep(1)
			jira[SERVER].uploadComment(issue, cmt, 0)
	LOG.info('comment : {0}'.format(cmt.strip()))

def _run(ID, jira, collab, PID, LOG):
	LOG.info("시작")
	collabData = collab.readData(PID)  # data[0] : 페이지 제목 / data[1] : 페이지 내용
	body = BeautifulSoup(collabData[1], 'html.parser')
	URL = re.search('[\d]+', str(body.find('li', attrs={'id': ID})).split('=')[2]).group()
	collabData = collab.readData(URL)
	body = BeautifulSoup(collabData[1], 'html.parser')

	data = _parseValidData(body, LOG)
	for SERVER in jiraLib.SERVER:
		LOG.info(SERVER)
		for unit in data[SERVER]:  # unit[0] : filter / unit[1] : comment
			filter = unit[1]
			# filter = 'filter=TEST.MACRO'
			LOG.info('filter:{0}'.format(filter))
			issues = jira[SERVER].searchIssues(filter)
			if issues == None:
				continue
			for issue in issues:
				LOG.info(issue.key)
				cmt = unit[0]
				# cmt = '테스트중1'
				try:
					issue = jira[SERVER].jira.issue(issue.key)
				except:
					time.sleep(5)
					for i in range(1, 10):
						print('bingo')
					issue = jira[SERVER].jira.issue(issue.key)
				try:
					assignee = jira[SERVER].getAssignee(issue).name
					cmt = _reMakeComment(assignee, cmt, SERVER, LOG)
				except:
					cmt = _reMakeComment(ID, "It is an unassigned issue", SERVER, LOG)

				# comment 업로드
				_uploadCmt(jira, issue, cmt, SERVER, LOG)

def _alarm():

	now = datetime.datetime.now()
	h = now.strftime('%H')
	h1 = now.strftime('%M')
	h2 = now.strftime('%S')

def main():
	# interval = 18000  # 5시간
	# interval = 7200  # 2시간
	# interval = 3600  # 1시간
	# interval = 60  # 1분
	interval = 1800  # 30분
	PID = '748003010'
	PW = getpass.getpass()
	ID = sys.argv[1]

	LOG = logLib.log(ID)
	flag = 0


	collab = collabLib.collab(ID, PW, LOG)
	jira = {}
	jira['HARMONY']    = jiraLib.jira('HARMONY',    ID, PW, LOG)
	jira['QTRACKER']   = jiraLib.jira('QTRACKER',   ID, PW, LOG)
	jira['DEVTRACKER'] = jiraLib.jira('DEVTRACKER', ID, PW, LOG)
	_run(ID, jira, collab, PID, LOG)
	while True:
		now = datetime.datetime.now()
		h = now.strftime('%H')
		m = now.strftime('%M')
		s = now.strftime('%S')
		if h in ('08', '13') and flag == 0:
			LOG.info('{0}시 {1}분 {2}초 매크로 시작'.format(h,m,s))
			_run(ID, jira, collab, PID, LOG)
			flag = 1
		if flag == 1 and h not in ('08', '13'):
			LOG.info('flag toggle : {0}'.format(flag))
			flag = 0

		LOG.info("{0} 초 동안 sleep / flag:{1}".format(interval,flag))
		time.sleep(interval)

	LOG.info('완료')

if __name__ == '__main__':
	main()
	#pass
