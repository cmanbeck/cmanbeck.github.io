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
        
        barnyardQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=barnyard"
        randomBarnyard = requests.get(barnyardQuery).json()
        barnyard = randomBarnyard['petfinder']['petIds']['id']['$t']

        birdQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=bird"
        randomBird = requests.get(birdQuery).json()
        bird = randomBird['petfinder']['petIds']['id']['$t']

        catQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=cat"
        randomCat = requests.get(catQuery).json()
        cat = randomCat['petfinder']['petIds']['id']['$t']

        dogQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=dog"
        randomDog = requests.get(dogQuery).json()
        dog = randomDog['petfinder']['petIds']['id']['$t']

        horseQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=horse"
        randomHorse = requests.get(horseQuery).json()
        horse = randomHorse['petfinder']['petIds']['id']['$t']

        pigQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=pig"
        randomPig = requests.get(pigQuery).json()
        pig = randomPig['petfinder']['petIds']['id']['$t']

        reptileQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=reptile"
        randomReptile = requests.get(reptileQuery).json()
        reptile = randomReptile['petfinder']['petIds']['id']['$t']

        smallfurryQuery = "http://api.petfinder.com/pet.getRandom?key=" + settings.SECRET_KEY + "&format=json"+"&animal=smallfurry"
        randomSmallfurry = requests.get(smallfurryQuery).json()
        smallfurry = randomSmallfurry['petfinder']['petIds']['id']['$t']

        petList = []
        idList = [barnyard,bird,cat,dog,horse,pig,reptile,smallfurry]

        for ID in idList:
            petQuery = "http://api.petfinder.com/pet.get?key=" + settings.SECRET_KEY + "&id=" + ID + "&format=json"
            randomPet = requests.get(petQuery).json()
            petList.append(randomPet['petfinder']['pet'])

        name,animal,age,sex,size,breed,shelterName,location,ID,photos = [],[],[],[],[],[],[],[],[],[]

        for i in range(len(petList)):
            name.append(petList[i]['name']['$t'])
            animal.append(petList[i]['animal']['$t'])
            age.append(petList[i]['age']['$t'])
            ID.append(petList[i]['id']['$t'])

            if 'photos' in petList[i]['media'].keys():
                for each in petList[i]['media']['photos']['photo']:
                    #print(each.keys())
                    if each['@size'] == 'pn':
                        photos.append(each['$t'])
                        break
                try:
                    photos[i]
                except IndexError:
                    for each in petList[i]['media']['photos']['photo']:
                        if each['@size'] == 'x':
                            photos.append(each['$t'])
                            break

                try:
                    photos[i]
                except IndexError:
                    photos.append('http://www.jackspets.com/Images/Pet-Care-Information/Pet-Care-Information.png')
                #print(photos[i])
                # print("")
                # print("")

            else:
                photos.append("http://reddeerspca.com/images/content/nophoto.jpg")
            #print(photos[i])
            #print("")
            #print('')

            if petList[i]['sex']['$t'] == 'M':
                sex.append('Male')
            elif petList[i]['sex']['$t'] == 'F':
                sex.append('Female')
            else:
                sex.append('Unknown')

            if petList[i]['size']['$t'] == 'S':
                size.append('Small')
            elif petList[i]['size']['$t'] == 'M':
                size.append('Medium')
            elif petList[i]['size']['$t'] == 'L':
                size.append('Large')
            elif petList[i]['size']['$t'] == 'XL':
                size.append('Extra-Large')


            if type(petList[i]['breeds']['breed']) == type(petList):
                bred = []
                for each in petList[i]['breeds']['breed']:
                    bred.append(each['$t'])
                breed.append(bred)

            elif type(petList[i]['breeds']['breed']) == type(randomPet):
                breed.append([petList[i]['breeds']['breed']['$t']])

            location.append([petList[i]['contact']['city']['$t'],petList[i]['contact']['state']['$t']])

        searchFiltered= {}
        searchFiltered['petfinder'] = {}
        for i in range(len(petList)):
            #print(sex)
            searchFiltered['petfinder'][name[i]] = {}
            searchFiltered['petfinder'][name[i]]['info'] = [name[i],
            photos[i],
            " Animal: "+animal[i],
            " Age: "+ age[i],
            " Sex: "+ sex[i],
            " Size: "+ size[i],
            " Breed: "+"/".join(breed[i]),
            " Location: "+location[i][0]+", "+location[i][1]
            ]

            searchFiltered['petfinder'][name[i]]['ID'] = ID[i]
        searchFiltered['petfinderItems'] = list(searchFiltered['petfinder'].items())
        searchFiltered['petfinderKeys'] = list(searchFiltered['petfinder'].keys())
        searchFiltered['petfinderValues'] = list(searchFiltered['petfinder'].values())
        searchFiltered['petIDs'] = ID

        return render(request, self.template, searchFiltered)


    def post(self, request):
        return render(request, self.template)

class FindPet(View):

    template = "app/search.html"


    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        location = request.POST.get('location')
        if location == "":
            location = '10017'
        print(location)
        animal = request.POST.get('animal')
        breed = request.POST.get('breed')
        sex = request.POST.get('sex')
        size = request.POST.get('size')
        age = request.POST.get('age')


        query = "http://api.petfinder.com/pet.find?key=" + settings.SECRET_KEY + "&location=" + location + "&animal=" + animal + "&breed=" + breed + "&sex=" + sex + "&size=" + size + "&age=" + age + "&format=json"
        search = requests.get(query).json()

        petList = search['petfinder']['pets']['pet']
        name,animal,age,sex,size,breed,shelterName,location,ID,photos = [],[],[],[],[],[],[],[],[],[]

        for i in range(len(petList)):
            name.append(petList[i]['name']['$t'])
            animal.append(petList[i]['animal']['$t'])
            age.append(petList[i]['age']['$t'])
            ID.append(petList[i]['id']['$t'])

            if 'photos' in petList[i]['media'].keys():
                for each in petList[i]['media']['photos']['photo']:
                    #print(each.keys())
                    if each['@size'] == 'pn':
                        photos.append(each['$t'])
                        break
                try:
                    photos[i]
                except IndexError:
                    for each in petList[i]['media']['photos']['photo']:
                        if each['@size'] == 'x':
                            photos.append(each['$t'])
                            break

                try:
                    photos[i]
                except IndexError:
                    photos.append('http://www.jackspets.com/Images/Pet-Care-Information/Pet-Care-Information.png')
                #print(photos[i])
                # print("")
                # print("")

            else:
                photos.append("http://reddeerspca.com/images/content/nophoto.jpg")
            # print(photos[i])
            # print("")
            # print('')

            if petList[i]['sex']['$t'] == 'M':
                sex.append('Male')
            elif petList[i]['sex']['$t'] == 'F':
                sex.append('Female')
            else:
                sex.append('Unknown')

            if petList[i]['size']['$t'] == 'S':
                size.append('Small')
            elif petList[i]['size']['$t'] == 'M':
                size.append('Medium')
            elif petList[i]['size']['$t'] == 'L':
                size.append('Large')
            elif petList[i]['size']['$t'] == 'XL':
                size.append('Extra-Large')


            if type(petList[i]['breeds']['breed']) == type(petList):
                bred = []
                for each in petList[i]['breeds']['breed']:
                    bred.append(each['$t'])
                breed.append(bred)

            elif type(petList[i]['breeds']['breed']) == type(search):
                breed.append([petList[i]['breeds']['breed']['$t']])

            location.append([petList[i]['contact']['city']['$t'],petList[i]['contact']['state']['$t']])

            # print(name[i],"|",animal[i],"|",age[i],"|",sex[i],"|",size[i],"|",breed[i][:],"|",location[i][0],",",location[i][1])
            # print("")

        searchFiltered= {}
        searchFiltered['petfinder'] = {}
        for i in range(len(petList)):
            #print(sex)
            searchFiltered['petfinder'][name[i]] = {}
            searchFiltered['petfinder'][name[i]]['info'] = [name[i],
            # " Animal: "+animal[i],
            photos[i],
            " Breed: "+"/".join(breed[i]),
            " Age: "+ age[i],
            " Sex: "+ sex[i],
            " Size: "+ size[i],
            " Location: "+location[i][0]+", "+location[i][1]]
            

            searchFiltered['petfinder'][name[i]]['ID'] = ID[i]
        searchFiltered['petfinderItems'] = list(searchFiltered['petfinder'].items())
        searchFiltered['petfinderKeys'] = list(searchFiltered['petfinder'].keys())
        searchFiltered['petfinderValues'] = list(searchFiltered['petfinder'].values())
        searchFiltered['petIDs'] = ID

        return render(request, self.template, searchFiltered)

class FindShelter(View):

    template = "app/shelterSearch.html"

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        location = request.POST.get('location')
        if location == "":
            location = '10017'
        name = request.POST.get('name')

        print(location)


        query = "http://api.petfinder.com/shelter.find?key=" + settings.SECRET_KEY + "&location=" + location + "&name=" + name + "&format=json"
        search = requests.get(query).json()
        #print(search)
        #print(query)

        if 'shelters' not in list(search['petfinder'].keys()):
            return HttpResponse("Invalid Location")
        elif 'shelters' in list(search['petfinder'].keys()):
            if 'shelter' not in list(search['petfinder']['shelters'].keys()):
                return HttpResponse("No shelters found. Please try again.")
            elif 'shelter' in list(search['petfinder']['shelters'].keys()):
                shelterList = search['petfinder']['shelters']['shelter']
        name, location , email , phone, fax, email = [], [], [], [], [], []

        #print(type(shelterList), '*****')
        # If you search by location, shelterList is a list
        # If you search by name, shelterList is a dictionary
        if type(shelterList) is not list:
            shelterList = [shelterList]

        for i in range(len(shelterList)):
            name.append(shelterList[i]['name']['$t'])
            # If the address is not listed, append the city, state, and zip code
            if '$t' not in list(shelterList[i]['address1'].keys()):
                location.append(['', '',shelterList[i]['city']['$t'], shelterList[i]['state']['$t'],shelterList[i]['zip']['$t']])
            else:
                if '$t' not in shelterList[i]['address2'].keys():
                    location.append([shelterList[i]['address1']['$t'],'',shelterList[i]['city']['$t'], shelterList[i]['state']['$t'],shelterList[i]['zip']['$t']])
                else:
                    location.append([shelterList[i]['address1']['$t'],shelterList[i]['address2']['$t'],shelterList[i]['city']['$t'], shelterList[i]['state']['$t'],shelterList[i]['zip']['$t']])
            # If the phone number is not listed, append an empty string
            if '$t' not in list(shelterList[i]['phone'].keys()):
                phone.append('')
            else:
                phone.append("Phone: "+shelterList[i]['phone']['$t'])

            if '$t' not in shelterList[i]['fax'].keys():
                fax.append('')
            else:
                fax.append("Fax: "+shelterList[i]['fax']['$t'])

            if '$t' not in shelterList[i]['email'].keys():
                email.append('')
            else:
                email.append(["Email: ","mailto:"+shelterList[i]['email']['$t'],shelterList[i]['email']['$t']])




            # print(name[i],"|",location[i][0]+","+location[i][1]+","+location[i][2],"|",phone[i])
            # print("")


        shelterFiltered = {}
        shelterFiltered['petfinder'] = {}
        for i in range(len(shelterList)):
            if location[i][0] != '':
                if location[i][1] != '':
                    shelterFiltered['petfinder'][name[i]] = [name[i],
                    location[i][0]+" "+location[i][1]+", "+location[i][2]+", "+location[i][3]+" "+location[i][4],
                    phone[i],
                    fax[i],
                    email[i]]
                else:
                    shelterFiltered['petfinder'][name[i]] = [name[i],
                    location[i][0]+", "+location[i][2]+", "+location[i][3]+" "+location[i][4],
                    phone[i],
                    fax[i],
                    email[i]]
            else:
                shelterFiltered['petfinder'][name[i]] = [name[i],
                location[i][2]+", "+location[i][3]+" "+location[i][4],
                phone[i],
                fax[i],
                email[i]]

        shelterFiltered['petfinderItems'] = list(shelterFiltered['petfinder'].items())
        shelterFiltered['petfinderKeys'] = list(shelterFiltered['petfinder'].keys())
        shelterFiltered['petfinderValues'] = list(shelterFiltered['petfinder'].values())
        # print(shelterFiltered)


        # end post function
        return render(request, self.template, shelterFiltered)


class Details(View):

    template = "app/details.html"

    def get(self, request, pk = None):
        return render(request, self.template)

    def post(self, request):
        pet_id = request.GET.get('ID')

        query = "http://api.petfinder.com/pet.get?key=" + settings.SECRET_KEY + "&id=" + pet_id + "&format=json"
        details = requests.get(query).json()

        # dictionary
        pet_details = details['petfinder']['pet']['description']
        pet = details['petfinder']['pet']
        #print(pet_details)
        detailsFiltered = {}
        detailsFiltered['petfinder'] = {}
        #Description
        if '$t' not in pet_details.keys():
            description = "No description available."
        else:
            description = pet_details['$t']

        #Photo
        if 'photos' in pet['media'].keys():
            photos = []
            for each in pet['media']['photos']['photo']:
                if each['@size'] == 'pn':
                    photos.append(each['$t'])
            for each in pet['media']['photos']['photo']:
                #print(each.keys())
                if each['@size'] == 'pn':
                    photo = each['$t']
                    break
            try:
                photo
            except NameError:
                for each in pet['media']['photos']['photo']:
                    if each['@size'] == 'x':
                        photo = each['$t']
                        break

            try:
                photo
            except NameError:
                photo ='http://www.jackspets.com/Images/Pet-Care-Information/Pet-Care-Information.png'
            #print(photos[i])
            # print("")
            # print("")

            if photo in photos:
                photos.remove(photo)




        else:
            photo = "http://reddeerspca.com/images/content/nophoto.jpg"
            photos = ""

        #Name,Animal,Breed,Sex,Age,Size,ShelterName,Address
        name = pet['name']['$t']
        animal = pet['animal']['$t']
        age= pet['age']['$t']

        if pet['status']['$t'] == 'A':
            status = 'Adoptable'
        elif pet['status']['$t'] == 'H':
            status = 'On hold'
        elif pet['status']['$t'] == 'P':
            status = 'Pending'
        elif pet['status']['$t'] == 'X':
            status = 'Adopted/Removed'

        if pet['sex']['$t'] == 'M':
            sex='Male'
        elif pet['sex']['$t'] == 'F':
            sex='Female'
        else:
            sex='Unknown'


        if 'option' in pet['options'].keys():
            print(pet['options']['option'])
            options = []

            if type(pet['options']['option']) == type(details):
                if pet['options']['option']['$t'] == 'hasShots':
                    options.append('Has shots')
                elif pet['options']['option']['$t'] == 'altered':
                    if sex == 'Male':
                        options.append('Neutered')
                    elif sex == 'Female':
                        options.append('Spayed')
                    else:
                        options.append('Spayed/Neutered')
                elif pet['options']['option']['$t'] == 'noCats':
                    options.append('No cats')
                elif pet['options']['option']['$t'] == 'housetrained':
                    options.append('Housetrained')
                elif pet['options']['option']['$t'] == 'specialNeeds':
                    options.append('Housetrained')
                elif pet['options']['option']['$t'] == 'noDogs':
                    options.append('No dogs')
                elif pet['options']['option']['$t'] == 'noClaws':
                    options.append('Declawed')

            elif type(pet['options']['option']) == type([]):
                for each in pet['options']['option']:
                    if each['$t'] == 'hasShots':
                        options.append('Has shots')
                    elif each['$t'] == 'altered':
                        if sex == 'Male':
                            options.append('Neutered')
                        elif sex == 'Female':
                            options.append('Spayed')
                        else:
                            options.append('Spayed/Neutered')
                    elif each['$t'] == 'noCats':
                        options.append('No cats')
                    elif each['$t'] == 'housetrained':
                        options.append('Housetrained')
                    elif each['$t'] == 'specialNeeds':
                        options.append('Special needs')
                    elif each['$t'] == 'noDogs':
                        options.append('No dogs')
                    elif each['$t'] == 'noClaws':
                        options.append('Declawed')

            options = " | ".join(options)
            print(options)
        else:
            options = ''



        shelterID = pet['shelterId']['$t']
        shelterQuery = "http://api.petfinder.com/shelter.get?key=" + settings.SECRET_KEY + "&id=" + shelterID + "&format=json"
        shelter = requests.get(shelterQuery).json()
        print(shelter['petfinder']['shelter'])
        shelter = shelter['petfinder']['shelter']
        print("")
        print("")

        shelterName = shelter['name']['$t']
        if '$t' not in shelter['address1'].keys():
            address1 = ''
        else:
            address1 = shelter['address1']['$t']+", "

        if '$t' not in shelter['address2'].keys():
            address2 = ''
        else:
            address2 = shelter['address2']['$t']+", "

        if '$t' not in shelter['fax'].keys():
            fax = ''
        else:
            fax = shelter['fax']['$t']

        if '$t' not in shelter['email'].keys():
            email = 'None'
        else:
            email = shelter['email']['$t']

        if '$t' not in shelter['phone'].keys():
            phone = ''
        else:
            phone = shelter['phone']['$t']

        if '$t' not in shelter['zip'].keys():
            zipcode = ''
        else:
            zipcode = shelter['zip']['$t']

        if '$t' not in shelter['city'].keys():
            city = ''
        else:
            city = shelter['city']['$t']+", "

        state = shelter['state']['$t']+" "

        shelterLocation1 = "".join([address1,city,state,zipcode])
        print(shelterLocation1)


        if pet['size']['$t'] == 'S':
            size='Small'
        elif pet['size']['$t'] == 'M':
            size='Medium'
        elif pet['size']['$t'] == 'L':
            size='Large'
        elif pet['size']['$t'] == 'XL':
            size='Extra-Large'

        if type(pet['breeds']['breed']) == type([]):
            breed = []
            for each in pet['breeds']['breed']:
                breed.append(each['$t'])

        elif type(pet['breeds']['breed']) == type(details):
            breed=[pet['breeds']['breed']['$t']]

        breed = "/".join(breed)
        #Defining Context
        detailsFiltered['petfinder']['petInformation'] = [
        "Animal: "+animal,
        "Breed: "+breed,
        "Sex: " +sex,
        "Age: "+age,
        options,
        "Status: "+status]

        splitDescription = " ".join(description.split("\n")).split(" ")

        splitDescription2 = []
        for word in splitDescription:
            if ('www' in word or '.com' in word or '.org' in word or '.net' in word) and 'http' not in word and '@' not in word:
                splitDescription2.append("http://"+word)
            else:
                splitDescription2.append(word)

        splitDescription3 = []
        for word in splitDescription2:
            if "@" in word and not(word.startswith('@')):
                if ".org." in word or '.com.' in word or '.net.' in word:
                    splitDescription3.append(["mailto:"+word[:-1],word])
                else:
                    splitDescription3.append(["mailto:"+word,word])
            else:
                splitDescription3.append(word)

        splitDescription4 = []
        for word in splitDescription3:
            if "http" in word and (".org." in word or ".com." in word or ".net." in word):
                splitDescription4.append(word[:-1])
            else:
                splitDescription4.append(word)

        if phone != '' and fax != '':
            detailsFiltered['petfinder']['shelterInformation'] = [shelterName,
            shelterLocation1,
            ["Email: ","mailto:"+email,email],
            "Phone: "+phone,
            "Fax: "+phone]
        elif phone != '' and fax == '':
            detailsFiltered['petfinder']['shelterInformation'] = [shelterName,
            shelterLocation1,
            ["Email: ","mailto:"+email,email],
            "Phone: "+phone]
        elif phone == '' and fax != '':
            detailsFiltered['petfinder']['shelterInformation'] = [shelterName,
            shelterLocation1,
            ["Email: ","mailto:"+email,email],
            "Fax: "+fax]
        else:
            detailsFiltered['petfinder']['shelterInformation'] = [shelterName,
            shelterLocation1,
            ["Email: ","mailto:"+email,email]]

        detailsFiltered['petfinder']['petBigPhoto'] = photo
        detailsFiltered['petfinder']['morePhotos'] = photos
        detailsFiltered['petfinder']['petDescription'] = splitDescription4
        detailsFiltered['petfinder']['petName'] = name


        detailsFiltered['petfinderItems'] = list(detailsFiltered['petfinder'].items())
        detailsFiltered['petfinderKeys'] = list(detailsFiltered['petfinder'].keys())
        detailsFiltered['petfinderValues'] = list(detailsFiltered['petfinder'].values())

        return render(request, self.template, detailsFiltered['petfinder'])