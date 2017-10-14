from django import forms
from panel.models import Cut


class SearchForm(forms.Form):
    query = forms.TextInput()
    fields = forms.CheckboxSelectMultiple(choices=('תגיות', 'פרמטרים', 'חניכים', 'תוכן'))

