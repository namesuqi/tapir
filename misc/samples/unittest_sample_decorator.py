# coding=utf-8
# author: zengyuetian

from misc.samples.calculator import Count
import unittest


class TestCount(unittest.TestCase):
    def setUp(self):
        print("Test Start")

    def tearDown(self):
        print("Test End")

    @unittest.skip("无条件跳过")
    def test_add1(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)

    @unittest.skipIf(1 > 0, "条件为真，跳过")
    def test_add2(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)

    @unittest.skipUnless(1 > 0, "条件为真，执行")
    def test_add3(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)

    # 直接置为失败
    @unittest.expectedFailure
    def test_add4(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)

if __name__ == "__main__":
    unittest.main()