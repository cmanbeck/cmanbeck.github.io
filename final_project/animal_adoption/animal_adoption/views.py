import requests
import project.settings as settings
from datetime import date
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
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

        list_of_users = UserProfile.objects.all()
        cur = False
        for each in list_of_users:
            if each.username == userName:
                cur = True
        if cur:
            current_user = UserProfile.objects.get(username = userName)
            print(userName)
            print(password)
            print(current_user.password)
     #       hash_password = make_password(password)
     #       print (hash_password)

            if (password == current_user.password):
                print(current_user.password)
                # request.session['member_id'] = current_user.id
                return redirect('animal_adoption:home')

            else:
                print('++++++++++++++++++++++')
                return HttpResponse('Incorrect password. Try again')
        else:
            print('++++++++++++++++++++++++')
            return HttpResponse('No account associated with username')

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
        #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(user_form)
        print(profile_form)

        list_of_users = UserProfile.objects.all()
        cur1 = True
        cur2 = True
        for each in list_of_users:
            #print(each.username)
            if each.username == request.POST['username']:
                cur1 = False
            if each.email == request.POST['email']:
                cur2 = False

        if cur1 and cur2:
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
        else:
            if not cur1 and not cur2:
                return HttpResponse("Account already exists")
            elif not cur1 and cur2:
                return HttpResponse("Username already taken")
            elif cur1 and not cur2:
                return HttpResponse("Email already taken")


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

    template = "app/search.html"


    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        location = request.POST.get('location')
        animal = request.POST.get('animal')
        breed = request.POST.get('breed')
        sex = request.POST.get('sex')
        size = request.POST.get('size')
        age = request.POST.get('age')

        query = "http://api.petfinder.com/pet.find?key=" + settings.SECRET_KEY + "&location=" + location + "&animal=" + animal + "&breed=" + breed + "&sex=" + sex + "&size=" + size + "&age=" + age + "&format=json"
        search = requests.get(query).json()

        count = 0
        for each in search['petfinder']['pets']['pet']:
            print("NEW PET")
            print(each.keys())
            for x in each.values():
                print("New info")
                print(x.keys())
                print(x.values())
            count += 1
        print(count)

        petList = search['petfinder']['pets']['pet']
        name,animal,age,sex,size,breed,shelterName,location = [],[],[],[],[],[],[],[]

        for i in range(len(petList)):
            name.append(petList[i]['name']['$t'])
            animal.append(petList[i]['animal']['$t'])
            age.append(petList[i]['age']['$t'])
            sex.append(petList[i]['sex']['$t'])
            size.append(petList[i]['size']['$t'])

            if type(petList[i]['breeds']['breed']) == type(petList):
                bred = []
                for each in petList[i]['breeds']['breed']:
                    bred.append(each['$t'])
                breed.append(bred)

            elif type(petList[i]['breeds']['breed']) == type(search):
                breed.append([petList[i]['breeds']['breed']['$t']])

            location.append([petList[i]['contact']['city']['$t'],petList[i]['contact']['state']['$t']])

            print(name[i],"|",animal[i],"|",age[i],"|",sex[i],"|",size[i],"|",breed[i][:],"|",location[i][0],",",location[i][1])
            print("")

        searchFiltered = {}
        searchFiltered['petfinder'] = {}
        for i in range(len(petList)):
            searchFiltered['petfinder'][name[i]] = animal[i],age[i],sex[i],size[i],breed[i][:],location[i][0],location[i][1]
        print(searchFiltered)

        return render(request, self.template, searchFiltered)

class FindShelter(View):

    template = "app/search.html"


    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        location = request.POST.get('location')
        name = request.POST.get('name')
        
        query = "http://api.petfinder.com/shelter.find?key=" + settings.SECRET_KEY + "&location=" + location + "&name=" + name + "&format=json"
        search = requests.get(query).json()

        count = 0
        for each in search['petfinder']['shelters']['shelter']:
            print("##################################################")
            print(each.keys())
            for x in each.values():
                print("New info")
                print(x.keys())
                print(x.values())
            count += 1
        print(count)

        shelterList = search['petfinder']['shelters']['shelter']
        name, location = [], []

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        for i in range(len(shelterList)):
            name.append(shelterList[i]['name']['$t'])
            location.append([shelterList[i]['address1']['$t'], shelterList[i]['city']['$t'], shelterList[i]['state']['$t']])

            print(address1[i],"|",city[i],"|",state[i],"|",location[i][0],",",location[i][1])
            print("")

        shelterFiltered = {}
        shelterFiltered['petfinder'] = {}
        for i in range(len(shelterList)):
            shelterFiltered['petfinder'][name[i]] = name[i], address1[i], city[i], state[i], location[i][0], location[i][1]
        print(shelterFiltered)

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        return render(request, self.template, search)



