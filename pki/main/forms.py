from django import forms

class UploadForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your name',
        'class': 'form-control'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-control'
    }))
    public_key = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Enter text content of .pem file',
        'class': 'form-control',
        'rows': 10,
        'cols': 50
    }))

class VerifyForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-control'
    }))
    cert = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Enter text content of .pem file',
        'class': 'form-control',
        'rows': 10,
        'cols': 50
    }))
