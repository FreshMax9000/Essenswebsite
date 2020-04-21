"""
a form is a collection of elements inside <form>...</form> that allow a visitor to do things like enter text, 
select options, manipulate objects or controls, and so on, and then send that information back to the server.
As well as its <input> elements, a form must specify two things:

where: the URL to which the data corresponding to the user’s input should be returned
how: the HTTP method the data should be returned by
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
