from datetime import date
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, CreateView, DetailView
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
from django.utils.datastructures import MultiValueDict
from .models import *

class Home(View):

    template_name = "app/home.html"
    template = "app/home.html"

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        return HttpResponse(render(request, self.template))

class Login(View):

    template_name = "app/login.html"
    template = "app/login.html"
    context_object_name = 'posts'

    def get(self, request, pk = None):
        # form in here
        # context
        # pass
        return render(request, self.template)

    def post(self,request):
        password = request.POST['password']
        current_user = User.objects.filter(username = username)

        if (len(current_user) == 1 and password == current_user[0].password):

            request.session['member_id'] = current_user[0].id
            return HttpResponse(redirect('animal_adoption:home'))

        else: 
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

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            return redirect('/')

        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }

            return render(request, self.template, context)

    # def get(self,request):
    #     return HttpResponse(render_to_response(request, self.template_name,))

    # def post(self,request):
    #     print(Member)
    #     print(request.POST)
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     print(username)
    #     print(password)
    #     print(type(username))
    #     member = Member.objects.create_user(username,password)
    #     # member = Member.objects.create(user=request.POST)
    #     member.save()
    #     member = get_object_or_404(Member,username = request.POST['username'])
    #     request.session['member_id'] = member.id
    #     print('=======================================')
    #     print(request)
    #     print(username)
    #     print(password)
    #     print('=======================================')
    #     return HttpResponse(render_to_response("animal_adoption/home.html"))
