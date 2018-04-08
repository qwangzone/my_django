import unittest
import requests
import os, sys
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
from parameterized import parameterized

class AddEventTest(unittest.TestCase):
    '''添加发布会'''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event/"

    @parameterized.expand([('all_null', '', '', '', '', '', ''),
                           ('id_exist', 1, '一加 4 发布会', 2000, '深圳宝体', '2018-04-08 17:00:00')])
    def test_add_event_all_null(self, name_test, eid, name, limit, address, start_time):
        payload = {'eid': eid, 'name': name, 'limit': limit, 'address': address, 'start_time': start_time}
        pay = {}
        r = requests.request('post', url=self.base_url, data=payload)
        self.result = r.json()
    # def test_add_event_all_null(self):
    #         '''所有参数为空'''
    #         payload = {"eid":"", "":"", "limit":"","address":"", "start_time":""}
    #         pay={}
    #         r = requests.post(self.base_url, data=pay)
    #         self.result = r.json()
    #         self.assertEqual(self.result['status'], 10021)
    #         self.assertIn('parameter error', self.result['message'])

    def tearDown(self):
        print(self.result)

if __name__ == '__main__':
    # test_data.init_data()
    # suit = unittest.TestSuite()
    # suit.addTest(AddEventTest('test_add_event_all_null'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    unittest.main()
    
         


