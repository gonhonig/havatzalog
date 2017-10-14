from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class UserLoginForm(forms.Form):
    username = forms.CharField(label="שם משתמש")
    password = forms.CharField(widget=forms.PasswordInput, label="סיסמה")

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("המשתמש לא קיים")
            if not user.check_password(password):
                raise forms.ValidationError("סיסמה לא נכונה")
            if not user.is_active:
                raise forms.ValidationError("המשתמש לא פעיל עוד")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email2 = forms.EmailField(label='אימות דוא"ל')
    password2 = forms.CharField(widget=forms.PasswordInput, label="אימות סיסמה")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'password2', 'email', 'email2']
        labels = {
            'first_name': 'שם פרטי',
            'last_name': 'שם משפחה',
            'username': 'שם משתמש',
            'password': 'סיסמה',
            'email': 'אימייל',
        }
        widgets = {'password': forms.PasswordInput()}

    def clean_email2(self):
        email = self.cleaned_data['email']
        email2 = self.cleaned_data['email2']
        if email != email2:
            raise forms.ValidationError("כתובות המייל אינן תואמות")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("כתובת המייל כבר קיימת במאגר")
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("הסיסמאות אינן תואמות")
        return password

