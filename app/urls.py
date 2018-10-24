from django.urls import path

from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # App main page
    path('', views.index, name='index'),

    # User accounts pages
    # path(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # path(r'^logout/$', auth_views.logout, {'template_name': 'login.html'}, name='logout'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]