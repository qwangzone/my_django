import unittest, os , sys, requests
from parameterized import parameterized
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)
from db_fixture import test_data
class AddGuestTest(unittest.TestCase):
    '''添加嘉宾测试'''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_guest/"
    @parameterized.expand([('all_null', '', '', '', '', 10021, 'parameter error'),
                           ('event_noexist', '10', 'meizhan', '18291', 'miezhan@mail.com', 10022, 'event id null'),
                           ('event_end', '3', 'meizhan', '18291', 'miezhan@mail.com', 10023, 'not available'),
                           ('event_full', '2', 'meizhan', '18291', 'miezhan@mail.com', 10024, 'event limit'),
                           ('event_started', '4', 'meizhan', '18291', 'miezhan@mail.com', 10025, 'event has started'),
                           ('phone number repeat', '5', 'meizhan', '13511001102', 'miezhan@mail.com', 10026, 'phone number repeat'),
                           ('success', '5', 'meizhan', '1586352', 'miezhan@mail.com', 200, 'success')])
    def test_add_guest(self, name, eid, realname, phone, email, status, message):
        data = {'eid': eid, 'realname': realname, 'phone': phone, 'email': email}
        r = requests.request('post', url=self.base_url, data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], status)
        self.assertIn(message, self.result['message'])
    def tearDown(self):
        print(self.result)

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()