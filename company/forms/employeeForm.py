from django import forms

from company.models import CompanyEmployee, Title


class EmployeeForm(forms.ModelForm):
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Start Date')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Birth Date')

    class Meta:
        model = CompanyEmployee
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.department is not None:
            self.fields['title'].queryset = Title.objects.filter(department=self.instance.department).order_by('name')
        else:
            self.fields['title'].queryset = Title.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['title'].queryset = Title.objects.filter(department_id=department_id).order_by('name')
            except(ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.department is not None:
            self.fields['title'].queryset = Title.objects.filter(department=self.instance.department).order_by('name')
