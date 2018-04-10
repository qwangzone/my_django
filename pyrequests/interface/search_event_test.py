import os, sys, requests, unittest
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
from parameterized import parameterized
class SearchEventTest(unittest.TestCase):
    '''发布会查询测试'''
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/get_event_list/'

    @parameterized.expand([('all_null', '', '', 10021, 'parameter error'),
                           ('eid_search_fail', '21', '红米Pro发布会', 10022, 'query result is empty'),
                           ('eid_search_success', '1', '红米Pro发布会', 200, 'success'),
                           ('name_search_fail', '', '红米Pro发布1会', 10022, 'query result is empty'),
                           ('name_search_success', '', '红米Pro发布会', 200, 'success')])
    def test_search_event(self, name_test, eid, name, status, message):
        data = {'eid': eid, 'name': name}
        r = requests.request('get', url=self.base_url, params=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], status)
        self.assertIn(message, self.result['message'])

    def tearDown(self):
        print(self.result)

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()