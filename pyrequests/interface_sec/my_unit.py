import unittest, hashlib
from datetime import datetime
class MyUnit(unittest.TestCase):
    def setUp(self):
        print("start========")

    @property
    def get_client_time(self):
        return datetime.now().timestamp()

    @property
    def get_client_sign(self):
        sign_str = '&Guest-Bugmaster'
        client_time = datetime.now().timestamp()
        md5 = hashlib.md5()
        md5.update((str(client_time) + sign_str).encode('utf8'))
        client_sign = md5.hexdigest()
        return client_sign

