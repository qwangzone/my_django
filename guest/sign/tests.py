from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User
from datetime import datetime
from parameterized import parameterized
import unittest

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
        Event.objects.create(id=3, name="xiaomi6", limit=2000, status=True,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')
        self.client.post("/login_action/", {'username': 'admin', 'password': 'admin123456'})

    def test_event_manager_success(self):
        '''测试发布会：xiaomi5'''
        # post 与get要根据方法中使用的方式来用，若测试的模块中用的是get，那么这得用get传参，反之亦然。
        response = self.client.get('/event_manager/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi6", response.content)

    def test_event_manager_search_success(self):
        '''测试发布会搜索成功:模糊搜索'''
        test_data = {'event_name': 'xiaomi'}
        response = self.client.get('/event_manager/event_name/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'xiaomi6', response.content)

    def test_event_manager_search_success1(self):
        '''测试发布会搜索：搜索条件为空'''
        #test_data = {{'event_name': ''}}
        response = self.client.get('/event_manager/event_name/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'xiaomi6', response.content)

    def test_event_manager_search_success2(self):
        '''测试发布会搜索:精确搜索'''
        test_data = {'event_name': 'xiaomi5'}
        response = self.client.get('/event_manager/event_name/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertNotIn(b'xiaomi6', response.content)

    def test_event_manager_search_fail(self):
        '''测试发布会搜索：查询数据为空'''
        test_data = {'event_name': 'xiaomi51'}
        response = self.client.get('/event_manager/event_name/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'xiaomi5', response.content)
        self.assertNotIn(b'xiaomi6', response.content)

class GuestManagerTest(TestCase):
    '''发布会嘉宾'''
    def setUp(self):
        Event.objects.create(id=2, name="xiaomi5", limit=2000, status=True,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        Guest.objects.create(id=1, realname='lucy', phone='110', email='john@qq.com',
                             sign=False, event_id=2)
        Guest.objects.create(id=2, realname='lili', phone='112', email='lucy@qq.com',
                             sign=True, event_id=2)

        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')
        self.client.post('/login_action/', {'username': 'admin', 'password': 'admin123456'})

    def test_guest_manger_success(self):
        '''测试发布会嘉宾'''
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lucy', response.content)
        self.assertIn(b'lili', response.content)

    def test_guest_manager_search_success(self):
        '''测试发布会嘉宾搜索:模糊搜索'''
        test_data = {'guest_name': 'lucy'}
        response = self.client.get('/guest_manage/guest_name/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lucy', response.content)
        self.assertNotIn(b'lili', response.content)

    def test_guest_manager_search_success1(self):
        '''测试发布会嘉宾搜索：搜索条件为空'''
        #test_data = {{'event_name': ''}}
        response = self.client.get('/guest_manage/guest_name/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lucy', response.content)
        self.assertIn(b'lili', response.content)

    def test_guest_manager_search_success2(self):
        '''测试发布会嘉宾搜索:精确搜索'''
        test_data = {'guest_name': 'lucy'}
        response = self.client.get('/guest_manage/guest_name/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lucy', response.content)
        self.assertNotIn(b'lili', response.content)

    def test_guest_manager_search_fail(self):
        '''测试发布会嘉宾搜索：查询数据为空'''
        test_data = {'guest_name': 'lucy2'}
        response = self.client.get('/guest_manage/guest_name/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'lucy', response.content)
        self.assertNotIn(b'lili', response.content)


class UserSignTest(TestCase):
    '''嘉宾签到测试'''
    def setUp(self):
        Event.objects.create(id=1, name="xiaomi5", limit=2000, status=True,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        Event.objects.create(id=2, name="xiaomi6", limit=2000, status=False,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        Event.objects.create(id=3, name="xiaomi7", limit=2000, status=True,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        Guest.objects.create(id=1, realname='lucy', phone='110', email='john@qq.com',
                             sign=False, event_id=1)
        Guest.objects.create(id=2, realname='lili', phone='112', email='lucy@qq.com',
                             sign=True, event_id=2)
        Guest.objects.create(id=3, realname='lilei', phone='113', email='lucy@qq.com',
                             sign=True, event_id=3)

        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')
        self.client.post('/login_action/', {'username': 'admin', 'password': 'admin123456'})

    # @parameterized.expand([('event_end', '112', '2', 200, b'event is end.'),
    #                        ('phone_error', '158', '1', 200, b'phone error.'),
    #                        ('event_phone_nomatch', '112', '1', 200, b'event id or phone error.'),
    #                        ('user_signed', '110', '1', 200, b'user has sign in.'),
    #                        ('sign_success', '113', '3', 200, b'sign in success!')])
    # def test_guest_sign(self, name, phone, event_id, status_code, result):
    #     '''测试发布会签到'''
    #     test_data = {'phone', phone}
    #     event_id = event_id
    #     response = self.client.post('/sign_index_action/%s/' % event_id, data=test_data)
    #     self.assertEqual(response.status_code, status_code)
    #     self.assertIn(result, response.content)

    def test_guest_sign_fail1(self):
        '''测试发布会签到：发布会已结束'''
        test_data = {'phone': '112'}
        event_id = 2
        response = self.client.post('/sign_index_action/%s/' %event_id, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event is end.', response.content)

    def test_guest_sign_fail2(self):
        '''测试发布会签到：输入不存在的手机号'''
        test_data = {'phone': '158'}
        event_id = 1
        response = self.client.post('/sign_index_action/%s/' %event_id, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error.', response.content)

    def test_guest_sign_fail3(self):
        '''测试发布会签到:输入的手机与发布会不匹配'''
        test_data = {'phone': '112'}
        event_id = 1
        response = self.client.post('/sign_index_action/%s/' % event_id, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event id or phone error.', response.content)

    def test_guest_sign_fail4(self):
        '''测试发布会签到：手机号已签到'''
        test_data = {'phone': '110'}
        event_id = 1
        response = self.client.post('/sign_index_action/%s/' % event_id, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user has sign in.', response.content)

    def test_guest_sign_success(self):
        '''测试发布会签到：签到成功'''
        test_data = {'phone': '113'}
        event_id = 3
        response = self.client.post('/sign_index_action/%s/' % event_id, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success!', response.content)

