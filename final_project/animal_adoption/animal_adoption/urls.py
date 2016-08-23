from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', Login.as_view(), name = "login"),
    url(r'^adopt/', Adopt.as_view(), name = "adopt"),
    url(r'^register/', Register.as_view(), name = "register"),
    # url(r'^random_pet/', APISample.as_view(), name = "random_pet"),
    url(r'^find_pet/', FindPet.as_view(), name = "find_pet"),
    url(r'^find_shelter/', FindShelter.as_view(), name = "find_shelter"),
    url(r'^details/', Details.as_view(), name = "details"),
    url(r'^', APISample.as_view(), name = "home"),
]