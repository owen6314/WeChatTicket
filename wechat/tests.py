from django.test import TestCase
from wechat.models import Activity, User, Ticket
from wechat.handlers import GetTicketHandler, ReturnTicketHandler
from wechat.wrapper import WeChatView
from datetime import datetime
from django.utils import timezone


# 抢票单元测试
class GetTicketTest(TestCase):
    fixtures = ['users.json']
    view = WeChatView
    msg = ""

    def setUp(self):
        self.saved_activity = Activity.objects.create(id=2, name='saved', key='saved', place='place',
                                                      description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                      end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                      total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)
        self.published_activity = Activity.objects.create(id=3, name='published', key='published', place='place',
                                                          description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                          end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                          total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)
        self.no_ticket_activity = Activity.objects.create(id=4, name='noticket', key='noticket', place='place',
                                                          description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                          end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                          total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=0)

    def test_not_bind(self):
        user = User.objects.get(open_id=1)
        get_ticket_handler = GetTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = get_ticket_handler.check_status(activity_key)
        self.assertEqual(status, GetTicketHandler.STATUS_NOT_BIND)

    def test_no_activity(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        get_ticket_handler = GetTicketHandler(self.view, self.msg, user)
        activity_key = "saved"
        status = get_ticket_handler.check_status(activity_key)
        self.assertEqual(status, GetTicketHandler.STATUS_NO_ACTIVITY)

    def test_no_ticket(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        get_ticket_handler = GetTicketHandler(self.view, self.msg, user)
        activity_key = "noticket"
        status = get_ticket_handler.check_status(activity_key)
        self.assertEqual(status, GetTicketHandler.STATUS_NO_TICKET)

    def test_has_got(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        activity = Activity.objects.get(id=3)
        Ticket.objects.create(student_id=1, unique_id="test", activity=activity, status=Ticket.STATUS_VALID)
        get_ticket_handler = GetTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = get_ticket_handler.check_status(activity_key)
        self.assertEqual(status, GetTicketHandler.STATUS_HAS_GOT)

    def test_get_ticket_success(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        get_ticket_handler = GetTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = get_ticket_handler.check_status(activity_key)
        self.assertEqual(status, GetTicketHandler.STATUS_VALID)


# 退票单元测试
class ReturnTicketTest(TestCase):
    fixtures = ['users.json']
    view = WeChatView
    msg = ""

    def setUp(self):
        self.published_activity = Activity.objects.create(id=3, name='published', key='published', place='place',
                                                          description='description', start_time=timezone.make_aware(datetime(2017, 12, 18, 20, 0, 0, 0)), pic_url="url",
                                                          end_time=timezone.make_aware(datetime(2017, 12, 18, 21, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.now(),
                                                          total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=900)

    def test_not_bind(self):
        user = User.objects.get(open_id=1)
        return_ticket_handler = ReturnTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = return_ticket_handler.check_status(activity_key)
        self.assertEqual(status, GetTicketHandler.STATUS_NOT_BIND)

    def test_no_activity(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        return_ticket_handler = ReturnTicketHandler(self.view, self.msg, user)
        activity_key = "noactivity"
        status = return_ticket_handler.check_status(activity_key)
        self.assertEqual(status, ReturnTicketHandler.STATUS_NO_ACTIVITY)

    def test_no_ticket(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        return_ticket_handler = ReturnTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = return_ticket_handler.check_status(activity_key)
        self.assertEqual(status, ReturnTicketHandler.STATUS_NO_TICKET)

    def test_no_ticket_cancelled(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        Ticket.objects.create(student_id=1, unique_id="test", activity=self.published_activity, status=Ticket.STATUS_CANCELLED)
        return_ticket_handler = ReturnTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = return_ticket_handler.check_status(activity_key)
        self.assertEqual(status, ReturnTicketHandler.STATUS_NO_TICKET)

    def test_been_used(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        Ticket.objects.create(student_id=1, unique_id="test", activity=self.published_activity, status=Ticket.STATUS_USED)
        return_ticket_handler = ReturnTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = return_ticket_handler.check_status(activity_key)
        self.assertEqual(status, ReturnTicketHandler.STATUS_BEEN_USED)

    def test_return_ticket_success(self):
        user = User.objects.get(open_id=1)
        user.student_id = 1
        user.save()
        Ticket.objects.create(student_id=1, unique_id="test", activity=self.published_activity, status=Ticket.STATUS_VALID)
        return_ticket_handler = ReturnTicketHandler(self.view, self.msg, user)
        activity_key = "published"
        status = return_ticket_handler.check_status(activity_key)
        self.assertEqual(status, ReturnTicketHandler.STATUS_VALID)
