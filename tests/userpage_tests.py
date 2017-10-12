
# userpage 功能测试

class UserPageTest(StaticLiveServerTestCase):
	browser = None

	@classmethod
	def setUpClass(self):
		super(UserPageTest, self).setUpClass()


	@classmethod
	def tearDownClass(self):
		cls.browser.quit()
		super(UserPageTest, self).tearDownClass()