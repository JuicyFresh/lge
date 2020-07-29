# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
import requests
import json
import getpass

ID = 'sangwoo.ahn'
PW = getpass.getpass()

harmony_server = 'https://harmony.lge.com:8443/issue'
headers = {"Accept": "application/json", 'Content-Type':'application/json'}
search_url = '/rest/api/2/search'
changelog_url_1 = '/rest/api/2/issue/'
changelog_url_2 = '?expand=changelog'
issue_url = '/rest/api/2/issue/'
label_url = '/rest/api/2/label/'

TABLE = {'TVOQAISSUE':'bm.oqa', 'WEBOSMXPR':'bm.branch', 'TVCSISSUE':'bm.cs','CERTTWENTY':'bm.cert', 'NATIVEAPP':'bm.cert',\
         'SWAUTO':'bm.etc','UHDRTK':'bm.etc','UHDMTKLMU':'bm.ppsw','UHDRTKLMU':'bm.ppsw' }



def get_remoteLink(key):
    url = "https://harmony.lge.com:8443/issue/rest/api/2/issue/" + str(key) + '/remotelink'

    result = requests.get(url, params={'os_username': ID, 'os_password': PW}).json()

    for part in result:
        project = part['object']['title'].split('-')[0]
        for target, label in TABLE.items():
            if project == target :
                print('Detected : ', project, label)
                return key, label
    return None, None

def update_label(issue, label,SERVER):
    if label not in issue['fields']['labels']:
        key = issue['key']
        print('------------------------------------ bingo ------------------------------------')
        payload = json.dumps({
            'update': {
                'labels': [
                    {
                        'add': label
                    }
                ]
            }
        })
        rest = requests.request("PUT", SERVER + issue_url + key, data=payload, headers=headers,
                                params={'os_username': ID, 'os_password': PW})
        print(rest)

def main():
    RTK_JQL = 'project in (KTASKWBS) AND filter = rtk.members AND resolution = Unresolved'
    # MTK_JQL = 'filter = mtk.lmtask.official.issue '
    MTK_Q_JQL = 'filter = lm21x.total'
    MTK_DEV_JQL = 'filter = lm21x.dev.total'
    # JQL = {RTK_JQL}
    JQL = {MTK_Q_JQL, MTK_DEV_JQL}
    SERVER = harmony_server
    fields = ['labels']

    for QERRY in JQL:
        STARTAT = 0
        MAXRESULTS = 1000
        issues = requests.get(SERVER + search_url, params={'jql': QERRY, 'os_username': ID, 'os_password': PW, 'fields': fields,'startAt': STARTAT, 'maxResults': MAXRESULTS}).json()
        while STARTAT + MAXRESULTS < issues['total']:
            print('------------------- Over', STARTAT + MAXRESULTS ,'-----------------')
            STARTAT += MAXRESULTS
            rest_tmp = requests.get(SERVER + search_url,params={'jql': QERRY, 'os_username': ID, 'os_password': PW, 'fields': fields,'startAt': STARTAT, 'maxResults': MAXRESULTS}).json()
            issues['issues'] += rest_tmp['issues']

        for idx, issue in enumerate(issues['issues']):
            key, label = get_remoteLink(issue['key'])
            if key is not None:
                update_label(issue,label,SERVER)
        print('TOTAL :', idx)
        print('------------------------------------ END ------------------------------------')

if __name__ == '__main__':
	main()