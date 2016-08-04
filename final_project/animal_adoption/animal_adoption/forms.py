from django import forms
from django.forms import Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website',)

class CreatePost(forms.ModelForm):
	class Meta:
		model = Member
		fields = [
			"username",
			"password",
		]

class UpdatePost(forms.ModelForm):
	class Meta:
		user_post = forms.CharField()

class PostForm(forms.ModelForm):
    class Meta:

        fields = [
            "title",
            "content",
        ]
        widgets = {
            "content": Textarea(attrs={"cols": 50, "rows": 10}),
        }