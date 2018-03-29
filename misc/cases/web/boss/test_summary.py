# coding=utf-8
# author: zengyuetian
#
# *** Settings ***
# Default Tags
# Library           ../../../lib/web/LoginPage.py
# Library           ../../../lib/web/SummaryPage.py
#
# *** Test Cases ***
# ShowSummaryReport
#     [Tags]    boss
#     [Setup]
#     LoginPage.ResetDriver
#     OpenLoginPage
#     InputUsername    wasu
#     InputPassword    wasubj
#     Submit
#     Sleep    3
#     CloseExitBtn
#     SelectFlowStastics
#     Sleep    3
#     SelectPeerStastics
#     Sleep    3
#     SelectUserStastics
#     Sleep    3
#     SelectOnlineUserStastics
#     Sleep    3
#     SelectBandWidthStastics
#     Sleep    3
#     SwitchToGridReport
#     Sleep    3
#     SwitchToTableReport
#     SummaryPage.Close
