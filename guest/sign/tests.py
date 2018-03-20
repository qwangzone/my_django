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
        Event.objects.create(id=3, name="xiaomi6", limit=2000, status=True,
                             address="beijing", start_time=datetime(2016, 8, 10, 14, 0, 0))
        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')
        self.client.post("/login_action/", {'username': 'admin', 'password': 'admin123456'})

    def test_event_manager_success(self):
        '''测试发布会：xiaomi5'''
        response = self.client.get('/event_manager/') #post 与get都可以，重要的是先登录
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
        response = self.client.get('/guest_manage/')
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
        Guest.objects.create(id=1, realname='lucy', phone='110', email='john@qq.com',
                             sign=False, event_id=1)
        Guest.objects.create(id=2, realname='lili', phone='112', email='lucy@qq.com',
                             sign=True, event_id=2)

        User.objects.create_user('admin', 'admin@qq.com', 'admin123456')
        self.client.post('/login_action/', {'username': 'admin', 'password': 'admin123456'})

    def test_guest_sign_fail1(self):
        '''测试发布会签到：发布会已结束'''
        test_data = {'phone': '112'}
        event_id = 2
        response = self.client.get('/sign_index_action/%s/' % event_id, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event is end.', response.content)