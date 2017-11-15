from django import forms
from .models import Task
from datetime import datetime


class TaskForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'style': 'width: 100%', 'placeholder': 'משימה חדשה'}))
    area = forms.ChoiceField(
        choices=(
            ('כללי', 'כללי'),
            ('פ.א.', 'פ.א.'),
            ('פ.ע.', 'פ.ע.'),
            ('עוד משהו', 'עוד משהו'),
            ('עוד אחד', 'עוד אחד'),
        )
    )
    deadline = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ללא דד-ליין'}), required=False)

    def clean_deadline(self):
        print("clean")
        data = self.cleaned_data['deadline']
        if not data:
            return None
        else:
            datetime_object = datetime.strptime(data, 'דד-ליין: %d/%m/%y | %H:%M')
            return datetime_object

