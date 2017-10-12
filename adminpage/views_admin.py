from codex.baseview import APIView
from codex.baseerror import ValidateError, DatabaseError
from django.contrib import auth


class AdminLogin(APIView):

    def validate_user(self):
        username = self.input['username']
        password = self.input['password']
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise ValidateError(self.input)
        try:
            auth.login(self.request, user)
        except:
            raise DatabaseError(self.input)

    def get(self):
        if not self.request.user:
            raise ValidateError(self.input)

    def post(self):
        self.check_input('username', 'password')
        self.validate_user()


class AdminLogout(APIView):

    def post(self):
        if not self.request.user:
            raise ValidateError(self.input)
        try:
            auth.logout(self.request)
        except:
            raise DatabaseError(self.input)
