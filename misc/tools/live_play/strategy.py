# coding=utf-8
# author: zengyuetian
import inspect
import paramiko
import threading
import time
import ConfigParser
import os
import sys
import random

SDK_IP_LIST = []
SDK_NUM_LIST = []
SDK_USER_NAME_LIST = []
SDK_PASSWORD_LIST = []
CHANNEL_URL_LIST = []

REQUEST_TIMEOUT = 5  # HTTP request timeout
STREAM_TARGET = 32  # How many stream connection we expected
THREAD_INTERVAL = 0.2  # Seconds

# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)

REMOTE_SDK_PATH = '/home/admin/live'
REMOTE_PLAYER_PATH = '/home/admin/player'
SDK_FILE = 'ys_service_static'
INI_FILE = 'host.ini'
REMOTE_SDK_FILE = '{0}/{1}'.format(REMOTE_SDK_PATH, SDK_FILE)

SDK_PORT_START = 60000
SDK_PORT_STEP = 10
SSH_PORT = 22
USERNAME = "admin"
PASSWORD = "yzhxc9!"
CHANNEL_URL = "live_flv/user/yunduan?url=http://rtmpp2p.meixiu98.com/cloudtropy/NziyzDYmxxgRJ30.flv"

# ini file and sdk file placed in current dir
SDK_FILE_PATH = "{0}/{1}".format(parent_path, SDK_FILE)
INI_FILE_PATH = "{0}/{1}".format(parent_path, INI_FILE)

# only get data from SDK which has specified prefix
USE_LF_PREFIX = ""
# USE_LF_PREFIX = " -x 00010047 "

# USER_PREFIX = ""
USER_PREFIX = " -u 0x075bcfbd "


def read_ini():
    """
    get configure info from ini file
    :return: None
    """
    total_sdk = 0
    config = ConfigParser.ConfigParser()
    config.readfp(open(INI_FILE_PATH))
    section_list = config.sections()
    for i in section_list:
        if config.has_section(i):
            SDK_IP_LIST.append(config.get(i, "IP"))
            # SDK_USER_NAME_LIST.append(config.get(i, "Username"))
            SDK_USER_NAME_LIST.append(USERNAME)
            # SDK_PASSWORD_LIST.append(config.get(i, "Password"))
            SDK_PASSWORD_LIST.append(PASSWORD)
            sdk_num = int(config.get(i, "SDK_Number"))
            SDK_NUM_LIST.append(sdk_num)
            total_sdk += sdk_num
            # CHANNEL_URL_LIST.append(config.get(i, "Channel_URL"))
            CHANNEL_URL_LIST.append(CHANNEL_URL)

    return total_sdk


class RemoteDeployer(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        # print [username, password]

    def deploy_folder(self, local_dir, remote_dir, kill_proc=None):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        if kill_proc is not None:
            ssh.exec_command("killall -9 {0}".format(kill_proc))
            print "kill process {0}".format(kill_proc)
        ssh.exec_command("rm -rf {0}".format(remote_dir))
        ssh.exec_command("mkdir -p {0}".format(remote_dir))
        ssh.close()
        self.copy_via_paramiko(local_dir, remote_dir)

    def copy_via_paramiko(self, local_path, remote_path):
        t = paramiko.Transport(self.ip, SSH_PORT)
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print local_path, remote_path
        if remote_path == REMOTE_PLAYER_PATH:
            sftp.put(local_path + "/flv_play.py", remote_path + "/flv_play.py")
            sftp.put(local_path + "/flv_parse.py", remote_path + "/flv_parse.py")
        else:
            sftp.put(local_path, remote_path)

        t.close()


class RemoteNode(object):
    def __init__(self, ip, sdk_nums, url, local_sdk, username, password):
        self.local_sdk = local_sdk
        self.sdk_nums = sdk_nums
        self.ip = ip
        self.url = url
        self.username = username
        self.password = password
        # print [username, password]

    def stop_sdk(self, i):
        """
        stop specified SDK on remote machine
        :param i: SDK index
        :return: Node
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        command = "killall -9 {0}_{1}".format(SDK_FILE, i)
        ssh.exec_command(command)
        print "Stop SDK for {0}:{1}".format(self.ip, i), "Command:", command
        ssh.close()

    def stop_sdk_all(self):
        """
        stop all SDKs on remote machines
        :return: None
        """
        print "Stop All SDK for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        print_str = "{print $2}"
        command = "ps aux | grep {0} |grep -v grep |awk -F ' ' '{1}' | xargs kill -9".format(SDK_FILE, print_str)
        ssh.exec_command(command)
        print "Command:", command
        ssh.close()

    def start_sdk(self, i):
        """
        Start specified SDK on remote machine, then start player
        :param i: SDK index
        :return: None
        """
        print "Start SDK for {0}:{1}".format(self.ip, i)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)

        # start SDK
        port = i * SDK_PORT_STEP + SDK_PORT_START
        p2pclient = "ulimit -c unlimited && cd {0}/{1} && nohup ./{2}_{1}".format(REMOTE_SDK_PATH, i, SDK_FILE)
        command = "{0} -p {1} {2} {3} > /dev/null 2>&1 &".format(p2pclient, port, USE_LF_PREFIX, USER_PREFIX)
        print "SDK command is:" + command
        ssh.exec_command(command)
        time.sleep(1)

        # start player
        url = "http://127.0.0.1:{0}/{1}".format(port, self.url)
        command = "nohup python {0}/flv_play.py {1} > /dev/null 2>&1 &".format(REMOTE_PLAYER_PATH, url)
        print "Player command is:", command
        ssh.exec_command(command)

        ssh.close()

    def deploy_sdk(self):
        """
        deploy sdk to remote machine
        :return: None
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)

        # KILL Process
        print_str = "{print $2}"
        kill_cmd = "ps aux | grep {0} |grep -v grep |awk -F ' ' '{1}' | xargs kill -9".format(SDK_FILE, print_str)
        ssh.exec_command(kill_cmd)
        time.sleep(0.5)

        # REMOVE SDKs and player
        ssh.exec_command("rm -rf {0}/".format(REMOTE_SDK_PATH))
        ssh.exec_command("rm -rf {0}".format(REMOTE_SDK_PATH))
        time.sleep(0.5)
        ssh.exec_command("mkdir -p {0}".format(REMOTE_SDK_PATH))
        ssh.close()

        # COPY SDK to remote machine
        deployer = RemoteDeployer(self.ip, self.username, self.password)
        deployer.copy_via_paramiko(self.local_sdk, REMOTE_SDK_FILE)

    def deploy_sdk_copy(self):
        """
        copy sdk for to folders
        :return: None
        """
        print "Deploy SDK copies for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("chmod +x {0}".format(REMOTE_SDK_FILE))
        for i in range(self.sdk_nums):
            port = i * SDK_PORT_STEP + SDK_PORT_START
            print "Deploy SDK for port {0}".format(port)
            ssh.exec_command("mkdir -p {0}/{1}".format(REMOTE_SDK_PATH, i))
            ssh.exec_command("cp {0} {1}/{2}/{3}_{2}".format(REMOTE_SDK_FILE, REMOTE_SDK_PATH, i, SDK_FILE))
            # init dictionary, set sdk to "not started" status
            sdk_start_dict["{0}_{1}".format(self.ip, i)] = False
            time.sleep(0.2)
        ssh.close()

    def deploy_player(self):
        # delete sdk on remote machines
        print "Start deploy player for {0}".format(self.ip)
        deployer = RemoteDeployer(self.ip, self.username, self.password)
        deployer.deploy_folder(parent_path, REMOTE_PLAYER_PATH, "python")


def deploy_sdk_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i])
    node.stop_sdk_all()
    node.deploy_sdk()
    node.deploy_sdk_copy()
    node.deploy_player()


def stop_sdk_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i])
    node.stop_sdk_all()


def dynamic_play(ip_num, increase):
    ip, num = ip_num.split("_")
    num = int(num)
    i = 0
    for address in SDK_IP_LIST:
        if ip == address:
            break
        i += 1

    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i])
    if increase:
        node.start_sdk(num)
    else:
        node.stop_sdk(num)


class Tester(object):
    """
    test helper class
    """

    @staticmethod
    def deploy_sdk_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=deploy_sdk_thread, args=(i,))
            t.start()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def stop_sdk_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=stop_sdk_thread, args=(i,))
            t.start()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def print_help():
        print "Please use control type: [start] or [stop]"


def dynamic_adjust(total, now):
    """
    calculate how many sdk should be start or stop in next step
    :param total: total sdk
    :param now: current started sdk
    :return: start|stop, change, started sdk in next step
    """

    # calc operation
    if now < (total / 10 * 2):
        increase = True
    elif now > (total / 10 * 9):
        increase = False
    else:
        increase = random.choice([True, False])

    # calc num
    rest = total - now
    if increase:
        num = random.choice(range(1, rest))
        now = now + num
    else:
        num = random.choice(range(1, now))
        now = now - num
    print "##############################"
    print "Total SDK {0}, Now {1} SDK is alive ".format(total, now)
    print "Add SDK {0}, Change num is {1}, Then there will be {2}".format(increase, num, now)
    print "##############################"
    return increase, num, now


def adjust_sdk(increase, num):
    """
    start or stop SDKs
    :param increase: True: start, False: stop
    :param num: how many number sdk
    :return: None
    """
    i = 0
    for ip_num, started in sdk_start_dict.items():
        if started != increase:
            dynamic_play(ip_num, increase)
            sdk_start_dict[ip_num] = increase
            i += 1
            if i == num:
                break


###############################
# Main Function
###############################
if __name__ == "__main__":
    tester = Tester()
    if len(sys.argv) != 2:
        tester.print_help()
        exit(0)

    INI_FILE = "host.ini"
    INI_FILE_PATH = "{0}/{1}".format(parent_path, INI_FILE)

    total_sdk = read_ini()
    if sys.argv[1] == "start":
        now_sdk = 0

        # {
        #     "192.168.4.236_0": True,
        #     "192.168.4.236_1": False,
        #     "192.168.4.237_1": False,
        #
        # }
        sdk_start_dict = dict()

        # only deploy once
        tester.deploy_sdk_test()

        # dynamic start and stop play
        while True:
            time1 = time.time()
            # start or stop
            incr, change_num, now_sdk = dynamic_adjust(total_sdk, now_sdk)
            print "##############################"
            print "Add SDK {0}, Change num is {1}, Then alive SDK {2}".format(incr, change_num, now_sdk)
            print "##############################"
            adjust_sdk(incr, change_num)

            time2 = time.time()
            print "Cost {0} seconds".format(time2 - time1)

            # according to online schedule strategy, adjust SDK number every 3 minutes
            time.sleep(60*3)
    elif sys.argv[1] == "stop":
        tester.stop_sdk_test()
