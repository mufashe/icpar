from django import forms

from company.models.company import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }
