from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def signupPage(request):
    context = {}
    return render(request, 'Messenger/signup.html', context)

def loginPage(request):
    if not request.user.is_authenticated:
        return render(request, 'Messenger/login.html')
    else:
        return redirect('../admin/login/')