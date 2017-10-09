# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from adminpage.views import AdminLogin, AdminLogout, ActivityList


__author__ = "Epsirom"


urlpatterns = [
    url(r'^login/?$', AdminLogin.as_view()),
    url(r'^logout/?$', AdminLogout.as_view()),
    url(r'^activity/list?$', ActivityList.as_view()),
]
