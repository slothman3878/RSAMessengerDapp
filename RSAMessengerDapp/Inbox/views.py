from django.http import HttpResponse
from django.shortcuts import render, redirect

import os, json
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import ipfshttpclient
from hashlib import sha256

from Scripts.Web3Wrapper import sendMessage, getPublicKey, getRecievedMessageByIndex, getMessage
from Scripts.IpfsWrapper import add, cat
from Key.models import Key

# Create your views here.
def decrypt(pem, passphrase, hash):
    # the key is saved as a string, not a bytestring. Need some way to save this differently
    private_key = RSA.import_key(pem.encode('utf-8'), passphrase=passphrase)
    encrypted_data = cat(hash)
    
    split_index = private_key.size_in_bytes()
    enc_session_key = encrypted_data[0:split_index]
    nonce = encrypted_data[split_index:split_index+16]
    split_index+=16
    tag = encrypted_data[split_index:split_index+16]
    split_index+=16
    ciphertext = encrypted_data[split_index:]

    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data.decode('utf-8')

def inbox_view(request):
    context = {}
    return render(request, 'Inbox/inbox.html', context)

def inbox_message_view(request, id):
    context = {}
    key = Key.objects.filter(is_main_key=True,user=request.user)
    data = decrypt(key[0].private_key, 'hello world', getMessage(getRecievedMessageByIndex(id, request.user.address)))
    data_dict = json.loads(data)
    context['from'] = data_dict['from']
    context['to'] = data_dict['to']
    context['title'] = data_dict['title']
    context['body'] = data_dict['body']
    return render(request, 'Inbox/inbox_message.html', context)