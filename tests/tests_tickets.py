# 功能测试：抢票和退票
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class GetTicketFuncTest(StaticLiveServerTestCase):
	