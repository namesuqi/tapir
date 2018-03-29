# coding=utf-8
import os

import paramiko
import time


class SFTPClient(object):

    def __init__(self, ip, username, password):
        # start = time.time()
        # print "SFTPConnect to {0}, it should be only call one time!!!".format(ip)
        self._transport = paramiko.Transport(ip, 22)
        self._transport.connect(None, username, password)
        self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        # end = time.time()
        # print "SFTPConnection cost {0} seconds.".format(end - start)

    def __del__(self):
        # print 'SFTPConnection close!'
        self._transport.close()

    def upload(self, remote_path, local_path):
        self._sftp.put(local_path, remote_path)
        # print '---------------------'
        # print '|  Upload Success!  |'
        # print '---------------------'

    def download(self, remote_path, local_path):
        self._sftp.get(remote_path, local_path)
        # print '---------------------'
        # print '| Download Success! |'
        # print '---------------------'

    def upload_dir(self, remote_dir_path, local_dir_path):
        """
            将某文件夹下的所有文件copy到一个远程目录下
        :param remote_dir_path:
        :param local_dir_path:
        :return:
        """
        for i, [root_path, dirs, files] in enumerate(os.walk(local_dir_path)):
            if i == 0:
                if files and dirs:
                    for dir_name in dirs:
                        self._sftp.mkdir(remote_dir_path + "/" + dir_name)
                    for file_name in files:
                        self._sftp.put(root_path + os.sep + file_name, remote_dir_path + "/" + file_name)
                if files and not dirs:
                    for file_name in files:
                        self._sftp.put(root_path + os.sep + file_name, remote_dir_path + "/" + file_name)
            else:
                long_dir_name = root_path.partition(local_dir_path)[-1].replace('\\', '/')
                if files and dirs:
                    for dir_name in dirs:
                        self._sftp.mkdir(remote_dir_path + "/" + long_dir_name + "/" + dir_name)
                    for file_name in files:
                        self._sftp.put(root_path + os.sep + file_name, remote_dir_path + "/" + long_dir_name +
                                       "/" + file_name)
                elif files and not dirs:
                    for file_name in files:
                        self._sftp.put(root_path + os.sep + file_name, remote_dir_path + "/" + long_dir_name + "/"
                                       + file_name)


if __name__ == '__main__':
    # sftp = SFTPClient('10.5.100.46', 'root', 'Yunshang2014')
    # sftp.upload('/root/Testdata/123.test', 'd://test.txt')
    # sftp.download('/root/Testdata/123.test', 'd://test123.txt')
    # sftp = SFTPClient('10.6.3.28', 'root', 'Yunshang2014')
    # sftp.upload_dir("/root/sdk_test", os.path.abspath(os.path.dirname(__file__)) + '/../../../misc/bin/sdk/daily_routine/')
    pass
