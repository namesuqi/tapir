# coding=utf-8
# author: zengyuetian

import os
from lib.common.tar_file import *

if __name__ == "__main__":
    """
    下载的tar.gz包放在download_dir目录
    将下载下来的tar.gz包，自动解压到特定extract目录
    并且清除源tag.gz包
    并且清除解压出来不需要的shell文件
    """
    import glob

    download_dir = r"D:\zDownload"
    extract_dir = download_dir + r"\extract"
    # delete older extract files
    cmd = r"DEL /Q /S {0}\*".format(extract_dir)
    print cmd

    os.system(cmd)

    gz_files = glob.glob(download_dir + "/*.tar.gz")
    for f in gz_files:
        print f
        untar(f, extract_dir)

    # delete sh and tar
    cmd = r"DEL /Q /S {0}\*.sh".format(extract_dir)
    print cmd
    os.system(cmd)

    # delete older tar.gz files
    cmd = r"DEL /Q /S {0}\*.tar.gz".format(download_dir)
    print cmd
    os.system(cmd)

    # z = ZFile("D:/Personal/Downloads/archive.zip")
    # z.extract_to("E:/")
