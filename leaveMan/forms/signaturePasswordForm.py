from django import forms


class SignaturePasswordForm(forms.Form):
    signature_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
                                         label='Signature Password')
