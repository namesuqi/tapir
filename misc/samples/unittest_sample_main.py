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

    def test_add(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)

# if __name__ == "__main__":
#     # unittest.main() 将一个单元测试模块编程可以直接运行的脚本
#     # unittest.main() 使用TestLoader类来搜寻该模块中以"test"开头的测试方法并自动执行它们
#     unittest.main()


