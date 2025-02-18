from django import forms
from events.models import Event,Category

class StyleMixin():
    form_style_classes = 'border border-gray-500 p-2 rounded-md w-full mb-2'

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
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': f'{self.form_style_classes} mb-2 mt-1',
                    'placeholder': f'Enter password'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f'{self.form_style_classes} resize-none',
                    'placeholder': f'Enter {field.label.lower()}',
                    'row': 3
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': 'border p-1 sm:p-2 rounded-md mr-1 sm:mr-2'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.formFieldStyle()


class EventModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'image']
        widgets = {
            'date': forms.SelectDateWidget,
            'category': forms.RadioSelect,
            'time': forms.TimeInput(attrs={
                    'value': "13:00",
                    'step': "900",
                    'type': 'time'
                })
        }


class CategoryModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
