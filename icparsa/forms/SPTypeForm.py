from django import forms

from icparsa.models.secondPartyType import SecondPartyType


class SecondPartyForm(forms.ModelForm):
    class Meta:
        model = SecondPartyType
        fields = '__all__'

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
