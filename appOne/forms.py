from django import forms
from datetime import date
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Ensure this import is added
from .models import *


class EquipmentFilterForm(forms.ModelForm):
    equipment_id = forms.IntegerField(required=False)
    type_of_device = forms.CharField(required=False)
    class Meta:
        model = Equipment
        fields = ['equipment_id', 'type_of_device']


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'audit': DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'audit': {
                'invalid': "Please enter a valid date (YYYY-MM-DD).",
            },
        }

    def clean_audit(self):
        audit = self.cleaned_data.get('audit')
        if audit and audit > date.today():
            raise ValidationError("Audit date cannot be in the future.")
        return audit



#User Registering and login form
class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(help_text='Format: YYYY-MM-DD')
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=17)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'surname', 'date_of_birth', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Set the email for the User model
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                surname=self.cleaned_data['surname'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user
