from main.models import InitiateSchedule
from datetime import datetime

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