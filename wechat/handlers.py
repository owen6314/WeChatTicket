# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import User, Activity, Ticket
from django.utils import timezone
from django.db.models import Q
import datetime
from WeChatTicket import settings
from codex.baseerror import DatabaseError

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
            self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))


# 抢啥：显示一个一周内开始抢票的活动（最近）以及抢票开始时间
class ActivityQueryHandler(WeChatHandler):

    def get_recent_activities(self):
        current_time = timezone.now()
        recent_activities = Activity.objects.filter(Q(book_start__lt=current_time + datetime.timedelta(days=7)) &
                                                    Q(status=Activity.STATUS_PUBLISHED) & Q(book_end__gt=current_time)).order_by('book_start')
        return recent_activities

    def check(self):
        return self.is_text('近期活动', '我要抢票') or self.is_event_click(self.view.event_keys['book_what'])

    def handle(self):
        recent_activities = self.get_recent_activities()
        if not recent_activities:
            return self.reply_text(self.get_message('book_empty'))
        article_list = []
        for activity in recent_activities:
            article = {}
            article['Title'] = activity.name
            article['Description'] = activity.description
            article['Url'] = settings.get_url('u/activity', {'id': activity.id})
            article['PicUrl'] = activity.pic_url
            article_list.append(article)
        return self.reply_news(article_list)


# 查票：查看用户自己获得的票
class TicketQueryHandler(WeChatHandler):

    def get_tickets(self):
        tickets = Ticket.objects.filter(Q(student_id=self.user.student_id) & Q(status=Ticket.STATUS_VALID))
        return tickets

    def check(self):
        return self.is_text('查票') or self.is_event_click(self.view.event_keys['get_ticket'])

    def handle(self):
        if self.user.student_id == "":
            return self.reply_text(self.get_message('not_bind'))
        user_tickets = self.get_tickets()
        if not user_tickets:
            return self.reply_text(self.get_message('user_no_ticket'))
        article_list = []
        for ticket in user_tickets:
            article = {}
            article['Title'] = ticket.activity.name + ":电子票"
            article['Description'] = "点击查看电子票详情"
            ticket_open_id = User.objects.get(student_id=ticket.student_id).open_id
            article['Url'] = settings.get_url('u/ticket', {'openid': ticket_open_id, 'ticket': ticket.unique_id})
            article_list.append(article)
        return self.reply_news(article_list)


# 抢票
class GetTicketHandler(WeChatHandler):

    STATUS_VALID = 0
    STATUS_NO_ACTIVITY = -1
    STATUS_NO_TICKET = -2
    STATUS_NOT_BIND = -3
    STATUS_HAS_GOT = -4

    def check_status(self, activity_key):
        # 未绑定
        if self.user.student_id == "":
            return self.STATUS_NOT_BIND
        # 不存在活动
        try:
            target_activity = Activity.objects.get(Q(key=activity_key) & Q(status=Activity.STATUS_PUBLISHED))
        except:
            return self.STATUS_NO_ACTIVITY
        # 活动票已抢完
        if target_activity.remain_tickets <= 0:
            return self.STATUS_NO_TICKET
        # 用户已经抢过票
        ticket = Ticket.objects.filter(Q(student_id=self.user.student_id) & Q(activity=target_activity))
        if ticket:
            return self.STATUS_HAS_GOT
        return self.STATUS_VALID

    def give_ticket_to_user(self, activity):
        # 注意并发问题
        activity.remain_tickets = activity.remain_tickets - 1
        activity.save()
        # 注意max问题
        ticket_unique_id = self.user.student_id + activity.key
        try:
            Ticket.objects.create(student_id=self.user.student_id, unique_id=ticket_unique_id,
                                  activity=activity, status=Ticket.STATUS_VALID)
        except:
            raise DatabaseError(self.input)

    # 按键
    def check(self):
        return self.is_text_command("抢票")

    def handle(self):
        activity_key = self.get_activity_name_in_command()
        status = self.check_status(activity_key)
        if(status == self.STATUS_NOT_BIND):
            return self.reply_text(self.get_message('not_bind'))
        elif(status == self.STATUS_NO_ACTIVITY):
            return self.reply_text(self.get_message('no_such_activity'))
        elif(status == self.STATUS_NO_TICKET):
            return self.reply_text(self.get_message('ticket_empty'))
        elif(status == self.STATUS_HAS_GOT):
            return self.reply_text(self.get_message("already_got_ticket"))
        else:
            target_activity = Activity.objects.get(key=activity_key)
            self.give_ticket_to_user(target_activity)
            return self.reply_text(self.get_message('get_ticket_success'))


# 退票
class ReturnTicketHandler(WeChatHandler):

    STATUS_VALID = 0
    STATUS_NO_ACTIVITY = -1
    STATUS_NO_TICKET = -2
    STATUS_NOT_BIND = -3
    STATUS_BEEN_USED = -4

    def return_ticket(self, activity, ticket):
        ticket.status = Ticket.STATUS_CANCELLED
        ticket.save()

    def check_status(self, activity_key):
        # 未绑定
        if self.user.student_id == "":
            return self.STATUS_NOT_BIND
        # 无对应活动
        try:
            target_activity = Activity.objects.get(key=activity_key)
        except:
            return self.STATUS_NO_ACTIVITY
        # 没有抢票
        ticket_set = Ticket.objects.filter(Q(student_id=self.user.student_id) & Q(activity=target_activity))
        if not ticket_set:
            return self.STATUS_NO_TICKET
        ticket = ticket_set[0]
        # 抢过票，但是已经退票
        if ticket.status == Ticket.STATUS_CANCELLED:
            return self.STATUS_NO_TICKET
        # 票已经被使用
        if ticket.status == Ticket.STATUS_USED:
            return self.STATUS_BEEN_USED
        return self.STATUS_VALID

    def check(self):
        return self.is_text_command("退票")

    def handle(self):
        activity_key = self.get_activity_name_in_command()
        status = self.check_status(activity_key)
        if status == self.STATUS_NOT_BIND:
            return self.reply_text(self.get_message('not_bind'))
        elif status == self.STATUS_NO_ACTIVITY:
            return self.reply_text(self.get_message('no_such_activity'))
        elif status == self.STATUS_NO_TICKET:
            return self.reply_text(self.get_message("no_ticket_to_return"))
        elif status == self.STATUS_BEEN_USED:
            return self.reply_text(self.get_message("ticket_has_been_used"))
        target_activity = Activity.objects.get(key=activity_key)
        ticket = Ticket.objects.get(Q(student_id=self.user.student_id) & Q(activity=target_activity))
        self.return_ticket(target_activity, ticket)
        return self.reply_text(self.get_message("return_ticket_success"))


class InvalidMathExpressionHandler(WeChatHandler):

    def check(self):
        return self.is_math_expression() and not self.is_valid_math_expression()

    def handle(self):
        return self.reply_text(self.get_message('invalid_math_expression'))


class ValidMathExpressionHandler(WeChatHandler):

    def check(self):
        return self.is_math_expression() and self.is_valid_math_expression()

    def handle(self):
        math_result = self.get_math_expression_value()
        return self.reply_text(self.get_message('math_result', math_result=math_result))
