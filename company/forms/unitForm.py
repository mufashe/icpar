from django import forms

from company.models import Unit


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }
