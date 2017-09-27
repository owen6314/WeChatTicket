from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import User

import requests

class UserBind(APIView):

    def validate_user(self):
        test_url = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp"
        user_data = {
            'userid':self.input['student_id'],
            'userpass':self.input['password']
        }
        r = requests.post(test_url, user_data)
        if 'window.alert' in r.text:
            raise ValidateError(self.input)
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        #raise NotImplementedError('You should implement UserBind.validate_user method')

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()
