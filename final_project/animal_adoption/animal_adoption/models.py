from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	username = models.CharField(max_length=30, default = None)
	password = models.CharField(max_length=30, default = None)
	email = models.EmailField(default = None)
	# website = models.URLField(blank = True)

	def __unicode__(self):
		return self.user.username



# class User(AbstractBaseUser, PermissionsMixin):
#     USERNAME_FIELD = 'email'
#     username = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     def get_full_name(self):
#         return self.email
#     def get_short_name(self):
#         return self.email

# class Member(models.Model):
# 	user = models.OneToOneField(User)
	
	# first_name = models.CharField(max_length = 30)
	# last_name = models.CharField(max_length = 30)
	# username = models.CharField(max_length = 30)
	# password = models.CharField(max_length = 30)
	# favorites = models.CharField(max_length = 200)
	# email = models.EmailField(max_length = 30)
	# is_active = models.BooleanField(default = True)

# class Quiz(models.Model):
# 	results = models.CharField(max_length = 300)
# 	date_taken = models.DateTimeField(default = timezone.now)
# 	user_id = models.OneToOneField(Member)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     website = models.URLField(blank = True)