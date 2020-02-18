# -*- coding: utf-8 -*-

import collections
import datetime
import sys
sys.path.append('./lib')
sys.path.append('./private')
from jiraLib import jira
import jiraLib
import emailLib
import htmlLib
import logLib

# filter
filterVIDEO   = ['filter = VIDEO.WEBOS45.ALLCHIP.EMPTYDUE.ALLEVENT' , 'filter = VIDEO.WEBOS45.ALLCHIP.OVERDUE.ALLEVENT' , 'filter = VIDEO.WEBOS45.ALLCHIP.TODAYDUE.ALLEVENT']
filterSYSTEM  = ['filter = SYSTEM.WEBOS45.ALLCHIP.EMPTYDUE.ALLEVENT', 'filter = SYSTEM.WEBOS45.ALLCHIP.OVERDUE.ALLEVENT', 'filter = SYSTEM.WEBOS45.ALLCHIP.TODAYDUE.ALLEVENT']
filterCDP     = ['filter = CDP.WEBOS45.ALLCHIP.EMPTYDUE.ALLEVENT'   , 'filter = CDP.WEBOS45.ALLCHIP.OVERDUE.ALLEVENT'   , 'filter = CDP.WEBOS45.ALLCHIP.TODAYDUE.ALLEVENT']
FILTER = [filterSYSTEM, filterCDP, filterVIDEO]
VIDEO_MAILIST  = ['Video Part', 'jongheon.lee@lge.com, seongcheoll.kim@lge.com,jaekyun.kim@lge.com,seonghoon1128.do@lge.com,\
choonghoon.park@lge.com,hyungyong.park@lge.com,mini.nam@lge.com,jihoons.kim@lge.com,yusun85.lee@lge.com,\
donghoon.keum@lge.com,sangchul87.park@lge.com,may.yoon@lge.com,jongsang.park@lge.com']
CDP_MAILIST    = ['CDP Part', 'ykwang.kim@lge.com,sanghyun.han@lge.com,yongchol.kee@lge.com,sungmo.yang@lge.com,cheolhwa.yoo@lge.com,\
kwangshik.kim@lge.com,jungyong.choi@lge.com,yongsu.yoo@lge.com,yk.son@lge.com,seong.lee@lge.com,yookyung.uh@lge.com,\
kyoungwon.seo@lge.com,kenneth0.park@lge.com']
SYSTEM_MAILIST = ['System Part', 'haeyong.pyun@lge.com,kwangseok.kim@lge.com,kyungmok.jun@lge.com,lgjh.kim@lge.com,youhyun.jung@lge.com,\
jeonghyeon.joo@lge.com,jm0122.kang@lge.com,jaesung5.lee@lge.com,ysw.yang@lge.com,byeongkuk.kim@lge.com,\
ks80.jeong@lge.com,sunghoon.jang@lge.com,hyunhojason.lee@lge.com,dy.jin@lge.com']
BI_MAILIST = ['BI Part', 'sangwoo.ahn@lge.com, hojin.koh@lge.com, ashton.lee@lge.com, hyungkyu.noh@lge.com, ieeum.lee@lge.com,sangwoo.ahn@lge.com']



def main():
	# f = open("D:\업무\python\private\private.txt",'r')
	f = open("/home/sangwoo_ahn/macro/private/private.txt", 'r')
	ID = f.readline()[:-1]
	PW = f.readline()[:-1]
	f.close()

	qJira = jira('QTRACKER', ID, PW)
	receiver = [SYSTEM_MAILIST, CDP_MAILIST, VIDEO_MAILIST]

	for i in range(FILTER.__len__()):
		TIME = datetime.datetime.now()
		# 필터에서 이슈 받기 (VIDEO -> CDP -> SYSTEM)
		# [i][0] EMPTY DUE 이슈 받기 / [i][1] Over due 이슈 받기
		_MSG = htmlLib.html()
		TITLE = '[webOS4.5] TBC팀 due date 관리 메일'
		TITLE = TITLE + ' - ' + receiver[i][0]
		_MSG.insertText('<p style = "font-size:11px"> 이 e-mail은 매일 오전 7시/ 오후 4시에 자동으로 전송됩니다. 문의사항이 있으시면 저에게 해주시면됩니다.</p>')
		_MSG.insertText('<br></br>')
		_MSG.insertText('<p><strong>' + receiver[i][0] + '</strong> Empty/Over Due-date Issues </p>')
		_MSG.insertText('<p>범위 : webOS4.5 </p>')
		_MSG.insertText('<p>시점 : ' + TIME.strftime("%Y-%m-%d %H:%M") + '</p>')
		print(receiver[i][0])
		for j in range(FILTER[i].__len__()):
			targetIssues = qJira.searchIssues(FILTER[i][j])
			_MSG.insertText('<div></div>')
			if j == 0:
				_MSG.insertText('<p><strong> < Empty duedate issues ></strong></p>')
				print("Empty Due")
			elif j == 1:
				_MSG.insertText('<p><strong> < Over duedate Issues ></strong></p>')
				print("Over Due")
			elif j == 2:
				_MSG.insertText("<p><strong> < Issues with today's deadline (내일이면 OverDue가 되는 이슈)></strong></p>")
				print("Today Due")
			print('target:',targetIssues)
			if targetIssues == []:
				_MSG.insertText('<p>없음.</p>')
			else:
				_MSG.insertTable(['Key', 'Due', 'Assignee', 'Status', 'Chip', 'Created', 'Model'])

				issueList = []
				for k in targetIssues:
					print(" /", k.key, "was sent")
					try:  # q-tracker
						chip = k.fields.customfield_13802[0]
					except Exception as e:
						print('chip 정보가 없습니다.')
						chip = 'Empty'
					issueList.append([jiraLib.ISSUE_ADDRESS[0] + str(k.key), k.fields.duedate, k.fields.assignee.displayName, k.fields.status.name, chip, k.fields.created.split('T')[0], str(k.fields.components[0]).split(')')[0] + ')'])
				issueList = sorted(issueList, key=lambda tmp: tmp[4])
				issueList = sorted(issueList, key=lambda tmp: tmp[2])

				for k in issueList:
					_MSG.insertRow(k, 0)
				_MSG.endOftable()
		# CC = 'sangwoo.ahn@lge.com, sangwoo.ahn@lge.com'
		# TO = 'sangwoo.ahn@lge.com'
		TO = receiver[i][1]
		CC = 'tbc-bi@lge.com, cheil.lee@lge.com'
		emailLib.sendMsg(FROM='sangwoo.ahn@lge.com', TO=TO, TITLE=TITLE, MSG=_MSG.getMsg(), CC=CC)
if __name__ == '__main__':
	main()
