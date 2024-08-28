from django import forms

from company.models import Unit, Department


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.company is not None:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')
        else:
            self.fields['department'].queryset = Department.objects.all()
        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['department'].queryset = Department.objects.filter(company_id=company_id).order_by('name')
            except(ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.company is not None:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')
