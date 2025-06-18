from django.urls import path

# from icpars_v2.filemanager.Views.FileUploaderView import uploadFile

from filemanager.Views.FileUploaderView import uploadFile, listFiles

urlpatterns = [
    path('/upload/', uploadFile, name='upload'),
    path('/files/', listFiles, name='files')
]
