from django.shortcuts import render, redirect

from filemanager.forms.fileManagerForm import FileUploaderForm
from filemanager.models.fileManagerModel import FileUploader


def uploadFile(request):
    if request.method == 'POST':
        form = FileUploaderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('fileList')
    else:
        form = FileUploaderForm()

    return render(request, 'filemanager/upload.html', {'form': form})


def listFiles(request):
    files = FileUploader.objects.all()
    return render(request, 'filemanager/filelist.html', {'files': files})
