import json
from web3 import Web3

import Scripts.IpfsWrapper

#Provider Instance
#Currently deployed to local hardhat network only
#Wrap the whole thing in a class, initialzied with the user address, private_key, and gas price of choice

provider = Web3.HTTPProvider('http://127.0.0.1:8545/')
web3 = Web3(provider)
contract_address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512'
contract_artifact = json.load(open('Messenger.json',))
abi = contract_artifact['abi']
contract_instance = web3.eth.contract(address=contract_address,abi=abi)

def name():
    return contract_instance.functions.name().call()

# Will deal with gas prices later. For now, placeholder values
def setPublicKey(user_address, keyURI, eth_key, gas=3000000, gasPrice=40):
    nonce = web3.eth.getTransactionCount(user_address)

    tx = contract_instance.functions.setPublicKey(user_address, keyURI).buildTransaction({
        'chainId': 31337,
        'gas': gas,
        'gasPrice': web3.toWei(gasPrice, 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx,eth_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def sendMessage(sender, sendee, messageURI, eth_key, gas=3000000, gasPrice=40):
    nonce = web3.eth.getTransactionCount(sender)

    tx = contract_instance.functions.sendMessage(sender,sendee,messageURI).buildTransaction({
        'chainId': 31337,
        'gas': gas,
        'gasPrice': web3.toWei(gasPrice,'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx,eth_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def getMessage(id):
    return contract_instance.functions.getMessage(id).call()

def getRecievedMessageByIndex(id, user_address):
    return contract_instance.functions.getRecievedMessageByIndex(id).call({'from': user_address})

def getSentMessageByIndex(id, user_address):
    return contract_instance.functions.getSentMessageByIndex(id).call({'from': user_address})

def getRecievedBalance(user_address):
    return contract_instance.functions.getRecievedBalance(user_address).call({'from': user_address})

def getSentBalance(user_address):
    return contract_instance.functions.getSentBalance(user_address).call({'from': user_address})

def getPublicKey(user_address):
    return contract_instance.functions.getPublicKey(user_address).call({'from': user_address})
    # returns IPFS hash