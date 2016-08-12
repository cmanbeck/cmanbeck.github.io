from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^index/', Index.as_view(), name = "index"),
    url(r'^login/', Login.as_view(), name = "login"),
    url(r'^adopt/', Adopt.as_view(), name = "adopt"),
    url(r'^register/', Register.as_view(), name = "register"),
    url(r'^random_pet/', APISample.as_view(), name = "random_pet"),
    url(r'^', Home.as_view(), name = "home"),
]