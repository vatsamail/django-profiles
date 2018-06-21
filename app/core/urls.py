from django.urls import include, path, re_path
from . import views
from django.contrib.auth.views import (
        login,
        logout,
        password_reset,
        password_reset_done,
        password_reset_confirm,
        password_reset_complete,
    )

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    re_path(r'friending/(?P<operation>.+)/(?P<pk>\d+)/$', views.friending, name='friend_unfriend'),
]
