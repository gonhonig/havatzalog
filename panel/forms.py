from django import forms
from .models import Cut, Parameter, Pupil, Event
from django.contrib.auth.models import User


class CutForm(forms.ModelForm):
    class Meta:
        model = Cut
        fields = ['parameter', 'headline', 'status', 'details', 'tags', 'private']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4}),
            'parameter': forms.SelectMultiple()

        }


class CutFormEvent(forms.ModelForm):
    class Meta:
        model = Cut
        fields = ['parameter', 'status', 'details', 'tags', 'private']
        widgets = {
            'parameter': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
            'details': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }


class CutFormSpecific(forms.ModelForm):
    class Meta:
        model = Cut
        fields = ['headline', 'status', 'details', 'tags', 'private']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4})
        }


class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ['name', 'year', 'platoon', 'can_read']
        widgets = {
            'can_read': forms.CheckboxSelectMultiple()
        }


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = ['name', 'category']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in Parameter.objects.values_list('name', flat=True):
            raise forms.ValidationError("הפרמטר כבר קיים")
        return name


class ChangePermissionsForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ['can_read']
        widgets = {
            'can_read': forms.CheckboxSelectMultiple()
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['headline', 'date', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'style': 'display: none'})
        }


class PremAddForm(forms.Form):
    to_add = forms.ModelChoiceField(User.objects.all())

