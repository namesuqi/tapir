# coding=utf-8
# author: zengyuetian
# demo how to use python unittest


from misc.samples.calculator import Count
import unittest


class TestCount(unittest.TestCase):
    def setUp(self):
        print("Test Start")

    def tearDown(self):
        print("Test End")

    def test_add1(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)

    def test_add2(self):
        j = Count(3, 3)
        self.assertEqual(j.add(), 5)

# if __name__ == "__main__":
#     # 构造测试套件
#     suite = unittest.TestSuite()
#     suite.addTest(TestCount("test_add1"))
#     suite.addTest(TestCount("test_add2"))
#     # 执行测试套件
#     runner = unittest.TextTestRunner()
#     runner.run(suite)



