from django.test import TestCase, Client
from django.contrib.auth.models import User
from .views_admin import AdminLogin, AdminLogout
from codex.baseerror import ValidateError, PrivilegeError


# 测试管理员登录、非管理员登录和密码输入错误的情况(抛出异常检测有问题)
class AdminLoginTest(TestCase):

    def setUp(self):
        User.objects.create_superuser('admin', 'a@test.com', '12345678a')
        User.objects.create_user('ordinaryUser', 'test@test.com', '12345678b')

    # 路由测试
    def test_login_url(self):
        c = Client()
        response = c.post('/api/a/login', {"username": "admin", "password": "12345678a"})
        self.assertEqual(response.status_code, 200)

    # 管理员登录(未完成)
    def test_login_superuser(self):
        c = Client()
        response = c.post('/api/a/login', {"username": "admin", "password": "12345678a"})
        print(response.content)

    # 非管理员登录
    def test_login_ordinaryuser(self):
        admin_login = AdminLogin()
        admin_login.input = {}
        admin_login.input['username'] = 'ordinaryUser'
        admin_login.input['password'] = '12345678b'
        self.assertRaises(PrivilegeError, admin_login.post)

    # 管理员登录，密码错误
    def test_login_superuser_wrong_password(self):
        admin_login = AdminLogin()
        admin_login.input = {}
        admin_login.input['username'] = 'admin'
        admin_login.input['password'] = '12345678b'
        self.assertRaises(ValidateError, admin_login.post)


class AdminLogoutTest(TestCase):

    def setUp(self):
        User.objects.create_superuser('admin', 'a@test.com', '12345678a')
        User.objects.create_user('ordinaryUser', 'test@test.com', '12345678b')

    # 路由测试
    def test_logout_url(self):
        c = Client()
        response = c.post('/api/a/logout')
        self.assertEqual(response.status_code, 200)

    # 管理员登出

    # 非管理员登出
