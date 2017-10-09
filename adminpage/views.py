from codex.baseview import APIView
from codex.baseerror import ValidateError, PrivilegeError
from django.contrib import auth
from django.contrib.auth.models import User


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
        self.validate_super_user()


class AdminLogout(APIView):

    def post(self):
        if not self.request.user.is_superuser:
            raise ValidateError(self.input)
        auth.logout(self.request)


class ActivityList(APIView):

    def post(self):
        pass

    def get(self):
        pass