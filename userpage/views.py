from codex.baseerror import ValidateError, LogicError
from codex.baseview import APIView
import time
from wechat.models import User, Activity, Ticket
import requests


class UserBind(APIView):

    def validate_user(self):
        test_url = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp"
        user_data = {
            'userid': self.input['student_id'],
            'userpass': self.input['password']
        }
        r = requests.post(test_url, user_data)
        if 'window.alert' in r.text:
            raise ValidateError(self.input)

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()


class ActivityDetail(APIView):

    def activity_to_dict(self, activity):
        activity_dict = {}
        activity_dict['name'] = activity.name
        activity_dict['key'] = activity.key
        activity_dict['description'] = activity.description
        activity_dict['startTime'] = activity.start_time.timestamp()
        activity_dict['endTime'] = activity.end_time.timestamp()
        activity_dict['place'] = activity.place
        activity_dict['bookStart'] = activity.book_start.timestamp()
        activity_dict['bookEnd'] = activity.book_end.timestamp()
        activity_dict['totalTickets'] = activity.total_tickets
        activity_dict['picUrl'] = activity.pic_url
        activity_dict['remainTickets'] = activity.remain_tickets
        activity_dict['currentTime'] = int(time.time())
        return activity_dict

    def get(self):
        self.check_input('id')
        activity = Activity.objects.get(id=self.input['id'])
        if activity.status == Activity.STATUS_PUBLISHED:
            return self.activity_to_dict(activity)
        else:
            raise LogicError(self.input)


class TicketDetail(APIView):

    def ticket_to_dict(self, ticket):
        ticket_dict = {}
        ticket_dict['activityName'] = ticket.activity.name
        ticket_dict['place'] = ticket.activity.place
        ticket_dict['activityKey'] = ticket.activity.key
        ticket_dict['uniqueId'] = ticket.unique_id
        ticket_dict['startTime'] = ticket.activity.start_time.timestamp()
        ticket_dict['endTime'] = ticket.activity.end_time.timestamp()
        ticket_dict['currentTime'] = int(time.time())
        ticket_dict['status'] = ticket.status
        return ticket_dict

    def get(self):
        print(self.input)
        self.check_input('openid', 'ticket')
        ticket = Ticket.objects.get(unique_id=self.input['ticket'])
        return self.ticket_to_dict(ticket)
