import unittest
import requests
import os, sys
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
from parameterized import parameterized

class AddEventTest(unittest.TestCase):
    '''添加发布会测试'''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event/"

    @parameterized.expand([('all_null', '', '', '', '', '', 10021, 'parameter error'),
                           ('id_exist', 1, '一加4发布会', 2000, '深圳宝体', '2018-04-08 17:00:00', 10022, 'event id already exists'),
                           ('name_exist', 11, '红米Pro发布会', 2000, '北京水立方', '2017', 10023, 'event name already exists'),
                           #('data_wrong', 11, '一加4手机发布会', 2000, '北京水立方', '20170508', 10024, 'start_time format error'),
                           ('success', 11, '一加4手机发布会', 2000, '北京水立方', '2018-04-09 11:00:00', 200, 'add event success')])
    def test_add_event(self, name_test, eid, name, limit, address, start_time, status, message):
        payload = {'eid': eid, 'name': name, 'limit': limit, 'address': address, 'start_time': start_time}
        r = requests.request('post', url=self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], status)
        self.assertIn(self.result['message'], message)
    def tearDown(self):
        print(self.result)

if __name__ == '__main__':
    test_data.init_data()
    # suit = unittest.TestSuite()
    # suit.addTest(AddEventTest('test_add_event_all_null'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    unittest.main()
    
         


