from django import forms

class DateSelectionForm(forms.Form):
    selected_dates = forms.CharField(widget=forms.HiddenInput())
    row = forms.CharField(widget=forms.HiddenInput())