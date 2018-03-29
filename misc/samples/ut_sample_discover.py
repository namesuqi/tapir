# coding=utf-8
# author: zengyuetian

import unittest


if __name__ == "__main__":
    # 定义测试用例的目录为当前目录
    test_dir = "./"

    suite = unittest.defaultTestLoader.discover(test_dir, pattern="unittest*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)


