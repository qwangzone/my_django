from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                             address='shenzhen', start_time='2016-08-31 02:18:22')

        Guest.objects.create(id=1, event_id=1, realname='alen',
                             phone='13711001101', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):

    ''' 测试index登录首页 '''

    def test_index_page_renders_index_template(self):
        ''' 测试index视图 '''
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class TestLoginAction(TestCase):
    ''' 测试登录函数'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')

    def test_login_action_username_password_null(self):
        ''' 用户名密码为空'''
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('用户名或密码错误'.encode('utf-8'), response.content)

    def test_login_action_username_password_error(self):
        '''用户名密码错误'''
        test_data = {'username': 'admin12', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('用户名或密码错误'.encode('utf-8'), response.content)

    def tear_login_action_success(self):
        '''登录成功'''
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post("/login_action/", data=test_data)
        print(response.status_code)
        self.assertEqual(response.status_code, 302)

class EventManagerTest(TestCase):
    '''发布会管理'''

    def setUp(self):
        Event.objects.create(id=2, name="xiaomi5", limit=2000, status=True,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')
        self.client.post("/login_action/", {'username': 'admin', 'password': 'admin123456'})

    def test_event_manager_success(self):
        '''测试发布会：xiaomi5'''
        response = self.client.post('/event_manager/')
        #self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)

