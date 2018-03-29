# coding=utf-8

SDK_FILE = "ys_service_static"
LOG_FILE = "result_log.txt"

REMOTE_SDK_API_PATH = "/root/sdk_api"
REMOTE_SDK_PATH = REMOTE_SDK_API_PATH + "/sdk"
REMOTE_SDK = REMOTE_SDK_PATH + "/{0}".format(SDK_FILE)

PATTERN_DICT = {'POST /session/peers/[0123456789ABCDEF]{32}': '.*version.*natType.*"publicIP.*publicPort.*'
                                                              'privateIP.*privatePort.*stunIP.*',
                # 'DELETE /session/peers/[0123456789ABCDEF]{32}': '^{}',
                'GET /session/peers/[0123456789ABCDEF]{32}': '',
                'POST /distribute/peers/[0123456789ABCDEF]{32}': '.*lsmSize.*universe.*',
                'GET /distribute/peers/[0123456789ABCDEF]{32}\?lsmFree=': '.*files.*\[.*\].*',
                'GET /startliveflv\?user=.*pid=.*url=.*': '.*file_id.*file_url.*',
                'GET /live/.*[0123456789ABCDEF]{32}/seeds\?pid=.*cid=.*': '.*seeds.*\[.*\].*',
                # 'POST /live/[0123456789ABCDEF]{32}/progress.*': '.*timestamp.*peer_id.*chunk_id.*type.*', delete
                'POST /sdk/business_report/v2.*':
                    '.*id.*peer_id.*downloads.*\[.*url.*vvid.*type.*live.*\].*uploads.*flows.*\[.*\].*distributes.*',
                'POST /sdk/control_report/v1.*':
                    '.*peer_id.*duration.*leifengs.*\[.*file_id.*cppc.*download.*provide.*\].*channels.*'
                    '\[.*file_id.*type.*chunk_id.*cdn.*p2p.*\].*',
                # 'POST /sdk/statistic_report/v1.*':
                #     '.*id.*timestamp.*peer_id.*connections.*accept_streams.*denied_streams.*',
                'POST /sdk/error_report/v1.*': '.*id.*peer_id.*errors.*\[.*type.*timestamp.*\].*'}

PATTERN_NAME = {'POST /session/peers/[0123456789ABCDEF]{32}': 'Peer Login',
                'DELETE /session/peers/[0123456789ABCDEF]{32}': 'Peer Logout',
                'GET /session/peers/[0123456789ABCDEF]{32}': 'Peer Heart Beat',
                'POST /distribute/peers/[0123456789ABCDEF]{32}': 'Peer Report LSM',
                'GET /distribute/peers/[0123456789ABCDEF]{32}\?lsmFree=': 'Peer Get Task',
                'GET /startliveflv\?user=.*pid=.*url=.*': 'Peer Start Live Flv',
                'GET /live/.*[0123456789ABCDEF]{32}/seeds\?pid=.*cid=.*': 'Peer Get Live seeds',
                # 'POST /live/[0123456789ABCDEF]{32}/progress.*': 'Peer Progress Report', delete
                'POST /sdk/business_report/v2.*': 'Peer Business Report',
                'POST /sdk/control_report/v1.*': 'Peer Control Report',
                'POST /sdk/error_report/v1.*': 'Peer Error Report',
                'POST /sdk/statistic_report/v1.*': 'Peer Statistic Report'}
