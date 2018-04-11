import os, sys, requests, unittest
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
from parameterized import parameterized
class UserSignTest(unittest.TestCase):
    '''嘉宾签到测试'''
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/user_sign/'

    @parameterized.expand([('eid_null', '', '13511001101', 10021, 'parameter error'),
                           ('phone_null', '1', '', 10021, 'parameter error'),
                           ('eid_not_exist', '6', '13511001101', 10022, 'event id is null'),
                           ('event_closed', '3', '13511001101', 10023, 'event status is not available'),
                           ('event_started', '1', '13511001101', 10024, 'event has started'),
                           ('phone_not_exist', '5', '13511001109', 10025, 'user phone null'),
                           ('event_phone_not_match', '5', '13511001100', 10026, 'user did not participate'),
                           ('user_signed', '5', '13511001103', 10027, 'user has sign in'),
                           ('sucess', '5', '13511001102', 200, 'success')])
    def test_user_sign(self, name, eid, phone, status, message):
        data = {'eid': eid, 'phone': phone}
        r = requests.request('post', url=self.base_url, data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], status)
        self.assertIn(message, self.result['message'])

    def tearDown(self):
        print(self.result)

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()