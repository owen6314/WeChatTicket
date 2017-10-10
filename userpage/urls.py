# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import UserBind, ActivityDetail, Ticket


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
    url(r'^activity/detail?$', ActivityDetail.as_view()),
    url(r'^ticket/detail?$', Ticket.as_view()),
]
