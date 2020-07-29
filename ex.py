#-*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
import jiraLib
from jira import JIRA
import requests
import json
import getpass
import datetime
from requests.auth import HTTPBasicAuth

ID = 'sangwoo.ahn'
PW = getpass.getpass()

qTracker_server = 'http://hlm.lge.com/qi'
dev_server      = 'http://hlm.lge.com/issue'
harmony_server = 'https://harmony.lge.com:8443/issue'

headers = {"Accept": "application/json", 'Content-Type':'application/json'}

TABLE = {'TVOQAISSUE':'bm.oqa', 'WEBOSMXPR':'bm.branch', 'TVCSISSUE':'bm.cs','CERTTWENTY':'bm.cert', 'NATIVEAPP':'bm.cert',\
         'SWAUTO':'bm.etc','UHDRTK':'bm.etc' }

search_url = '/rest/api/2/search'
changelog_url_1 = '/rest/api/2/issue/'
changelog_url_2 = '?expand=changelog'
issue_url = '/rest/api/2/issue/'

# 타겟 라벨링
# 1. over/empty due-date
# 2. MTTR
# 3. reopen 율
# 4. fixready <-> CCC까지 시간
# 5. daily comment 유무
# 6. due-date 변경 횟수
# 7. ccc reject율

def main():
    issue = 'WOSQRTK-15200'
    issue = 'WOSQRTK-15237'
    # issue = 'WOSQRTK-14647'
    SERVER = harmony_server
    url = SERVER + '/rest/api/2/issue/' + str(issue) + '?expand=changelog'
    print(url)

    result = requests.get(url, params={'os_username': ID, 'os_password': PW}).json()

    assigneeList = list()
    fFirstAssignee = True
    for history in result['changelog']['histories']:
        for subHistory in history['items']:
            # 2. assignee
            # print(result['key'])
            # print(subHistory['field'])
            if subHistory['field'] == 'assignee':
                # print(subHistory)
                if fFirstAssignee == True:
                    # assigneeList.append(subHistory['fromString'])
                    assigneeList.append(subHistory['from'])
                    fFirstAssignee = False
                if subHistory['toString'] != None and 'lge' not in subHistory['toString'] and 'WBS' not in subHistory['toString']:
                    # assigneeList.append(subHistory['toString'])
                    assigneeList.append(subHistory['to'])
                    # print(subHistory['toString'])

    if len(assigneeList) == 0:
        print('---------------bingo-------------')
        print(result['fields']['assignee']['name'])
        print('---------------end-------------')
    else:
        print(assigneeList)


    # tmpList = list()
    # print(len(tmpList))

def serach():
    RTK_JQL = 'project in (KTASKWBS) AND filter = rtk.members AND resolution = Unresolved'
    # MTK_JQL = 'filter = mtk.lmtask.official.issue '
    MTK_Q_JQL = 'filter = lm21x.total'
    MTK_DEV_JQL = 'filter = lm21x.dev.total'
    # JQL = {RTK_JQL, MTK_JQL}
    JQL = {MTK_Q_JQL}
    SERVER = harmony_server
    fields = ['labels']

    STARTAT = 0
    MAXRESULTS = 1000
    rest = requests.get(SERVER + search_url, params={'jql': JQL, 'os_username': ID, 'os_password': PW, 'fields': fields,'startAt':STARTAT, 'maxResults':MAXRESULTS}).json()
    while STARTAT+MAXRESULTS < rest['total']:
        STARTAT += MAXRESULTS
        rest_tmp = requests.get(SERVER + search_url,params={'jql': JQL, 'os_username': ID, 'os_password': PW, 'fields': fields,'startAt': STARTAT, 'maxResults': MAXRESULTS}).json()
        rest['issues'] += rest_tmp['issues']

    for issue in rest['issues']:
        print(issue['fields']['labels'])



def labels():
    SERVER = harmony_server
    key = 'KTASKWBS-17517'
    payload = json.dumps({
        'update':{
            'labels':[
                {
                    'add':'bm2'
                }
            ]
        }
    })
    rest = requests.request("PUT", SERVER + issue_url + key, data=payload, headers=headers, params={'os_username':ID, 'os_password':PW})
    print(rest)


if __name__ == '__main__':
	serach()