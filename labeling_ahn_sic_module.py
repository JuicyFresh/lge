# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
from jiraLib import jira
import logLib
import getpass
import time


def main():
	MODULE_NAME = ['AUDIO', 'HDMI', 'MEDIA', 'DECODER', 'VENC','PVR', 'BACKEND', 'DOLBY', 'PQ', 'VIDEO', 'DEMOD', 'NETWORK',
				  'USB', 'SYSTEM', '신뢰성', 'GRAPHIC', '8K']

	KEWORD_QE = 'SQE'
	KEWORD_QA = '인정'

	LABEL_QE = 'sic_qe'
	LABEL_QA = 'sic_qa'
	LABEL_MODULE = ''
	LABEL_TEST = ''

	FILTER_MODULE_1 = 'filter = SIC.'
	FILTER_MODULE_2 = '.MEMBERS AND resolution = Unresolved AND filter = WEBOS50.PROJECT.SW'
	FILTER_MODULE = 'DEFAULT'

	SLEEP = 1800

	# PW = getpass.getpass()
	# ID = sys.argv[1]

	f = open("/home/bi/work/macro/private/private.txt", 'r')
	ID = f.readline()[:-1]
	PW = f.readline()[:-1]
	f.close()

	LOG = logLib.log(ID)
	LOG.info('Labeling START')
	#============================================================================================


	# SIC
	qJira = jira('QTRACKER', ID, PW, LOG)
	for i in range(MODULE_NAME.__len__()):
		# 라벨 정하기
		LABEL_MODULE = 'SIC_' + MODULE_NAME[i]
		# 필터 정하기
		FILTER_MODULE = FILTER_MODULE_1+MODULE_NAME[i]+FILTER_MODULE_2

		# 필터 사용해서 이슈 뽑기
		issues = qJira.searchIssues(FILTER_MODULE)
		print('filter = ', FILTER_MODULE)
		# print('issues = ', issues)

		for issue in issues:
			print('{0} - '.format(issue), end=' ')

			## 테스트 부서 라벨 업데이트
			# 이미 라벨이 있다면 기존 라벨 유지
			GROUP_UPDATE = True
			if LABEL_QA in issue.fields.labels or LABEL_QE in issue.fields.labels:
				print('skip TEST_GROUP_LABEL', end=' ')
				GROUP_UPDATE = False
				pass
			else:
				if KEWORD_QE in str(issue.fields.components[0]):
					LABEL_TEST = LABEL_QE
				elif KEWORD_QA in str(issue.fields.components[0]):
					LABEL_TEST = LABEL_QA
				issue.fields.labels.append(LABEL_TEST)
				print('Append:{0}'.format(LABEL_TEST), end=' ')

			## 모듈 라벨 업데이트
			# 이미 라벨이 있다면 기존 라벨 유지
			MODULE_UPDATE = True
			for n in MODULE_NAME:
				if 'SIC_' + n in issue.fields.labels:
					print('skip MODULE_LABEL', end=' ')
					MODULE_UPDATE = False

			## (임시) 8K 컴포넌트는 라벨을 8K로 일괄 정리
			chip = issue.fields.customfield_13802
			if (chip is not None) and ('F20' in chip[0]):
				LABEL_MODULE = 'SIC_8K'

			if MODULE_UPDATE == True:
				issue.fields.labels.append(LABEL_MODULE)
				print('Append:{0}'.format(LABEL_MODULE), end=' ')

			# 라벨 최종 submit
			print()
			if GROUP_UPDATE == True or MODULE_UPDATE == True:
				LOG.info('{0} - label : {1}'.format(issue, issue.fields.labels))
				issue.update(fields={"labels": issue.fields.labels})
	LOG.info('Labeling END')

if __name__ == '__main__':
	main()
