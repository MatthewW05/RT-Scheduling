from main.models import InitiateSchedule, Admin
from datetime import datetime
from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.models import User

def get_schedules():
    schedules = []

    for o in InitiateSchedule.objects.values_list('schedule_start_date', flat=True):
            schedules.append(str(o))

    schedules.reverse()
    
    return schedules

def get_first_schedule_date():
    schedules = []

    for o in InitiateSchedule.objects.values_list('schedule_start_date', flat=True):
            schedules.append(str(o))

    schedules.reverse()
    first = datetime.strptime(schedules[0], "%Y-%m-%d").date()

    return first

def get_first_schedule():
    schedules = []

    for o in InitiateSchedule.objects.values_list('schedule_start_date', flat=True):
            schedules.append(str(o))

    schedules.reverse()
    if len(schedules) != 0:
        first = schedules[0]

        return first
    else:
          return None

def empty_name(name1, name2):
      if not name1 or not name2:
            return True
      else:
            return False
    
def rewrite_super(user):
      if Admin.objects.filter(user=user)[0].admin:
            user.is_superuser = True
            user.is_staff = True
            user.is_admin = True

            user.save()