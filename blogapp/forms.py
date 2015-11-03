from django import forms

class UploadImgForm(forms.Form):
    img = forms.FileField()
    fileName = forms.CharField(max_length=120)
