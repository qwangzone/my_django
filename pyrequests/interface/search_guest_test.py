import os, sys, requests, unittest
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
from parameterized import parameterized
class SearchGuestTest(unittest.TestCase):
    '''嘉宾查询测试'''
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/get_guest_list/'

    @parameterized.expand([('eid_null', '', '', 10021, 'eid cannot be empty'),
                           ('eid_notnull_phone_null_fail', '3', '', 10022, 'result is empty'),
                           ('eid_notnull_phone_null_success', '1', '', 200, 'success'),
                           ('eid_notnull_phone_notnull_fail', '1', '13511001105', 10022, 'result is empty'),
                           ('eid_notnull_phone_null_success', '1', '13511001101', 200, 'success')])
    def test_search_guest(self, name, eid, phone, status, message):
        data = {'eid': eid, 'phone': phone}
        r = requests.request('get', url=self.base_url, params=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], status)
        self.assertIn(message, self.result['message'])
    def tearDown(self):
        print(self.result)

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()