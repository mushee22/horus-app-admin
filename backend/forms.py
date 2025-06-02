# forms.py
from django import forms
from .models import CustomUser

class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone','password']

