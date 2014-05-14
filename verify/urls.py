from django.conf.urls import patterns, include, url

urlpatterns=patterns('',
    url(r'^$','verify.views.message_judgement'),
)
