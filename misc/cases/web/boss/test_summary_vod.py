# coding=utf-8
# author: zengyuetian

# *** Settings ***
# Default Tags
# Library           ../../../lib/web/LoginPage.py
# Library           ../../../lib/web/SummaryPage.py
# Library           ../../../lib/web/SummaryVodPage.py
#
# *** Test Cases ***
# ShowSummaryVodReport
#     [Tags]    boss
#     [Setup]
#     LoginPage.ResetDriver
#     OpenLoginPage
#     InputUsername    wasu
#     InputPassword    wasubj
#     Submit
#     Sleep    3
#     CloseExitBtn
#     OpenSummaryVodPage
#     SummaryVodPage.Close
