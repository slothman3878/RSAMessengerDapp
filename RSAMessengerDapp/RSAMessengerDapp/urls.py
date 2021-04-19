"""RSAMessengerDapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from User.views import home_view, signup_view, dashboard_view, login_view, logout_request
from Key.views import keygeneration_view, keyregistration_request
from Compose.views import compose_view
from Inbox.views import inbox_view, inbox_message_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout', logout_request, name='logout'),
    path('keygeneration', keygeneration_view, name='keygeneration'),
    path('keyregistration', keyregistration_request, name='keyregistration'),
    path('compose/', compose_view, name='compose'),
    path('inbox/', inbox_view, name='inbox'),
    path('inbox/<int:id>/', inbox_message_view, name='inbox-message'),
]