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
        fields = ('username', 'password', 'email')

# class UserForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website',)

# class RegistrationForm(forms.Form):
#     username = forms.EmailField(max_length=30)
#     password1 = forms.CharField()
#     password2 = forms.CharField()
#     email = forms.EmailField(max_length=100)

#     def clean(self):
#         cleaned_data = super(RegistrationForm, self).clean()
#         username = cleaned_data.get("username")
#         password1 = cleaned_data.get("password1")
#         password2 = cleaned_data.get("password2")

#     class Meta:
#         model = User

# class CreatePost(forms.ModelForm):
# 	class Meta:
# 		model = Member
# 		fields = [
# 			"username",
# 			"password",
# 		]

# class UpdatePost(forms.ModelForm):
# 	class Meta:
# 		user_post = forms.CharField()

# class PostForm(forms.ModelForm):
#     class Meta:

#         fields = [
#             "title",
#             "content",
#         ]
#         widgets = {
#             "content": Textarea(attrs={"cols": 50, "rows": 10}),
        # }