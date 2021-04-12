from django.conf.urls import url, include
from django.urls import path

from web3auth import urls as web3auth_urls
from web3auth import views as web3auth_views

from . import views

urlpatterns = [
    path('login/', views.loginPage),
    #url(r'^', include(web3auth_urls)),
    url(r'^login_api/$', web3auth_views.login_api, name='web3auth_login_api'),
    url(r'^signup_api/$', web3auth_views.signup_api, name='web3auth_signup_api'),
    url(r'^signup/$', web3auth_views.signup_view, name='web3auth_signup'),
]