import paramiko
import time


class SSHClient(object):

    def __init__(self, ip, username, password):
        start = time.time()
        # print "SSHConnect to {0}, it should be only call one time!!!".format(ip)
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(ip, 22, username, password)
        end = time.time()
        # print "SSHConnection cost {0} seconds.".format(end - start)

    def __del__(self):
        # print 'SSHConnection close!'
        self._ssh.close()

    def execute_command(self, command):
        remote_terminal_return = self._ssh.exec_command(command)
        # print '------------------------------------------------------'
        # for item in remote_terminal_return[1].readlines():
        #     print item,
        # print '------------------------------------------------------'
        result = ("".join(remote_terminal_return[1].readlines()), "".join(remote_terminal_return[2].readlines()))
        print 'executing cmd: {0}'.format(command)
        return result


# if __name__ == '__main__':
    # ssh = SSHClient('10.6.3.11', 'root', 'Yunshang2014')
    # stdout, stderr = ssh.execute_command('ifconfig')
    # ssh = SSHClient('10.6.3.12', 'root', 'Yunshang2014')
    # stdout, stderr = ssh.execute_command('iptables -')
    # print stdout
    # ssh = SSHClient('192.168.2.44', 'root', 'root')
    # stdout, stderr = ssh.execute_command('ifconfig')
    # print stdout
