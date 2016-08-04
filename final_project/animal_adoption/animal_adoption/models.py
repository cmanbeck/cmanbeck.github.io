from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Member(models.Model):
	user = models.OneToOneField(User)
	
	# first_name = models.CharField(max_length = 30)
	# last_name = models.CharField(max_length = 30)
	# username = models.CharField(max_length = 30)
	# password = models.CharField(max_length = 30)
	# favorites = models.CharField(max_length = 200)
	# email = models.EmailField(max_length = 30)
	# is_active = models.BooleanField(default = True)

class Quiz(models.Model):
	results = models.CharField(max_length = 300)
	date_taken = models.DateTimeField(default = timezone.now)
	user_id = models.OneToOneField(Member)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank = True)