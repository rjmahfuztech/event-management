from django import forms
from events.models import Event

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location']
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.SelectDateWidget,
        }