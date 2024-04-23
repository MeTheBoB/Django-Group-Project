from django import forms
from datetime import date
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Ensure this import is added
from .models import *


# To filter the equipment
# created by Saad
class EquipmentFilterForm(forms.ModelForm):
    equipment_id = forms.IntegerField(required=False)
    type_of_device = forms.CharField(required=False)
    class Meta:
        model = Equipment
        fields = ['equipment_id', 'type_of_device']


# To add equipment
# created by Saad
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
# Created Saad
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
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.phone_number = self.cleaned_data['phone_number']


        if commit:
            user.save()
            Person.objects.create(
            user=user,
            name=user.first_name,
            surname=user.last_name,
            date_of_birth=self.cleaned_data['date_of_birth'],
            email=user.email,
            phone_number=self.cleaned_data['phone_number']
        )
        return user



#reservation
# Created by Saad
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['booking_start_date', 'booking_end_date', 'purpose']
        widgets = {
            'booking_start_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

#admin funtion form
#created by Leandro
class UserEditForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(help_text='Format: YYYY-MM-DD')
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=17)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'surname', 'date_of_birth', 'phone_number']

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
            # Atualizar também a instância Person relacionada se necessário
            person, created = Person.objects.update_or_create(
                user=user,
                defaults={
                    'name': user.first_name,
                    'surname': user.last_name,
                    'date_of_birth': user.date_of_birth,
                    'email': user.email,
                    'phone_number': user.phone_number
                }
            )
        return user
