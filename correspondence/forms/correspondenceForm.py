from django import forms

from correspondence.models import Correspondence


class CorrespondenceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Correspondence
        fields = '__all__'
