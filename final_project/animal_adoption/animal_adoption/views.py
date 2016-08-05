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
from .models import User
try:
    from .models import Member, Quiz, UserProfile
except Exception:
    from models import Member, Quiz, UserProfile
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
    # model = Post
    context_object_name = 'posts'

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self,request):
        print(request.POST["username"])
        print(request)
        print(request.body)
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        # print(request.POST["username"])
        # username = request.POST["username"]
        # member = get_object_or_404(Member,username=username)
        # if check_password(request.POST["password"],member.password):
        #     if member.is_active:
        #         request.session['member_id'] = member.id
        #         return redirect("animal_adoption:home")
        #         HttpResponse("You are logged in.")
        # else:
        #     return render(request,self.template_name,{"error":"Invalid username or password"})

        current_user = User.objects.filter(username = username)
        print('=======================================')
        print(request)
        print(current_user)
        print('=======================================')

        if (len(current_user) == 1 and password == current_user[0].password):

            request.session['member_id'] = current_user[0].id
            return redirect('animal_adoption:home')

        else: 
            return HttpResponse('Invalid Login')

class Register(View):

    # form_class = RegistrationForm
    # model = User

    template_name = "app/login.html"
    template = "app/login.html"

    def get(self,request):
        return render_to_response(request, self.template_name,)

    def post(self,request):
        member = Member.objects.create(username=request.POST['username'],password=make_password(request.POST["password"]))
        member.save()
        member = get_object_or_404(Member,username = request.POST['username'])
        request.session['member_id'] = member.id
        return render_to_response("animal_adoption/home.html"


