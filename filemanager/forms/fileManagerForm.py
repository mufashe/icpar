from django import forms

from filemanager.models.fileManagerModel import FileUploader


class FileUploaderForm(forms.ModelForm):
    class Meta:
        model = FileUploader
        fields = ['file']
