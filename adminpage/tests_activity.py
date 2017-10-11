from django.test import TestCase, Client
from wechat.models import Activity
from .views_activity import ActivityList, ActivityDelete, ActivityCreate, ImageLoader, ActivityDetail, ActivityMenu, ActivityCheckin
from datetime import datetime
from django.utils import timezone


class ActivityListTest(TestCase):

    def setUp(self):
        deleted_activity = Activity.objects.create(id=1, name='deleted', key='key', place='place',
                                                   description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                   end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                   total_tickets=1000, status=Activity.STATUS_DELETED, remain_tickets=1000)
        saved_activity = Activity.objects.create(id=2, name='saved', key='key', place='place',
                                                 description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                 end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                 total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)
        published_activity = Activity.objects.create(id=3, name='published', key='key', place='place',
                                                     description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                     end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                     total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)

