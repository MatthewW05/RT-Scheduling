from django.urls import path
from register import views as v
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", v.register, name="register"),
    path('select_dates/', views.select_dates, name='select_dates'),
    path('events_list/', views.events_list, name='events_list'),
    path('schedule_view/', views.schedule_view, name='schedule_view'),
    path('users/', views.users, name='users'),
]