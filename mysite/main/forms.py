from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class DateSelectionForm(forms.Form):
    selected_dates = forms.CharField(widget=forms.HiddenInput(), required=False)
    row = forms.CharField(widget=forms.HiddenInput(), required=False)

class ScheduleInitiationForm(forms.Form):
    user_start_date = forms.DateField(label="When should the first group begin selecting?")
    schedule_start_date = forms.DateField(label="When should the schedule begin?")

class CreateGroups(forms.Form):
    selected_row = forms.CharField(widget=forms.HiddenInput())
    selected_column = forms.CharField(widget=forms.HiddenInput())

class EditProfileForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )