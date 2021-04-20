from django.http import HttpResponse
from django.shortcuts import render, redirect

import os, json
from datetime import datetime
from hashlib import sha256

from Scripts.Web3Wrapper import sendMessage, getPublicKey
from Scripts.IpfsWrapper import add, cat
from Scripts.CryptoWrapper import encrypt

from .forms import MessageComposeForm

# Create your views here.
def compose_view(request):
    context={}
    if request.POST:
        form = MessageComposeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            recipient = form.cleaned_data.get('recipient')
            full_message = {
                'from' : request.user.address,
                'to'   : recipient,
                'title': title,
                'body' : body,
            }

            file_title = sha256((title + request.user.username + datetime.now().strftime('%s')).encode()).hexdigest()
            file_loc = 'temp/'+file_title+'.bin'

            encrypt(full_message, cat(getPublicKey(recipient)), file_loc)

            msgHash = add(file_loc)
            os.remove(file_loc)

            sendMessage(request.user.address, recipient, msgHash, request.user.eth_key)
            
            return redirect('home')
        else:
            context['message_form'] = form
    else:
        form = MessageComposeForm()
        context['message_form'] = form
    return render(request, 'Compose/compose.html', context)