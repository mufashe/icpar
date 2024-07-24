from django import forms

from icparsa.models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }
