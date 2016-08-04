from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', Home.as_view(), name = "home"),
    url(r'^login/', Login.as_view(), name = "login"),
    url(r'^', Index.as_view(), name = "index"),
]