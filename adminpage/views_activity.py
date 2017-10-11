from codex.baseview import APIView
from codex.baseerror import ValidateError, LogicError, PrivilegeError, DatabaseError
from WeChatTicket import settings
from wechat.models import Activity, Ticket
from adminpage.models import Image
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
import time
from dateutil import parser


class ActivityList(APIView):

    def activity_to_dict(self, activity):
        activity_dict = {}
        activity_dict['id'] = activity.id
        activity_dict['name'] = activity.name
        activity_dict['description'] = activity.description
        activity_dict['startTime'] = time.mktime(activity.start_time.timetuple())
        activity_dict['endTime'] = time.mktime(activity.end_time.timetuple())
        activity_dict['place'] = activity.place
        activity_dict['bookStart'] = time.mktime(activity.book_start.timetuple())
        activity_dict['bookEnd'] = time.mktime(activity.book_end.timetuple())
        activity_dict['currentTime'] = int(time.time())
        activity_dict['status'] = activity.status
        return activity_dict

    def get(self):
        activity_set = Activity.objects.exclude(status=-1)
        activity_list = []
        for item in activity_set:
            item_dict = self.activity_to_dict(item)
            activity_list.append(item_dict)
        return activity_list


class ActivityDelete(APIView):

    def post(self):
        self.check_input('id')
        try:
            Activity.objects.get(id=self.input['id']).delete()
        except:
            raise DatabaseError(self.input)


class ActivityCreate(APIView):

    def post(self):
        self.check_input('name', 'key', 'place', 'picUrl', 'startTime', 'endTime', 'bookStart', 'bookEnd', 'totalTickets', 'status')
        print(self.input['startTime'])
        self.input['startTime'] = parser.parse(self.input['startTime'])
        print(self.input['bookStart'])
        Activity.objects.create(name=self.input['name'], key=self.input['key'], place=self.input['place'],
                                description=self.input['description'], start_time=self.input['startTime'], pic_url=self.input['picUrl'],
                                end_time=self.input['endTime'], book_start=self.input['bookStart'], book_end=self.input['bookEnd'],
                                total_tickets=self.input['totalTickets'], status=self.input['status'], remain_tickets=self.input['totalTickets'])


class ImageLoader(APIView):

    def post(self):
        self.check_input('image')
        i = Image(image=self.request.FILES['image'])
        i.save()
        # 发布时这里要改
        image_url = settings.SITE_DOMAIN + "/wechat" + "/media" + "/upload_img/" + str(self.input['image'][0])
        return image_url


class ActivityDetail(APIView):

    def get_used_ticket_num(self, activity):
        ticket_set = Ticket.objects.filter(Q(activity=activity, status=Ticket.STATUS_USED))
        return len(ticket_set)

    def activity_to_dict(self, activity):
        activity_dict = {}
        activity_dict['name'] = activity.name
        activity_dict['key'] = activity.key
        activity_dict['description'] = activity.description
        activity_dict['startTime'] = time.mktime(activity.start_time.timetuple())
        activity_dict['endTime'] = time.mktime(activity.end_time.timetuple())
        activity_dict['place'] = activity.place
        activity_dict['bookStart'] = time.mktime(activity.book_start.timetuple())
        activity_dict['bookEnd'] = time.mktime(activity.book_end.timetuple())
        activity_dict['totalTickets'] = activity.total_tickets
        activity_dict['picUrl'] = activity.pic_url
        activity_dict['bookedTickets'] = activity.total_tickets - activity.remain_tickets
        activity_dict['usedTickets'] = self.get_used_ticket_num(activity)
        activity_dict['currentTime'] = int(time.time())
        activity_dict['status'] = activity.status
        return activity_dict

    def change_activity_detail(self, activity):
        current_time = (int)(time.time())
        # 所有情况下都可以修改
        activity.description = self.input['description']
        activity.pic_url = self.input['picUrl']
        # 已发布活动不可修改
        activity.name = self.input['name']
        activity.place = self.input['place']
        activity.status = self.input['status']
        activity.save()

    # 检查活动修改是否符合逻辑
    def check_change(self, activity):
        pass

    def get(self):
        self.check_input('id')
        choosen_activity = Activity.objects.get(id=self.input['id'])
        choosen_activity_dict = self.activity_to_dict(choosen_activity)
        return choosen_activity_dict

    def post(self):
        self.check_input('id', 'name', 'place', 'picUrl', 'startTime', 'endTime', 'bookStart', 'bookEnd', 'totalTickets', 'status')
        choosen_activity = Activity.objects.get(id=self.input['id'])
        self.check_change(activity)
        self.change_activity_detail(choosen_activity)


class ActivityMenu(APIView):

    def get(self):
        pass

    def post(self):
        pass


class ActivityCheckin(APIView):

    def get(self):
        pass

    def post(self):
        pass
