from django.http import HttpResponse
from django.shortcuts import render, redirect

import os
from datetime import datetime
from Crypto.PublicKey import RSA
import ipfshttpclient
from hashlib import sha256

from Scripts.Web3Wrapper import setPublicKey

from .models import Key
from .forms import KeyGenerationForm

# Create your views here.
def keygeneration_view(request):
    context = {}
    if request.POST:
        form = KeyGenerationForm(request.POST)
        if form.is_valid():
            passphrase = form.cleaned_data.get('passphrase')
            rsa_key = RSA.generate(2048)
            private_key = rsa_key.export_key(passphrase=passphrase, pkcs=8, protection='scryptAndAES128-CBC')
            public_key = rsa_key.public_key().export_key('PEM')

            # probably best if I created a wrapper for IPFS to. Add add and cat functions
            now = datetime.now().strftime('%s')
            file_title = sha256(('public key' + request.user.username + datetime.now().strftime('%s')).encode()).hexdigest()
            file_loc = 'temp/'+file_title+'.pem'
            file_out = open(file_loc,'wb')
            file_out.write(public_key)
            file_out.close()

            client = ipfshttpclient.connect()
            res = client.add(file_loc)

            os.remove(file_loc)

            # Save those keys to the database
            keys = Key.objects.filter(is_main_key=True)
            for key in keys:
                key.is_main_key=False
                key.save()

            key = Key(user=request.user, public_key=public_key.decode('utf-8'), private_key=private_key.decode('utf-8'), is_main_key=True)
            key.save()

            setPublicKey(request.user.address, res['Hash'], request.user.eth_key)

            return redirect('home')
        else:
            context['keygeneration_form'] = form
    else:
        form = KeyGenerationForm()
        context['keygeneration_form'] = form
    return render(request, 'User/keygeneration.html', context)

def keyregistration_request(request):
    keys = Key.objects.filter(user=request.user)
    return HttpResponse('hello')