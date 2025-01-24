from django import forms
from events.models import Event,Participant,Category

class StyleMixin():
    form_style_classes = 'border-2 border-gray-600 p-2 rounded-md w-full'

    def formFieldStyle(self):
        for field_key, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.form_style_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.form_style_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f'{self.form_style_classes} resize-none',
                    'placeholder': f'Enter {field.label.lower()}',
                    'row': 4
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': 'border-2 p-2 rounded-md mr-2'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                })
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                })
            else:
                field.widget.attrs.update({
                    'class': self.form_style_classes    
                })


class EventModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'category', 'participant']
        widgets = {
            'date': forms.SelectDateWidget,
            'category': forms.RadioSelect,
            'participant': forms.CheckboxSelectMultiple
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.formFieldStyle()

class ParticipantModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.formFieldStyle()

class CategoryModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.formFieldStyle()