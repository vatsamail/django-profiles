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

app_name = 'ui'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', login, {'template_name': 'ui/login.html'}, name='login'),
    path('logout/', logout, {'template_name': 'ui/logout.html'}, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile-edit'),
    path('change_password', views.change_password, name='change-password'),

    path('reset_password', password_reset, {
                                            'template_name': 'ui/reset_password.html',
                                            'post_reset_redirect': 'ui:password_reset_done',
                                            'email_template_name': 'ui/reset_password_email.html',
                                            }, name='reset-password'),

    path('reset_password/done', password_reset_done, {'template_name': 'ui/reset_password_done.html'}, name='password_reset_done'),

    re_path(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
                                                                                {'post_reset_redirect': 'ui:password_reset_complete',
                                                                                 'template_name' : 'ui/reset_password_confirm.html',
                                                                                }, name='password_reset_confirm'),
    path('reset_password/complete', password_reset_complete, {'template_name': 'ui/reset_password_complete.html'}, name='password_reset_complete'),
]

"""
Tutorial and useful links
"""
'''
1. https://wsvincent.com/django-user-authentication-tutorial-password-reset/
2. https://stackoverflow.com/questions/5802189/django-errno-111-connection-refused/5802348#5802348
'''
