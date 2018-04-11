import HTMLTestRunner
import os, sys, time
dir = os.path.dirname(__file__)
sys.path.append(dir)
import unittest
from db_fixture import test_data
start_dir = dir + "/interface_sec"
print(start_dir)
discover = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='*_test.py')
if __name__ == '__main__':
    test_data.init_data()
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = dir + "/report/" + now + '_result.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='添加发布会接口测试报告', description='Linux')
        runner.run(discover)