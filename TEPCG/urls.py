from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from gamification import views
from gamification.views import *


urlpatterns = patterns('',

	url(r'^$', Home.as_view(), name='home'),

	url(r'^easy/$', Easy.as_view(), name='easy'),

	url(r'^hard/$', Hard.as_view(), name='hard'),

	url(r'^easy/(?P<article>.*)&&sent=(?P<snum>s\d*.\d*)&&vote=true$', TrueE.as_view(), name='truee'),

	url(r'^easy/(?P<article>.*)&&sent=(?P<snum>s\d*.\d*)&&vote=false$', FalseE.as_view(), name='falsee'),

	url(r'^hard/(?P<article>.*)&&sent=(?P<snumen>s\d*.\d*)(?P<snumtr>s\d*.\d*)&&vote=true$', TrueH.as_view(), name='trueh'),

	url(r'^hard/(?P<article>.*)&&sent=(?P<snumen>s\d*.\d*)(?P<snumtr>s\d*.\d*)&&vote=false$', FalseH.as_view(), name='falseh'),

)
