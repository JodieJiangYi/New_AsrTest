from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_asr),
    # url(r'^iflytek_asr/$', views.iflytek_asr_intro),
]

