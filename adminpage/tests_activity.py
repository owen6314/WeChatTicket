from django.test import TestCase
from wechat.models import Activity, Ticket
from codex.baseerror import ValidateError, LogicError, DatabaseError
from adminpage.views_activity import ActivityList, ActivityDelete, ActivityCreate, ActivityDetail, ActivityMenu, ActivityCheckin
from datetime import datetime
from django.utils import timezone


# 单元测试
# 测试Activity相关接口
class ActivityListTest(TestCase):

    def setUp(self):
        Activity.objects.create(id=1, name='deleted', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_DELETED, remain_tickets=1000)
        Activity.objects.create(id=2, name='saved', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)
        Activity.objects.create(id=3, name='published', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)

    def test_activity_list(self):
        activity_list = ActivityList()
        activity_result = activity_list.get()
        self.assertEqual(len(activity_result), 2)
        sorted(activity_result, key=lambda x: x['id'])
        self.assertEqual(activity_result[0]['id'], 2)
        self.assertEqual(activity_result[1]['id'], 3)

    def tearDown(self):
        Activity.objects.get(id=1).delete()
        Activity.objects.get(id=2).delete()
        Activity.objects.get(id=3).delete()


class ActivityCreateTest(TestCase):

    activity_data = {"name": "saved", "key": "key", "place": "place", "description": "description", "picUrl": "pic_url",
                     "startTime": timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), "endTime": timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)),
                     "bookStart": timezone.now(), "bookEnd": timezone.now(), "totalTickets": 1000, "status": Activity.STATUS_PUBLISHED}

    def test_activity_create(self):
        activity_create = ActivityCreate()
        activity_create.input = self.activity_data
        activity_create.post()
        self.assertEqual(Activity.objects.get(name="saved").key, "key")

    def tearDown(self):
        Activity.objects.all().delete()


class ActivityDeleteTest(TestCase):

    def setUp(self):
        Activity.objects.create(id=1, name='deleted', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_DELETED, remain_tickets=1000)
        Activity.objects.create(id=2, name='saved', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)

    def delete_activity_prepare(self, activity_id):
        activity_delete = ActivityDelete()
        activity_delete.input = {}
        activity_delete.input['id'] = activity_id
        return activity_delete

    def test_delete_existing_activity(self):
        activity_delete = self.delete_activity_prepare(2)
        activity_delete.post()
        self.assertEqual(Activity.objects.get(id=2).status, Activity.STATUS_DELETED)

    def test_delete_deleted_activity(self):
        activity_delete = self.delete_activity_prepare(1)
        self.assertRaises(LogicError, activity_delete.post)

    def test_delete_not_existing_activity(self):
        activity_delete = self.delete_activity_prepare(3)
        self.assertRaises(DatabaseError, activity_delete.post)

    def tearDown(self):
        Activity.objects.get(id=1).delete()
        Activity.objects.get(id=2).delete()


# 必做部分：查看活动详情
class ActivityDetailTest(TestCase):

    change_activity_data_valid = {"id": 1, "name": "changed", "place": "place", "description": "description", "picUrl": "pic_url",
                                  "startTime": timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), "endTime": timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)),
                                  "bookStart": timezone.now(), "bookEnd": timezone.now(), "totalTickets": 1000, "status": Activity.STATUS_PUBLISHED}
    change_activity_data_invalid = {"id": 500, "name": "changed", "place": "place", "description": "description", "picUrl": "pic_url",
                                    "startTime": timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), "endTime": timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)),
                                    "bookStart": timezone.now(), "bookEnd": timezone.now(), "totalTickets": 1000, "status": Activity.STATUS_PUBLISHED}

    def setUp(self):
        Activity.objects.create(id=1, name='saved', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)
        Activity.objects.create(id=2, name='published', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)

    def test_get_activity_detail_valid(self):
        activity_detail = ActivityDetail()
        activity_detail.input = {}
        activity_detail.input['id'] = 1
        activity_info_dict = activity_detail.get()
        self.assertEqual(activity_info_dict['name'], "saved")

    def test_get_activity_detail_invalid(self):
        activity_detail = ActivityDetail()
        activity_detail.input = {}
        activity_detail.input['id'] = 3
        self.assertRaises(DatabaseError, activity_detail.get)

    def test_change_activity_detail_valid(self):
        activity_detail = ActivityDetail()
        activity_detail.input = self.change_activity_data_valid
        activity_detail.post()
        self.assertEqual(Activity.objects.get(id=1).name, "changed")

    def test_change_activity_detail_invalid(self):
        activity_detail = ActivityDetail()
        activity_detail.input = self.change_activity_data_invalid
        self.assertRaises(DatabaseError, activity_detail.post)


class ActivityMenuTest(TestCase):

    def setUp(self):
        Activity.objects.create(id=1, name='saved', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)
        Activity.objects.create(id=2, name='published', key='key', place='place',
                                description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)

    def test_get_activity_menu(self):
        activity_menu = ActivityMenu()
        activity_list = activity_menu.get()
        self.assertEqual(len(activity_list), 1)
        sorted(activity_list, key=lambda x: x['id'])
        self.assertEqual(activity_list[0]['name'], 'published')
        self.assertEqual(activity_list[0]['menuIndex'], 0)


class ActivityCheckinTest(TestCase):

    student_id = "target_student"
    other_student_id = "other_student"
    target_activity_id = 1
    other_activity_id = 2
    valid_ticket_id = "valid_ticket"
    invalid_ticket_id = "invalid_ticket"
    other_activity_ticket_id = "other_activity_ticket"

    def setUp(self):
        target_activity = Activity.objects.create(id=self.target_activity_id, name='target', key='key', place='place',
                                                  description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                  end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                  total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)
        other_activity = Activity.objects.create(id=self.other_activity_id, name='other', key='key', place='place',
                                                 description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                 end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                 total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)
        # 有效票
        Ticket.objects.create(student_id=self.student_id, unique_id=self.valid_ticket_id, activity=target_activity, status=Ticket.STATUS_VALID)
        # 无效票(status错误)
        Ticket.objects.create(student_id=self.student_id, unique_id=self.invalid_ticket_id, activity=target_activity, status=Ticket.STATUS_USED)
        # 无效票(对应其他活动)
        Ticket.objects.create(student_id=self.student_id, unique_id=self.other_activity_ticket_id, activity=other_activity, status=Ticket.STATUS_VALID)

    def checkin_ticket_prepare(self, activity_id, ticket_id):
        activity_checkin = ActivityCheckin()
        activity_checkin.input = {}
        activity_checkin.input['actId'] = activity_id
        activity_checkin.input['ticket'] = ticket_id
        return activity_checkin

    def test_checkin_ticket_valid(self):
        activity_checkin = self.checkin_ticket_prepare(self.target_activity_id, self.valid_ticket_id)
        ticket_info_dict = activity_checkin.checkin_ticket()
        self.assertEqual(ticket_info_dict['ticket'], self.valid_ticket_id)
        self.assertEqual(ticket_info_dict['studentId'], self.student_id)

    def test_checkin_ticket_invalid(self):
        activity_checkin = self.checkin_ticket_prepare(self.target_activity_id, self.invalid_ticket_id)
        self.assertRaises(ValidateError, activity_checkin.checkin_ticket)

    def test_checkin_ticket_unrelated(self):
        activity_checkin = self.checkin_ticket_prepare(self.other_activity_id, self.valid_ticket_id)
        self.assertRaises(ValidateError, activity_checkin.checkin_ticket)

    def checkin_student_id_prepare(self, activity_id, student_id):
        activity_checkin = ActivityCheckin()
        activity_checkin.input = {}
        activity_checkin.input['actId'] = activity_id
        activity_checkin.input['studentId'] = student_id
        return activity_checkin

    def test_checkin_student_id_valid(self):
        activity_checkin = self.checkin_student_id_prepare(self.target_activity_id, self.student_id)
        ticket_info_dict = activity_checkin.checkin_student_id()
        self.assertEqual(ticket_info_dict['ticket'], self.valid_ticket_id)
        self.assertEqual(ticket_info_dict['studentId'], self.student_id)

    def test_checkin_student_id_invalid(self):
        activity_checkin = self.checkin_student_id_prepare(self.target_activity_id, self.other_student_id)
        self.assertRaises(ValidateError, activity_checkin.checkin_student_id)
