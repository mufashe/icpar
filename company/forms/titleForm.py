from django import forms

from company.models import Unit, Department
from company.models.title import Title


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.company is not None:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')
        else:
            self.fields['department'].queryset = Department.objects.none()

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['department'].queryset = Department.objects.filter(company_id=company_id).order_by('name')
            except(ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.company is not None:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')

        # -------------------------------------------------------------------------------------------------------------------------------------------

        if self.instance.department is not None:
            self.fields['unit'].queryset = self.instance.department.unit_set.order_by('name')
        else:
            self.fields['unit'].queryset = Unit.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['unit'].queryset = Unit.objects.filter(department_id=department_id).order_by('name')
            except(ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.department is not None:
            self.fields['unit'].queryset = self.instance.department.unit_set.order_by('name')
