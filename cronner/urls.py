from django.conf.urls import include, url
from . import views

urlpatterns = [
    url('toggle', views.toggle, name='toggle'),
    url('add_cron', views.add_cron, name='add_cron'),
    url('disable_cron', views.disable_cron, name='disable_cron'),
    url('enable_cron', views.enable_cron, name='enable_cron'),
    url('delete_cron', views.delete_cron, name='delete_cron'),
    url('', views.index, name='index'),
]