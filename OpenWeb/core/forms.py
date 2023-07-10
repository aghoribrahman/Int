from django import forms

class FolderUploadForm(forms.Form):
    folder = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))
