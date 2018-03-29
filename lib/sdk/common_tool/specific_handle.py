# coding=utf-8
import json
import os
import threading
import re

from lib.sdk.common_tool.sftp_client import *
from lib.sdk.common_tool.ssh_client import *
from lib.request.http_request import *
from distutils.version import StrictVersion

from lib.sdk.sdk_constant import root_path


def occupy_port(sdk_ip, username, password, occupied_port):
    """
        占用远程机器上的某指定端口
    :return:
    """
    sftp_client = SFTPClient(sdk_ip, username, password)
    local_path = os.path.abspath(os.path.dirname(__file__)) + "/socket_server_tcp.py"
    sftp_client.upload(remote_path='/root/sdk_api/socket_server_tcp.py', local_path=local_path)

    ssh_client = SSHClient(sdk_ip, username, password)
    occupy_cmd = "python /root/sdk_api/socket_server_tcp.py {0}".format(occupied_port)
    son_process = threading.Thread(target=ssh_client.execute_command, args=(occupy_cmd,))
    son_process.daemon = True
    son_process.start()
    time.sleep(3)


def release_port(sdk_ip, username, password):
    """
        解除远端机器的某个因socket_server_tcp.py占用的指定端口
    :return:
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    occupy_cmd = "ps aux | grep -v grep | grep socket_server_tcp.py | awk '{print $2}' | xargs kill -9"
    ssh_client.execute_command(occupy_cmd)


def modify_conf_file(sdk_ip, username, password, remote_sdk_path, modified_keyword, new_value):
    """
        改写远端机器上sdk的yunshang.conf文件
    :param sdk_ip:
    :param username:
    :param password:
    :param remote_sdk_path: 远端sdk存放路径
    :param modified_keyword: 需要改写的配置的key
    :param new_value: 改写的值
    :return:
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    get_cmd = "cat {0}/yunshang/yunshang.conf".format(remote_sdk_path)
    stand_out, stand_error = ssh_client.execute_command(get_cmd)
    conf_dict = json.loads(stand_out)

    if new_value == "null":
        conf_dict[modified_keyword] = new_value
        modified_conf = json.dumps(conf_dict).replace('\"null\"', '').replace('"', '\\"')
        set_cmd = 'echo "{0}" > {1}/yunshang/yunshang.conf'.format(modified_conf, remote_sdk_path)
    elif new_value == 'delete field':
        conf_dict.pop(modified_keyword)
        modified_conf = json.dumps(conf_dict).replace('"', '\\"')
        set_cmd = 'echo "{0}" > {1}/yunshang/yunshang.conf'.format(modified_conf, remote_sdk_path)
    else:
        conf_dict[modified_keyword] = new_value
        modified_conf = json.dumps(conf_dict).replace('"', '\\"')
        set_cmd = 'echo "{0}" > {1}/yunshang/yunshang.conf'.format(modified_conf, remote_sdk_path)
    print set_cmd
    ssh_client.execute_command(set_cmd)


def get_32_prefix(string):
    if len(string) >= 32:
        return string[:32]
    else:
        raise Exception("input string total length is less than 32!!!")


def get_sdk_dashboard(sdk_ip, sdk_port, dashboard_tail_url):
    """
        获取sdk dashboard 的信息
    :param sdk_ip:
    :param sdk_port:
    :param dashboard_tail_url:
    :return:
    """
    try:
        response = send_request(
            'SDKDashboard',
            'HTTP',
            'GET',
            sdk_ip,
            sdk_port,
            dashboard_tail_url
        )
    except Exception, e:
        print e
        return False
    return response.text


def get_sdk_conf_file(sdk_ip, username, password, remote_sdk_path):
    """
        获取 sdk yunshang.conf 文件信息
    :param sdk_ip:
    :param username:
    :param password:
    :param remote_sdk_path:
    :return:
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = r"cat {0}/yunshang/yunshang.conf".format(remote_sdk_path)
    stand_out, stand_err = ssh_client.execute_command(cmd)
    return stand_out


def get_json_value(response_text, json_key=None, length=None):
    """
        获取json 某字段的值
    :param response_text:
    :param json_key:
    :param length:获取字段长度
    :return:
    """
    temp = json.loads(response_text)
    if length is None:
        if json_key is None:
            return temp
        else:
            return temp[json_key]
    else:
        return temp[json_key][:int(length)]


def get_sdk_run_log(sdk_ip, username, password, remote_sdk_path):
    """
        获取sdk 运行后的 run log 其中记录了sdk控制台信息
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = r"cat {0}/sdk_run.log".format(remote_sdk_path)
    stand_out, stand_err = ssh_client.execute_command(cmd)
    return stand_out


def get_sdk_version_by_run_log(sdk_ip, username, password, remote_sdk_path):
    """
        获取run log 中的版本号信息
    """
    log = get_sdk_run_log(sdk_ip, username, password, remote_sdk_path)
    re_compile = re.compile(r'\[supervisor\] version (.*)\n')
    version = re_compile.search(log).group(1)
    return str(version)


def check_upgrade_by_run_log(sdk_ip, username, password, remote_sdk_path):
    """
        检查run log中是否有升级请求信息
    """
    log = get_sdk_run_log(sdk_ip, username, password, remote_sdk_path)
    if log.find('check upgrade http://') < 0:
        return False
    else:
        return True


def check_sdk_init_successfully_by_log(sdk_ip, username, password, remote_sdk_path):
    """
    检查run log中是否存在初始化成功信息
    """
    log = get_sdk_run_log(sdk_ip, username, password, remote_sdk_path)
    if log.find('p2p_core_init successfully') < 0:
        return False
    else:
        return True


def replace_core_so_by_other_file(sdk_ip, username, password, remote_sdk_path):
    """
        用其他文件代替 core.so文件
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    stand_out, stand_err = ssh_client.execute_command("ls {0} | grep core".format(remote_sdk_path))
    s = stand_out.split('\n')
    remove_sdk_s(sdk_ip, username, password, remote_sdk_path, '*core*')
    # remove_sdk_s(sdk_ip, username, password, remote_sdk_path, 'yunshang/*core.so*')
    for file_name in s:
        if file_name.find('core') > 0:
            cmd = r"cd {0};cp ys_service {1}".format(remote_sdk_path, file_name)
            ssh_client.execute_command(cmd)


def modify_core_so_file(sdk_ip, username, password, remote_sdk_path):
    """
        修改 ys_service 同级目录下的 core.so文件
    """
    # remove_sdk_s(sdk_ip, username, password, remote_sdk_path, 'yunshang/*core.so*')
    ssh_client = SSHClient(sdk_ip, username, password)
    stand_out, stand_err = ssh_client.execute_command("ls {0} | grep \'so$\'".format(remote_sdk_path))
    cmd = "sed -i '2d' {0}/{1}".format(remote_sdk_path, stand_out.replace('\n', ''))
    ssh_client.execute_command(cmd)


def remove_sdk_s(sdk_ip, username, password, remote_sdk_path, sdk_file_path):
    """
        因为robot的神奇原因，无法调用 sdk_handle.py下的remove方法，就多写了个这玩意儿
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = r"rm -f {0}/{1}".format(remote_sdk_path, sdk_file_path)
    ssh_client.execute_command(cmd)


def get_max_core_version(sdk_ip, username, password, remote_sdk_path):
    """
        获取SDK Core so 文件最大的版本
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    stand_out, stand_err = ssh_client.execute_command("cd {0};strings *.so|grep YunshangSDK/".format(remote_sdk_path))
    re_compile = re.compile(r'YunshangSDK/(.*)')
    versions = re_compile.findall(stand_out)
    a = set(versions)
    max_version = '0.0.0'
    if len(a) == 1:
        max_version = list(a)[0]
        return max_version
    else:
        for version in versions:
            if StrictVersion(version) > StrictVersion(max_version):
                max_version = version
        return max_version


def verify_file_is_exist(sdk_ip, username, password, remote_sdk_path, *files_path):
    """
        确认yunshang目录或yunshang/目录下指定文件是否存在 （通过传入的files_path过滤得到）
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    if files_path == 'yunshang':
        stand_out, stand_err = ssh_client.execute_command("ls {0}|grep {1}".format(remote_sdk_path, 'yunshang'))
        if stand_out == '':
            flag = False
        else:
            flag = True
        return flag
    else:
        flag = True
        for file_path in files_path:
            stand_out, stand_err = ssh_client.execute_command(
                "cd {0};ls {1}|grep {2}".format(remote_sdk_path, 'yunshang/',
                                                file_path))
            if stand_out == '':
                flag = False
        return flag


def execute_command(sdk_ip, username, password, command):
    ssh_client = SSHClient(sdk_ip, username, password)
    ssh_client.execute_command(command)
    pass


def start_capture(sdk_ip, username, password, dev, tcp=1, udp=0, time_out=10000):
    sftp_client = SFTPClient(sdk_ip, username, password)
    local_path = os.path.abspath(os.path.dirname(__file__)) + "/packet_capture.py"
    sftp_client.upload(remote_path='/root/sdk_api/packet_capture.py', local_path=local_path)

    ssh_client = SSHClient(sdk_ip, username, password)
    capture_cmd = "cd /root/sdk_api; python packet_capture.py {} {} {} {}".format(dev, tcp, udp, time_out)
    son_process = threading.Thread(target=ssh_client.execute_command, args=(capture_cmd,))
    son_process.daemon = True
    son_process.start()
    time.sleep(3)


def stop_capture(sdk_ip, username, password):
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = "ps aux | grep packet_capture |grep -v grep | grep -v bash | awk '{print $2}' | xargs kill "
    ssh_client.execute_command(cmd)


def get_interface_macs(sdk_ip, username, password):
    interface_list = [
        'ens',
        'eno',
        'eth',
        'br',
        'wlan']
    ssh_client = SSHClient(sdk_ip, username, password)
    cmd = "ls /sys/class/net"
    cmd_result = ssh_client.execute_command(cmd)
    result = cmd_result[0].split('\n')
    num = len(result)

    for interface in interface_list:
        for i in range(num):
            if interface in result[i]:
                cmd = "cat /sys/class/net/{0}/address".format(result[i])
                stand_out, stand_err = ssh_client.execute_command(cmd)
                print "interface is {0}, macs is {1} ".format(result[i], stand_out)
                return stand_out


def remove_network_monitor_log():
    if os.path.exists(os.path.abspath(os.path.dirname(__file__)) + "/NetworkMonitor.log"):
        os.remove(os.path.abspath(os.path.dirname(__file__)) + "/NetworkMonitor.log")
    else:
        pass


def play(sdk_ip, username, password, remote_sdk_path, file_url):
    """
    使用fake play 模拟sdk播放
    """
    sftp_client = SFTPClient(sdk_ip, username, password)
    flv_parse_path = os.path.join(root_path, "misc/pyplayer/flv_parse.py")
    play_path = os.path.join(root_path, "misc/pyplayer/play.py")
    sftp_client.upload(remote_path=remote_sdk_path + '/flv_parse.py', local_path=flv_parse_path)
    sftp_client.upload(remote_path=remote_sdk_path + '/play.py', local_path=play_path)

    ssh_client = SSHClient(sdk_ip, username, password)
    start_cmd = "nohup python {0} http://127.0.0.1:32717/{1}> /dev/null 2>&1 &".format(remote_sdk_path + "/play.py",
                                                                                       file_url)
    ssh_client.execute_command(start_cmd)
    print "PLAY!"


def stop_play(sdk_ip, username, password):
    """
    停止播放
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    start_cmd = "ps aux |grep python |grep play |grep -v grep |awk '{print $2}' | xargs kill -9"
    ssh_client.execute_command(start_cmd)
    pass


def find_coredump(sdk_ip, username, password, remote_path):
    """
    发现core dump文件
    """
    ssh_client = SSHClient(sdk_ip, username, password)
    ssh_client.execute_command("ulimit -c unlimited")
    find_command = "find {0} -name core.* ".format(remote_path)
    stand_out, stand_er = ssh_client.execute_command(find_command)
    return stand_out.find('core')

# def test_stand_out():
#     ssh_client = SSHClient('192.168.2.44', 'root', 'root')
#     cmd = "ifconfig"
#     stand_out, stand_err = ssh_client.execute_command(cmd)
#     # stand_out, stand_err = ssh_client.execute_command('./root/sdk_api/sdk/ys_service')
#     print stand_out, stand_err

if __name__ == '__main__':
    # occupy_port('10.6.3.28', 'root', 'Yunshang2014', 40000)
    # release_port('10.6.3.28', 'root', 'Yunshang2014')
    # modify_conf_file('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test', 'peer_id',
    #                  '00000000000000000000000000000000')
    # modify_conf_file('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test', 'peer_id', 'null')
    # modify_conf_file('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test', 'peer_id', 'delete file')
    # print get_32_prefix('00000004C10F48719E4A207D2CDA06C0A3432')
    # print get_sdk_run_log('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # print get_sdk_dashboard('10.6.3.28', '32719', '/ajax/login')
    # print get_sdk_version_by_run_log('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # replace_core_so_by_other_file('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # modify_core_so_file('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # print get_max_core_version('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # start_capture('10.6.3.28', 'root', 'Yunshang2014', 'eth0')
    # time.sleep(10)
    # stop_capture('10.6.3.28', 'root', 'Yunshang2014')
    # play('10.6.3.28', 'root', 'Yunshang2014', '/root/sdk_test')
    # stop_play('10.6.3.28', 'root', 'Yunshang2014')
    # response = get_sdk_dashboard('192.168.2.44', '32719', '/ajax/version')
    # print response, type(response)
    # print get_json_value('{"core": "3.11.14", "lsm": 2, "dccp": 2}', 'core')
    # log = get_sdk_run_log('192.168.2.44', 'root', 'root', '/root/sdk_api/sdk')
    # print log
    # re_compile = re.compile(r'\[supervisor\] version (.*)\n')
    # version = re_compile.search(log).group(0)
    # is_upgrade = check_upgrade_by_run_log('192.168.2.44', 'root', 'root', '/root/sdk_api/adk')
    # print is_upgrade
    # occupy_port('192.168.2.44', 'root', 'root', '32717')
    # print check_sdk_init_successfully_by_log('192.168.2.44', 'root', 'root', '/root/sdk_api/sdk')
    # print get_sdk_run_log('192.168.2.44', 'root', 'root', '/root/sdk_api/sdk')
    test_stand_out()
