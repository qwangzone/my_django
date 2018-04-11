import unittest
import requests
import os, sys, hashlib
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
from datetime import datetime
from parameterized import parameterized

class AddEventTest(unittest.TestCase):
    '''添加发布会测试'''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event_sec/"
        # self.client_time = datetime.now().timestamp()
        # sign_str = '&Guest-Bugmaster'
        # md5 = hashlib.md5()
        # md5.update((str(self.client_time) + sign_str).encode('utf8'))
        # self.client_sign = md5.hexdigest()
    @property
    def get_client_time(self):
        client_time = datetime.now().timestamp()
        return client_time

    @property
    def get_client_sign(self):
        sign_str = '&Guest-Bugmaster'
        md5 = hashlib.md5()
        md5.update((str(self.client_time) + sign_str).encode('utf8'))
        return md5.hexdigest()
    # @parameterized.expand([('all_null', '', '', '', '', '', 10021, 'parameter error'),
    #                        ('id_exist', 1, '一加4发布会', 2000, '深圳宝体', '2018-04-08 17:00:00', 10022, 'event id already exists'),
    #                        ('name_exist', 11, '红米Pro发布会', 2000, '北京水立方', '2017', 10023, 'event name already exists'),
    #                        ('data_wrong', 11, '一加4手机发布会', 2000, '北京水立方', '20170508', 10024, 'start_time format error'),
    #                        ('success', 11, '一加4手机发布会', 2000, '北京水立方', '2018-04-09 11:00:00', 200, 'add event success')])
    # #测试接口功能
    # def test_add_event(self, name_test, eid, name, limit, address, start_time, status, message):
    #     payload = {'time': self.get_client_time, 'sign': self.client_sign,
    #                'eid': eid, 'name': name, 'limit': limit, 'address': address, 'start_time': start_time}
    #     auth_data = ('admin', 'admin123456')
    #     r = requests.request('post', url=self.base_url, data=payload, auth=auth_data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], status)
    #     self.assertIn(self.result['message'], message)

    def tearDown(self):
        print(self.result)

    @parameterized.expand([('sign_null', 20011, 'sign null', '', '', ),
                           ('timeout', 20012, 'time is', '0', 'client_sign', ),
                           ('sign_error', 20013, 'sign error', '', 'client_sign',)])
    #测试接口签名加密
    def test_add_event_sec(self, name, status, message, client_time=get_client_time, client_sign=get_client_sign):
        time_1 = datetime.now().timestamp()
        payload = {'time': client_time, 'sign': client_sign}
        r = requests.request('post', url=self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], status)
        self.assertIn(message, self.result['message'])





if __name__ == '__main__':
    test_data.init_data()
    # suit = unittest.TestSuite()
    # suit.addTest(AddEventTest('test_add_event_sec'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    unittest.main()


    
         


