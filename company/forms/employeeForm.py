from django import forms

from company.models import CompanyEmployee


class EmployeeForm(forms.ModelForm):
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Start Date')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Birth Date')

    class Meta:
        model = CompanyEmployee
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }
