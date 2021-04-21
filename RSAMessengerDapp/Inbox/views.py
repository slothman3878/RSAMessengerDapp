from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

import json

from Scripts.Web3Wrapper import sendMessage, getPublicKey, getRecievedMessageByIndex, getMessage, getRecievedBalance
from Scripts.IpfsWrapper import add, cat
from Scripts.CryptoWrapper import decrypt
from Key.models import Key

# Create your views here.
def inbox_view(request):
    context = { 'messages': [] }
    inbox = json.loads(inbox_api(request).content)
    for message in inbox:
        context['messages'].append(inbox[message])
    return render(request, 'Inbox/inbox.html', context)

def inbox_message_view(request, id):
    context={}
    context.update(json.loads(inbox_message_api(request, id).content))
    return render(request, 'Inbox/inbox_message.html', context)

def inbox_api(request):
    try:
        inbox = {}
        recieved_balance = getRecievedBalance(request.user.address)
        for i in range(recieved_balance):
            inbox.update({ i: getMessage(getRecievedMessageByIndex(i, request.user.address))[0] })
        return JsonResponse(inbox)
    except Exception as ex:
        return JsonResponse({ 'error': ex })

def inbox_message_api(request, id):
    try:
        message = getMessage(getRecievedMessageByIndex(id, request.user.address))
        encrypted_msg = cat(message[2])
        key = Key.objects.filter(is_main_key=True,user=request.user)
        data = decrypt(key[0].private_key, 'hello world', encrypted_msg)
        data_dict = json.loads(data)
        return JsonResponse({
            'from': message[0],
            'to': message[1],
            'title': data_dict['title'],
            'body': data_dict['body'],
            'signed': message[3],
        })
    except Exception as ex:
        return JsonResponse({ 'error': ex })