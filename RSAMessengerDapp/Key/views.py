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

#Currently deployed to local hardhat network only
provider = Web3.HTTPProvider('http://127.0.0.1:8545/')
web3 = Web3(provider)
contract_address = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
contract_artifact = json.load(open('Messenger.json',))
abi = contract_artifact['abi']
contract_instance = web3.eth.contract(address=contract_address,abi=abi)

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

            now = datetime.now().strftime('%s')
            file_title = sha256(('public key' + request.user.username + datetime.now().strftime('%s')).encode()).hexdigest()
            file_loc = 'Key/temp/'+file_title+'.pem'
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

            key = Key(user=request.user, public_key=public_key, private_key=private_key, is_main_key=True)
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