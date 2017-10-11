from django.test import TestCase, Client
from wechat.models import Activity
from .views_activity import ActivityList, ActivityDelete, ActivityCreate, ImageLoader, ActivityDetail, ActivityMenu, ActivityCheckin
from datetime import datetime
from django.utils import timezone


class ActivityListTest(TestCase):

    def setUp(self):
        Activity.objects.create(id=1, name='deleted', key='key', place='place',
                                description='description', start_time=timezone(2017, 12, 18, 20, 0, 0, 0), pic_url="url",
                                end_time=timezone(2017, 12, 18, 21, 0, 0, 0), book_start=datetime.now(), book_end=datetime.now(),
                                total_tickets=1000, status=Activity.STATUS_DELETED, remain_tickets=1000)

    def test_get(self):
        pass
