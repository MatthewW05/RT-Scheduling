from django.urls import path
from register import views as v
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include, path
from django.contrib import admin
from functools import wraps
from django.shortcuts import redirect
from okta_oauth2.decorators import okta_login_required



def okta_admin_required(view_func):
    @wraps(view_func)
    @okta_login_required  # Apply Okta's login required decorator first
    def wrapped_view(request, *args, **kwargs):
        # Check additional conditions, if any
        if not request.user.is_superuser:
            # Redirect non-superusers to a different URL
            return redirect('/accounts/login/')  # Adjust the login URL as needed
        # Proceed with the view function for authenticated users
        return view_func(request, *args, **kwargs)
    return wrapped_view



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

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    
    #path('reset_password/', auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name='reset_password'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_sent.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_form.html'), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_done.html'), name='password_reset_complete'),
    

    #path('admin/', okta_admin_required(admin.site.urls)),
    #path('change_password/', views.change_password, name='change_password'),
    #path('password_change_success/', views.password_change_success, name='password_change_success'),
    #path("register/", v.register, name="register"),
    #path('events_list/', views.events_list, name='events_list'),
    #path('users/', views.users, name='users'),
]