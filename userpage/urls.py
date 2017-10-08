# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import UserBind


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
]
