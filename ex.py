# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
import requests
import json
import getpass

# 서버 주소
qTracker_server = 'http://hlm.lge.com/qi'
dev_server = 'http://hlm.lge.com/issue'
harmony_server = 'https://harmony.lge.com:8443/issue'

ID = 'sangwoo.ahn'
PW = getpass.getpass()
# jira server read
# jira = JIRA(dev_server, basic_auth=(ID, PW))
# jira = JIRA(harmony_server, basic_auth=(ID, PW))
# jira = JIRA(qTracker_server, basic_auth=(ID, PW))
# LOG = logLib.log(ID)
# jira = jiraLib.jira('HARMONY',    ID, PW, LOG)

# jira project read
# projects = jira.projects()


# issue read
# issueNo = 'SWPRETEST-279'
issueNo = 'QEVENTTWEN-18918'


def search():
    issueNo = 'SWPRETEST-279'
    issue = jira.issue(issueNo)
    # issues = jira.search_issues('reporter = currentUser()', maxResults=400)
    # issues = jira.search_issues('parent = MSIXTEEN-853', maxResults=400)
    # jira.issue(issues, fields = 'comment,assignee, creator') # 정보를 제한해서 속도를 높인다.
    print(len(issues))


def sort():
    keys = sorted([project.key for project in projects])[2:5]


def comments():
    print('comments')
    issue = jira.issue(issueNo)
    print(issue)
    # # comment read
    # atl_comments = [comment for comment in issue.fields.comment.comments
    #                 if re.search(r'@atlassian.com$', comment.author.emailAddress)]

    # commnet upload
    jira.add_comment(issue, 'Comment text')
    # issue.update(notify=False, comment='Comment text')


def summary_description():
    # summary & description upload
    issue.update(
        summary="I'm different!", description='Changed the summary to be different.')

    # Change the issue without sending updates
    issue.update(notify=False, description='Quiet summary update.')


def label():
    # label update
    # 기존 라벨 삭제
    # You can update the entire labels field like this
    issue.update(fields={"labels": ['AAA', 'BBB']})

    # Or modify the List of existing labels. The new label is unicode with no
    # 기존 라벨 유지한체 추가
    issue.fields.labels.append(u'new_text')
    issue.update(fields={"labels": issue.fields.labels})


def delete():
    issue.delete()


def linking():
    issue2 = jira.issue('RTKREQ-503')
    # print(issue2.raw['self'])
    # issue2  = {'object': {'url': 'https://harmony.lge.com:8443/issue/rest/api/2/issue/883042', 'title':'none'}}
    # issue2 = {'globalId':'system=https://harmony.lge.com:8443/issue/browse/RTKREQ-503', 'object': {'url': 'https://harmony.lge.com:8443/issue/browse/RTKREQ-503', 'title': 'none', 'summary':'summary'}, "relationship":"causes"}
    # issue2 = {'url': 'https://harmony.lge.com:8443/issue/browse/RTKREQ-503', 'title':str(issue2.fields.summary)}
    # issue2 = {'url': 'https://harmony.lge.com:8443/issue/rest/api/2/issue/847317'}

    # jira.add_remote_link(issue, issue2, application=str(issue), relationship='blocks')
    # jira.add_remote_link(issue, issue2)
    # jira.add_simple_link(issue, issue2)
    # jira.add_remote_link('https://harmony.lge.com:8443/issue/browse/RTKREQ-522', 'https://harmony.lge.com:8443/issue/browse/RTKREQ-503', relationship='causes')


# Find the top three projects containing issues reported by admin
def counter():
    issues = jira.search_issues('assignee=admin')
    top_three = Counter(
        [issue.fields.project.key for issue in issues]).most_common(3)


def Chip():
    chip = issue.fields.customfield_13802
    print(chip, chip[0])


def issueHistory(option):
    SERVER = harmony_server
    issue = 'WOSQRTK-15200'
    url = SERVER + '/rest/api/2/issue/' + str(issue) + '?expand=changelog'
    result = requests.get(url, params={'os_username': ID, 'os_password': PW}).json()

    dueSet = set()
    assigneeList = list()
    fFirstAssignee = True
    for history in result['changelog']['histories']:
        for idx, subHistory in enumerate(history['items']):
            # 1. duedate
            if option == 'duedate':
                if result['fields']['duedate'] != None:
                    dueSet.add(result['fields']['duedate'])
                if subHistory['field'] == 'duedate':
                    if subHistory['from'] != None:
                        dueSet.add(subHistory['from'])
                    dueSet.add(subHistory['to'])
                if len(history['items'])-1 == idx:
                    print(len(history['items']), idx)



            # 3. Reopened Count

issueHistory('duedate')