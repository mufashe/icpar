from django import forms

from icparsa.models.contractSetting import ContractSetting, ContractSettingName


class ContractSettingForm(forms.ModelForm):
    class Meta:
        model = ContractSetting
        fields = '__all__'
        widgets = {
            'remindingTimes': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class ContractSettingNameForm(forms.ModelForm):
    class Meta:
        model = ContractSettingName
        fields = '__all__'
