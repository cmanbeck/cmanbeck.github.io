import requests
import project.settings as settings
from datetime import date
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, CreateView, DetailView
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
from django.utils.datastructures import MultiValueDict
from .models import *
from .forms import *

class Home(View):

    template_name = "app/home.html"
    template = "app/home.html"

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)

class Login(View):

    template_name = "app/login.html"
    template = "app/login.html"

    def get(self, request):
        user_form = UserForm()
        profile_form = UserProfileForm()
        print(user_form)
        print(profile_form)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, self.template, context)

    def post(self,request):
        userName = request.POST['username']
        password = request.POST['password']
        current_user = User.objects.get(username = userName)
        print(userName)
        print(password)
        print(current_user)
        hash_password = make_password(password)
        print (hash_password)

        # if (len(current_user) == 1 and password == current_user[0].password):
        if (password == current_user.password):
            print(current_user)
            print(current_user.password)
            request.session['member_id'] = current_user.id
            return redirect('animal_adoption:home')

        else: 
            print('++++++++++++++++++++++')
            return HttpResponse('Invalid Login')

class Register(View):

    template_name = "app/login.html"
    template = "app/login.html"

    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'home.html', {})
        user_form = UserForm()
        profile_form = UserProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template, context)

    def post(self, request):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        print(user_form)
        print(profile_form)

        if profile_form.is_valid():
            # user = user_form.save()
            profile = profile_form.save(commit = False)
            # profile.user = user_form.save()
            profile.save()
            # user.save()
            return redirect('/')

        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }

            return render(request, self.template, context)

class Adopt(View):

    template_name = "app/adopt.html"
    template = "app/adopt.html"

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)

class APISample(View):

    template = "app/home.html"

    def get(self, request, pk= None):
        query = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"
        randomPet = requests.get(query).json()
        print(randomPet)
        return render(request, self.template, randomPet)

    def post(self, request):
        return render(request, self.template)

class FindPet(View):

    template = "app/home.html"

    def get(self, request, pk = None):

        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)
