"""
URL configuration for BookLender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp.views import *
from messagesApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', index, name='index'),
    path('work/', work, name='work'),
    path('about/', about, name='about'),
    path('category/', category, name='category'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('', include('messagesApp.urls')),
    path('profile/', profile, name='dashboard'),
    path('add-book/', addBook, name='addBook'),
    path('remove-book/', removeBook, name='removeUserBook'),
    path('update-profile/', updateProfile, name='updateProfile'),
    path('messages/', loadFullConversation, name='conversation'),
    path('messages/send/', sendMessage, name='sendMessage'),
]
