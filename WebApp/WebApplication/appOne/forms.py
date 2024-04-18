from django import forms
from .models import Equipment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Person




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
        exclude = ('admin', 'reservation')



class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='First name')
    surname = forms.CharField(max_length=30, required=True, help_text='Last name')
    date_of_birth = forms.DateField(help_text='Format: YYYY-MM-DD')
    phone_number = forms.CharField(max_length=17, required=True)
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, help_text='Select your role')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'surname', 'date_of_birth', 'phone_number', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Person.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                surname=self.cleaned_data['surname'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                phone_number=self.cleaned_data['phone_number'],
                role=self.cleaned_data['role']
            )
        return user
