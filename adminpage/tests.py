from django.test import TestCase, Client
from django.contrib.auth.models import User
from codex.baseerror import ValidateError, PrivilegeError


# 测试管理员登录、非管理员登录和密码输入错误的情况(抛出异常检测有问题)
class AdminLoginTest(TestCase):

    def setUp(self):
        super_user = User.objects.create_superuser('admin', 'a@test.com', '12345678a')
        user = User.objects.create_user('ordinaryUser', 'test@test.com', '12345678b')

    # 管理员登录
    def test_login_superuser(self):
        c = Client()
        response = c.post('/api/a/login', {"username": "admin", "password": "12345678a"})
        self.assertEqual(response.status_code, 200)

    # 非管理员登录
    def test_login_ordinaryuser(self):
        c = Client()
        response = c.post('/api/a/login', {"username": "ordinaryUser", "password": "12345678b"})
        self.assertEqual(response.status_code, 200)
        # self.assertRaises(PrivilegeError)

    # 管理员登录，密码错误
    def test_login_superuser_wrong_password(self):
        c = Client()
        response = c.post('/api/a/login', {"username": "admin", "password": "12345678c"})
        self.assertEqual(response.status_code, 200)
        # self.assertRaises(PrivilegeError)