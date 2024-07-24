from django import forms
from django.utils.safestring import mark_safe

from company.models import EmployeeAsUserSignature


# class SignaturePadWidget(forms.Widget):
#     template_name = 'company/employee/signaturePad.html'  # Create this template
#
#     def render(self, name, value, attrs=None, renderer=None):
#         return mark_safe(f'<div id="{name}_signature_pad"></div>')
#
#     def value_from_datadict(self, data, files, name):
#         # Handle form submission and retrieve the signature data
#         return data.get(name, None)


class UserAsEmployeeSignatureForm(forms.ModelForm):
    class Meta:
        model = EmployeeAsUserSignature
        fields = '__all__'

        widgets = {
            'signature_password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),

        }

