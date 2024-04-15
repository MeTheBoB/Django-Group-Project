from django import forms
from .models import Equipment

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
