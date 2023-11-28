from django.urls import path
from register import views as v
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('select_dates/', views.select_dates, name='select_dates'),
    path('select_dates/<str:check_error>', views.select_dates, name='select_dates'),
    path('schedule_view/', views.schedule_view, name='schedule_view'),
    path('schedule_view/<str:start>', views.schedule_view, name='schedule_view'),

    path('admin_select_dates/<str:user_n>', views.admin_select_dates, name='admin_select_dates'),
    path('create_groups/', views.create_groups, name='create_groups'),
    path('initialize_schedule/', views.initialize_schedule, name='initialize_schedule'),
    path('master/', views.master, name="master"),
    path('master/<str:start>', views.master, name="master"),

    path('change_password/', views.change_password, name='change_password'),
    path('password_change_success/', views.password_change_success, name='password_change_success'),

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_done.html'), name='password_reset_complete'),

    #path("register/", v.register, name="register"),
    #path('events_list/', views.events_list, name='events_list'),
    #path('users/', views.users, name='users'),
]