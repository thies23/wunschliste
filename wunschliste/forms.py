from django import forms
from .models import Wish


class PublicPasswordForm(forms.Form):
    
    password = forms.CharField(
        label="Passwort",
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Passwort eingeben'
        })
    )


class GiverNameForm(forms.Form):
    
    giver_name = forms.CharField(
        label="Dein Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dein Name',
            'required': True
        })
    )



class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = ['title', 'description', 'link', 'image', 'image_url', 'price', 'urgency']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Produktbezeichnung'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Kurze Beschreibung'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://.../image.jpg'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'urgency': forms.Select(attrs={
                'class': 'form-select'
            }),
        }