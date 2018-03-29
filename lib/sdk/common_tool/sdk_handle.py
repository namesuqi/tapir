# coding=utf-8
import os
import threading

from lib.sdk.common_tool.sftp_client import *
from lib.sdk.common_tool.ssh_client import *

'''
    sdk环境布置、启动与环境清理
'''


def remove_sdk(sdk_ip, username, password, remote_sdk_path, sdk_file_path=None):
    ssh_client = SSHClient(sdk_ip, username, password)
    if remote_sdk_path.startswith("/root/") and sdk_file_path is None:
        cmd = r"rm -rf {0}/*".format(remote_sdk_path)
    elif remote_sdk_path.startswith("/root/") and sdk_file_path is not None:
        cmd = r"rm -rf {0}/{1}".format(remote_sdk_path, sdk_file_path)
    else:
        raise Exception("remove path is dangerous!")
    ssh_client.execute_command(cmd)

    print 'remove sdk complete...'


def remove_file(sdk_ip, username, password, remote_path, file_path):
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = r"rm -f {0}/{1}".format(remote_path, file_path)
    ssh_client.execute_command(cmd)

    print 'remove file complete...'


def upload_sdk(sdk_ip, username, password, remote_sdk_path):
    sftp_client = SFTPClient(sdk_ip, username, password)
    local_path = os.path.abspath(os.path.dirname(__file__)) + "/../../../misc/sdk/daily_routine/ys_service_static"
    sftp_client.upload(remote_path=remote_sdk_path + "/ys_service_static", local_path=local_path)
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = r"chmod a+x {0}/ys_service_static".format(remote_sdk_path)
    ssh_client.execute_command(cmd)

    print 'upload ys_service_static complete...'


def upload_full_sdk(sdk_ip, username, password, remote_sdk_path):
    ssh_client = SSHClient(sdk_ip, username, password)
    mkdir_cmd = "mkdir -p {0}".format(remote_sdk_path)
    ssh_client.execute_command(mkdir_cmd)
    sftp_client = SFTPClient(sdk_ip, username, password)
    local_path = os.path.abspath(os.path.dirname(__file__)) + '/../../../misc/sdk/daily_routine/'
    print local_path, remote_sdk_path
    sftp_client.upload_dir(remote_dir_path=remote_sdk_path, local_dir_path=local_path)
    cmd = r"chmod a+x {0}/ys_service*".format(remote_sdk_path)
    ssh_client.execute_command(cmd)

    print 'upload full sdk complete...'


def upload_old_version_sdk(sdk_ip, username, password, remote_sdk_path):
    sftp_client = SFTPClient(sdk_ip, username, password)
    local_path = os.path.abspath(os.path.dirname(__file__)) + '/../../../misc/sdk/core_of_old_version_sdk/'
    sftp_client.upload_dir(remote_dir_path=remote_sdk_path, local_dir_path=local_path)

    print 'upload old version sdk complete...'


def start_sdk(sdk_ip, username, password, remote_sdk_path, start_port=None, user_prefix=None):
    """
        默认启动sdk ys_service_static 文件
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    if start_port is not None:
        cmd = r"cd {0};nohup {1}/ys_service_static -p {2} > /dev/null 2>&1 &".format(remote_sdk_path, remote_sdk_path,
                                                                                     start_port)
    elif user_prefix is not None:
        cmd = r"cd {0};nohup {1}/ys_service_static -u 0x{2} > /dev/null 2>&1 &".format(remote_sdk_path, remote_sdk_path,
                                                                                       user_prefix)
    else:
        cmd = r"cd {0};nohup {1}/ys_service_static > /dev/null 2>&1 &".format(remote_sdk_path, remote_sdk_path)
    ssh_client.execute_command(cmd)

    print 'start sdk complete...'


def start_sdk_ys_service(sdk_ip, username, password, remote_sdk_path, start_port=None, user_prefix=None,
                         save_log=False):
    ssh_client = SSHClient(sdk_ip, username, password)
    if save_log:
        cmd = r"cd {0};nohup {1}/ys_service > sdk_run.log &".format(remote_sdk_path, remote_sdk_path)
        print cmd
        son_process = threading.Thread(target=ssh_client.execute_command, args=(cmd,))
        son_process.daemon = True
        son_process.start()
        time.sleep(3)
    else:
        cmd = r"cd {0};nohup {1}/ys_service > /dev/null 2>&1 & ".format(remote_sdk_path, remote_sdk_path)
        ssh_client.execute_command(cmd)

    print 'start sdk complete...'


def stop_sdk(sdk_ip, username, password):
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd1 = r"ps aux | grep ys_service |grep -v grep |awk '{print $2}' | xargs kill -9"
    ssh_client.execute_command(cmd1)

    print 'kill sdk complete...'


def stop_sdk_kill_all(sdk_ip, username, password):
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = "killall -9 ys_service"
    ssh_client.execute_command(cmd)
    cmd = "killall -9 ys_service_static"
    ssh_client.execute_command(cmd)
    print 'kill sdk complete...'


if __name__ == '__main__':
    # q = get_sdk_dashboard('192.168.2.56', '32719', '/ajax/login')
    # temp = json.loads(q)
    # print temp["status"]

    # upload_sdk('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # upload_full_sdk('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # upload_old_version_sdk('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # start_sdk_ys_service('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test', save_log=True)
    upload_full_sdk('192.168.2.44', 'root', 'root', "/root/sdk_api/sdk")
    # start_sdk_ys_service('192.168.2.44', 'root', 'root', '/root/sdk_api/sdk', save_log=False)
    # stop_sdk_kill_all('192.168.2.44', 'root', 'root')
    # remove_sdk('192.168.2.44', 'root', 'root', '/root/sdk_api/sdk')
    # upload_full_sdk('192.168.4.195', 'root', 'root', "/root/sdk_api/sdk")
    # remove_sdk('192.168.4.195', 'root', 'root', '/root/sdk_api/sdk')
    pass
