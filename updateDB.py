# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
from jira import JIRA
import requests
import json
import getpass

ID = 'sangwoo.ahn'
PW = getpass.getpass()

harmony_server = 'https://harmony.lge.com:8443/issue'
headers = {"Accept": "application/json", 'Content-Type':'application/json'}
search_url = '/rest/api/2/search'


def get_remoteLink(key):
    url = "https://harmony.lge.com:8443/issue/rest/api/2/issue/" + str(key) + '/remotelink'

    result = requests.get(url, params={'os_username': ID, 'os_password': PW}).json()

    for part in result:
        project = part['object']['title'].split('-')[0]
        for target, label in TABLE.items():
            if project == target :
                print('------------------------------------ bingo ------------------------------------')
                print('Detected : ', project, label)
                return key, label
    return None, None

def update_label(issue, label):
    if label not in issue.fields.labels:
        print('Fianlly : ',issue.key, label)
        issue.fields.labels.append(label)
        issue.update(fields={"labels": issue.fields.labels})

def getSoc(project):
    if project in ('WOSQRTK','KTASKWBS','SOCTSRTK','RTKREQII'):
        return 'rtk'
    elif project in ('WOSQMTK','LMTASKWBS','SOCTSMTK','MTKREQ'):
        return 'mtk'
    else:
        return 'undefined'

def getHistoryItems(tmp,option):
    SERVER = harmony_server
    issue = tmp['key']
    url = SERVER + '/rest/api/2/issue/' + str(issue) + '?expand=changelog'
    result = requests.get(url, params={'os_username': ID, 'os_password': PW}).json()

    dueSet = set()
    assigneeList = list()
    fFirstAssignee = True
    for history in result['changelog']['histories']:
        for subHistory in history['items']:
            # 1. duedate
            if option == 'duedate':
                if result['fields']['duedate'] != None:
                    dueSet.add(result['fields']['duedate'])
                if subHistory['field'] == 'duedate':
                    if subHistory['from'] != None:
                        dueSet.add(subHistory['from'])
                    dueSet.add(subHistory['to'])

            # 2. assignee
            if option == 'assignee':
                if subHistory['field'] == 'assignee':
                    if fFirstAssignee == True:
                        assigneeList.append(subHistory['from'])
                        fFirstAssignee = False
                    if subHistory['toString'] != None and 'lge' not in subHistory['toString'] and 'WBS' not in subHistory['toString']:
                        assigneeList.append(subHistory['to'])

            # 3. Reopened Count


            # if 'lge' not in result['fields']['assignee']:
    if option == 'duedate':
        return list(dueSet)
    if option == 'assignee':
        return assigneeList


def main():
    RTK_JQL = 'project in (wosqrtk) AND filter = rtk.members AND resolution = Unresolved'
    # MTK_JQL = 'filter = mtk.lmtask.official.issue '
    # JQL = {RTK_JQL, MTK_JQL}
    JQL = {RTK_JQL}

    SERVER = harmony_server
    fields = ['labels','created','customfield_13827','components','duedate']
    final_list = list()
    # print(SERVER + url)

    for jql in JQL:
        result = requests.get(SERVER + search_url, params={'jql': jql, 'os_username': ID, 'os_password': PW, 'fields': fields}).json()
        for issue in result['issues']:
            field = issue['fields']
            tmp = dict()
            tmp['key']     = issue['key']
            tmp['project'] = tmp['key'].split('-')[0]
            tmp['created'] = field['created']
            tmp['soc']     = getSoc(tmp['project'])
            tmp['chip']    = field['customfield_13827'][0].lower()
            tmp['component'] = field['components'][0]['name']
            tmp['duedate'] = getHistoryItems(tmp,'duedate')
            tmp['assignee'] = getHistoryItems(tmp, 'assignee')


            final_list.append(tmp)
        for i in final_list:
            print(i)



if __name__ == '__main__':
	main()
  
# socIssue	/ soc 이슈인지 유무	/ 이슈생성 ~ closed	/ int	1 : soc, 2 : lge, 3 : not yet resolved
# emptyDueCnt	/issue가 create 되고 첫 duedate 입력까지 걸린 일 수	/이슈생성 ~ 첫 duedate 입력	
# overDueCnt	/over duedate로 유지된 일 수	매크로 시작일 ~ closed	
# reopened	reopen된 횟 수	이슈생성 ~ closed	
# daysSpent	이슈생성 후 첫 Fixready까지 걸린 일 수	이슈생성 ~ 1st Fixready	
# daysTotal	이슈생성 후 마지막 Fixready까지 걸린 일 수 = 이슈 개선에 들어간 총 일 수	이슈생성 ~ last Fixready	
# socCommentCnt	SoC업체 인원의 comment 수	이슈생성 ~ closed	
# lgeCommentCnt	LGE인원의 comment 수	이슈생성 ~ closed	
# commentRuleCnt	comment rule 위반 일 수 rule : 매일 status 업데이트	이슈생성 ~ closed assignee = soc 인원	
# fixreadyRule	fixready 없이 closed되었는지 유무	이슈생성 ~ closed	 bool	true / false
#  labelRule(RTK only)	 <SOC>_RESOLVED or NOT_<SOC>_ISSUE 라벨 없이 Close되었는지 유무 ex) RTK_RESOLVED, NOT_RTK_ISSUE
