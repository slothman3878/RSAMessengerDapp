from django.http import HttpResponse
from django.shortcuts import render, redirect

import os
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import ipfshttpclient
from hashlib import sha256

from Scripts.Web3Wrapper import sendMessage, getPublicKey
from Scripts.IpfsWrapper import add, cat

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
                'title': title,
                'body' : body
            }
            data = full_message.__str__().encode('utf-8')

            file_title = sha256((title + request.user.username + datetime.now().strftime('%s')).encode()).hexdigest()
            file_loc = 'temp/'+file_title+'.bin'
            file_out = open(file_loc, 'wb')

            recipient_key = RSA.import_key(cat(getPublicKey(recipient)))
            session_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)

            [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
            file_out.close

            msgHash = add(file_loc)
            sendMessage(request.user.address, recipient, msgHash, request.user.eth_key)

            os.remove(file_loc)
            
            return redirect('home')
        else:
            context['message_form'] = form
    else:
        form = MessageComposeForm()
        context['message_form'] = form
    return render(request, 'Compose/compose.html', context)