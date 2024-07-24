from django import forms

from icparsa.models import SecondParty


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = SecondParty
        fields = '__all__'

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
