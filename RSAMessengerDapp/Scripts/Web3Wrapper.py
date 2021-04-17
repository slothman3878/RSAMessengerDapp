import json
from web3 import Web3

#Provider Instance
#Currently deployed to local hardhat network only
provider = Web3.HTTPProvider('http://127.0.0.1:8545/')
web3 = Web3(provider)
contract_address = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
contract_artifact = json.load(open('Messenger.json',))
abi = contract_artifact['abi']
contract_instance = web3.eth.contract(address=contract_address,abi=abi)

def name():
    contract_instance.functions.name().call()

# Will deal with gas prices later. For now, placeholder values
def setPublicKey(user_address, keyURI, eth_key, gas=None):
    nonce = web3.eth.getTransactionCount(user_address)

    tx = contract_instance.functions.setPublicKey(user_address, keyURI).buildTransaction({
        'chainId': 31337,
        'gas': 3000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx,eth_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)