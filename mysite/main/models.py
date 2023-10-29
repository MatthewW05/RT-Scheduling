from django.db import models
from django.contrib.auth.models import User

class SelectedDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_date = models.DateField()
    row = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}: {self.selected_date} (Row {self.row})"