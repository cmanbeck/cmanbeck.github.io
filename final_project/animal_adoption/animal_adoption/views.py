from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, CreateView, DetailView
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
from django.utils.datastructures import MultiValueDict
from django.db import models
# from models import Member
try:
    from .models import Member, Quiz, UserProfile
except Exception: #ImportError
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

        current_user = get_object_or_404(Member, username = username)
        print('=======================================')
        print(request)
        print(current_user)
        print('=======================================')

        if (password == current_user.password):
            # Render the home page
            request.session['member_id'] = member.id

            return redirect('animal_adoption:home')

        else: 
            HttpResponse('Invalid Login')


class Index(View):

    template_name = "app/index.html"
    template = "app/index.html"

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)

    def index(request, success_url=None,
             form_class=UserForm,
             authentication_form=UserForm,
             profile_callback=None,
             template_name='index.html',
             extra_context=None, **kwargs):

        redirect_to = request.REQUEST.get('next', '')

        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES)
            form_auth = authentication_form(data=request.POST)

            if form.is_valid():
                new_user = form.save(profile_callback=profile_callback)
                return HttpResponseRedirect(success_url or reverse('registration_complete'))

            if form_auth.is_valid():
                netloc = urlparse.urlparse(redirect_to)[1]

                if not redirect_to:
                    redirect_to = "/"

                elif netloc and netloc != request.get_host():
                    redirect_to = "/"

                auth_login(request, form_auth.get_user())

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                return HttpResponseRedirect(redirect_to)

        else:
            form = form_class()
            form_auth = authentication_form()


        if extra_context is None:
            extra_context = {}
        context = RequestContext(request)
        for key, value in extra_context.items():
            context[key] = callable(value) and value() or value
        return render_to_response(template_name,
                                  { 'form': form, 'form_auth': form_auth},
                                  context_instance=context) 
