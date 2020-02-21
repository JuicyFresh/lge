# -*- coding: utf-8 -*-
from jira import JIRA
import requests
from bs4 import BeautifulSoup
import datetime
import json

ID = 'sangwoo.ahn'
PW = '@435tmdqls'

TARGET_CYCLE_NAME = '[NOT USE] BIT_1'
harmony_server = 'https://harmony.lge.com:8443/issue'

def _findIssuesInEpic(jira, epic_key):
    storyList = []
    BASE_JQL = 'project = WOSBIT AND "Epic Link" = '
    JQL = BASE_JQL + str(epic_key)
    stories = jira.search_issues(JQL)
    for story in stories:
        storyList.append(story.key)
    return storyList

def _findLinkedList(jira, parant_key, issue_type):
    issueList = []
    LinkedType = issue_type
    BASE_JQL = 'project = WOSBIT AND issue in linkedIssues('
    JQL = BASE_JQL + str(parant_key) + ',' + LinkedType + ')'
    issues = jira.search_issues(JQL)
    for issue in issues:
        issueList.append(issue.key)
    return issueList

def _getTestCase(test_key):
    # test_key = 'WOSBIT-142'
    testCase = {}
    BASE_URL = 'https://harmony.lge.com:8443/issue/si/jira.issueviews:issue-xml/'
    URL = BASE_URL + test_key + '/' + test_key + '.xml'

    request_data = requests.get(URL, params={'os_username': ID, 'os_password': PW}).text
    soup = BeautifulSoup(request_data, 'html.parser')
    # output1 = soup.select('customfield[id=customfield_14614]')

    rawData = soup.find(id='customfield_14614')
    if rawData != None:
        rawData = rawData.find_all('step')
        for tcData in rawData:
            # print('start')
            testStep = tcData.find('step')
            if testStep != None:
                testCase['step'] = testStep.string
                testCase['data'] = tcData.find('data').string
                testCase['result'] = tcData.find('result').string
                yield testCase

def getCycleId(projectId):
    url = "https://harmony.lge.com:8443/issue/rest/zephyr/latest/cycle/?projectId=" + projectId
    result = requests.get(url, params={'os_username': ID, 'os_password': PW})
    result = result.json()['-1'][0]

    for cycleIDs in result.keys():
        value = result[str(cycleIDs)]
        if type(value) is not int:
            if value['name'] == TARGET_CYCLE_NAME:
                return cycleIDs

def create_execution(jira, test, cycleId, projectId):
    test = 'WOSBIT-142'
    issue = jira.issue(test)
    url = "https://harmony.lge.com:8443/issue/rest/zephyr/latest/execution/"
    headers = {'Content-Type': 'application/json'}
    body = {
        'cycleId': str(cycleId),
        'issueId': str(issue.id),
        'projectId': str(projectId),
        'assignee': str(issue.fields.reporter.name)
    }
    body = json.dumps(body)
    res = requests.post(url, data=body, headers=headers, auth=(ID, PW))
    print(res.text)

def main():
    Initiative_key = 'WOSBIT-1'

    jira = JIRA(harmony_server, basic_auth=(ID, PW))
    issue = jira.issue(Initiative_key)

    # 1. get project ID
    projectId = issue.fields.project.id

    # 2. get cycle ID
    cycleId = getCycleId(projectId)

    # 3. find epics from initiative
    epics = _findLinkedList(jira, Initiative_key, '"relates to"')

    # 4. find stories from epics
    for epic in reversed(epics):
        stories = _findIssuesInEpic(jira,epic)

        # 5. find tests from stories
        for story in reversed(stories):
            tests = _findLinkedList(jira,story, '"relates to"')

            # 6. make execution
            for test in reversed(tests):
                create_execution(jira, test, cycleId, projectId)


if __name__ == '__main__':
	main()