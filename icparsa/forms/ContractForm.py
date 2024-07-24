from django import forms

from icparsa.models import Contract, DepartmentMember, ContractSetting


class ContractForm(forms.ModelForm):
    signedDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Signed On')
    expirationDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Expires Date')

    class Meta:
        model = Contract
        fields = '__all__'
        exclude = ['notificationSentOn']

        labels = {
            'name': 'Title',
            # 'contract_type': 'Type',
            'contract_status': 'Status',
            'expirationDate': 'Expiration Date',
            'secondParty': 'Company',
            'departmentUnit': 'Unit',
            'contractCategory': 'Select Category',
            'contractType': 'Available Type',
        }

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'contract_status': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:540px', "rows": 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.department is not None:
            self.fields['departmentUnit'].queryset = self.instance.department.departmentmember_set.order_by('name')
        else:
            self.fields['departmentUnit'].queryset = DepartmentMember.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['departmentUnit'].queryset = DepartmentMember.objects.filter(
                    department_id=department_id).order_by('name')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department is not None:
            self.fields['departmentUnit'].queryset = self.instance.department.departmentmember_set.order_by('name')

        # ----------------------------------------------------------------------------------------------------------------------

        if self.instance.contractCategory is not None:
            self.fields['contractType'].queryset = self.instance.contractCategory.contractsetting_set.order_by('name')
        else:
            self.fields['contractType'].queryset = ContractSetting.objects.none()

        if 'contractCategory' in self.data:
            try:
                contractName_id = int(self.data.get('contractCategory'))
                self.fields['contractType'].queryset = ContractSetting.objects.filter(
                    contractName_id=contractName_id).order_by('name')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.contractCategory is not None:
            self.fields['contractType'].queryset = self.instance.contractCategory.contractsetting_set.order_by('name')
