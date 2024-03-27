from django.db import models
from django.contrib.auth.models import User

class SelectedDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    selected_date = models.DateField(blank=True)
    row = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.user}: {self.selected_date} (Row {self.row})"

class InitiateSchedule(models.Model):
    user_start_date = models.DateField()
    schedule_start_date = models.DateField()

    def __str__(self):
        return f"users will begin selecting on {self.user_start_date} for {self.schedule_start_date}"

class SelectionGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.IntegerField()

    def __str__(self):
        return f"{self.user}: group {self.group}"

class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}"