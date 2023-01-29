from django.contrib import admin
from django.urls import path,include
from . import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('homepage.urls'),name = 'homepage'),
    path('scan',include('recognition_app.urls')),
    path('report',include('report.urls'),name='report'),
    path('contact',include('contact.urls'),name='contact'),
   
    # path('history',include('history.urls')),
]
