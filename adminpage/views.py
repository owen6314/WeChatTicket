from codex.baseview import APIView
from codex.baseerror import ValidateError, PrivilegeError, DatabaseError
from WeChatTicket import settings
from wechat.models import Activity, Ticket
from adminpage.models import Image
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import time


class AdminLogin(APIView):

    def validate_super_user(self):
        username = self.input['username']
        password = self.input['password']
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise ValidateError(self.input)
        if not user.is_superuser:
            raise PrivilegeError(self.input)
        auth.login(self.request, user)

    def get(self):
        if not self.request.user.is_superuser:
            raise ValidateError(self.input)

    def post(self):
        self.check_input('username', 'password')
        self.validate_super_user()


class AdminLogout(APIView):

    def post(self):
        if not self.request.user.is_superuser:
            raise ValidateError(self.input)
        auth.logout(self.request)


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

    def get(self):
        self.check_input('id')
        choosen_activity = Activity.objects.get(id=self.input['id'])
        choosen_activity_dict = self.activity_to_dict(choosen_activity)
        return choosen_activity_dict

    def post(self):
        pass


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
