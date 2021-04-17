import json
from web3 import Web3
from web3.contract import ConciseContract

#Provider Instance
#Currently deployed to local hardhat network only
provider = Web3.HTTPProvider('http://127.0.0.1:8545/')
web3 = Web3(provider)
contract_address = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
contract_artifact = json.load(open('Messenger.json',))
abi = contract_artifact['abi']
contract_instance = web3.eth.contract(address=contract_address,abi=abi)

