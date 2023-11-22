from django.contrib import admin
from .models import SelectedDate, InitiateSchedule, SelectionGroups
# Register your models here.
admin.site.register(SelectedDate)
admin.site.register(InitiateSchedule)
admin.site.register(SelectionGroups)