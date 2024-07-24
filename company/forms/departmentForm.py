from django import forms

from company.models.department import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }
