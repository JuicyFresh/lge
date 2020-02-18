# -*- coding: utf-8 -*-
from jira import JIRA
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.styles import Side,  Border, Font
import datetime

ID = ''
PW = ''

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

def _makeStyle(tcSheet, i):
    thinBorder = Border(left=Side(border_style='thin', color='5083c0'),
                        right=Side(border_style='thin', color='5083c0'),
                        top=Side(border_style='thin', color='5083c0'),
                        bottom=Side(border_style='thin', color='5083c0'))

    tcSheet.row_dimensions[i].height = 30
    range = 'A' + str(i) + ":Y" + str(i)
    rows = tcSheet[range]
    for row in rows:
        for cell in row:
            cell.border = thinBorder
            cell.font = Font(name='굴림')


def write_to_excel(wb, jira, epicIssue, storyIssue,test_key, idx):
    tcSheet = wb['TestCase']
    baseIndex = 8

    testcIssue  = jira.issue(test_key, fields='description,summary,assignee,updated')
    testData = _getTestCase(test_key)
    preCondition = testcIssue.fields.description
    epicSummary = epicIssue.fields.summary.rstrip()
    storySummary = storyIssue.fields.summary.rstrip().split('(')[0]
    testSummary = testcIssue.fields.summary.rstrip()


    for i,tc in enumerate(testData):
        index = baseIndex + idx[0]
        # print(index)
        # Module
        tcSheet['a' + str(index)] = epicSummary
        # MID
        tcSheet['b' + str(index)] = 'BIT_'+epicSummary.strip()
        # Function
        tcSheet['c' + str(index)] = storySummary
        # tc_id
        tcSheet['d' + str(index)] = ' ' # 나중에 자동생성 된다고 함.
        # type
        tcSheet['e' + str(index)] = 'Basic'
        # Area
        tcSheet['f' + str(index)] = 'Common'
        # Category
        tcSheet['g' + str(index)] = 'Common'
        # Display
        tcSheet['h' + str(index)] = 'Common'
        # Item_Kor
        tcSheet['i' + str(index)] = testSummary
        # Precondition_Kor
        tcSheet['j' + str(index)] = preCondition.rstrip()
        # Item_Eng
        tcSheet['k' + str(index)] = ' ' #optional
        # Precondition_Eng
        tcSheet['l' + str(index)] = ' ' #optional
        # idx
        tcSheet['m' + str(index)] = i+1
        # Procedure_Kor
        tcSheet['n' + str(index)] = tc['step'].rstrip()
        # Expected Result_Kor
        tcSheet['o' + str(index)] = tc['result'].rstrip()
        # Procedulre_Eng
        tcSheet['p' + str(index)] = ' ' #optional
        # Expected Result_Eng
        tcSheet['q' + str(index)] = ' ' #optional
        # Maker
        tcSheet['r' + str(index)] = testcIssue.fields.assignee.name
        # Date
        tcSheet['s' + str(index)] = testcIssue.fields.updated.split('T')[0]
        # Technique
        tcSheet['t' + str(index)] = 'Legacy' #optional
        # Priority
        tcSheet['u' + str(index)] = 'P1' #optional
        # Compliance
        tcSheet['v' + str(index)] = ' ' #optional
        # Cause
        tcSheet['w' + str(index)] = 'Event'
        # Reason
        tcSheet['x' + str(index)] = 'Wrap_Up'
        # Expected Time
        tcSheet['y' + str(index)] = ' '
        _makeStyle(tcSheet, index)
        print('Epic= {0} {1} / Story= {2} {3} / Test= {4} {5}'.format(epicIssue.key, epicSummary, storyIssue.key,
                                                                      storySummary, test_key, testSummary))

        idx[0] += 1

def main():
    Initiative_key = 'WOSBIT-1'
    jira = JIRA(harmony_server, basic_auth=(ID, PW))
    idx = [0,]
    FILENAME = 'bitToWRTS'
    wb = load_workbook(keep_vba=True, filename=FILENAME+'.xlsm')


    # 1. find epics from initiative
    epics = _findLinkedList(jira, Initiative_key, '"relates to"')
    # print('Epic List = ', epics)

    # 2. find stories from epics
    for epic in reversed(epics):
        stories = _findIssuesInEpic(jira,epic)
        epicIssue = jira.issue(epic, fields='summary,key')
        # 3. find tests from stories
        for story in reversed(stories):
            tests = _findLinkedList(jira,story, '"relates to"')
            storyIssue = jira.issue(story, fields='summary,key')
            # 4. make excel file
            for test in reversed(tests):
                write_to_excel(wb, jira, epicIssue, storyIssue, test, idx)
    FILENAME = FILENAME + '(' + str(datetime.date.today()) + ').xlsm'
    wb.save(FILENAME)
    wb.close()

if __name__ == '__main__':
	main()
