from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "What's on your mind?",
                'rows': 6,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...'
            })
        }




class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


