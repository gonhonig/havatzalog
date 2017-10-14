from django import forms
from .models import Cut, Parameter, Pupil
from django.contrib.auth.models import User


class CutForm(forms.ModelForm):
    class Meta:
        model = Cut
        fields = ['parameter', 'headline', 'status', 'trend', 'details', 'tags']
        widgets = {
            'parameter': forms.SelectMultiple()
        }


class CutFormSpecific(forms.ModelForm):
    class Meta:
        model = Cut
        fields = ['headline', 'status', 'trend', 'details', 'tags']


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


class PremAddForm(forms.Form):
    to_add = forms.ModelChoiceField(User.objects.all())

