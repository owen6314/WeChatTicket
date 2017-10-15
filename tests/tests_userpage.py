# userpage 功能测试：绑定
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class UserPageTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None
    username = '2015013226'
    password = '123456'

    @classmethod
    def setUpClass(self):
        super(UserPageTest, self).setUpClass()
        self.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        super(UserPageTest, self).tearDownClass()

    def test_bind_user(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/bind?openid=1'))

        name_box = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'inputUsername'))
        )
        name_box.send_keys(self.username)

        password_box = self.browser.find_element_by_id('inputPassword')
        password_box.send_keys(self.password)

        submit_button = self.browser.find_element_by_css_selector('#validationHolder button')
        submit_button.click()

        self.assertIn("认证成功", self.browser.find_element_by_id('mainbody').text)
