from django import forms

from icparsa.models import DepartmentMember


class DepartmentMemberForm(forms.ModelForm):
    class Meta:
        model = DepartmentMember
        fields = '__all__'
