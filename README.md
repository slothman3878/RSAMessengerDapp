# RSA messenger Dapp
### Messenger dapp on Ethereum with assymetric encryption

## Introduction
  The idea is to create a messenger service without relying on centralized servers for successful transmission and privacy of messages.<br><br>
  This dapp works as such:
1. When user <b>A</b> registers with the dapp, they generate a public and private key pair.
2. The public key is stored on the ethereum blockchain. The private key is kept by <b>A</b> for safe keeping.
3. If a user <b>B</b> wants to message <b>A</b>, they request the public key from the blockchain, and uses it to encrypt their message.
4. The encrypted messages is stored on a decentralized storage system (in this project, IPFS is used). The CID of the message is stored on the blockchain.
5. <b>A</b> requests the message CID from the blockchain, gets the encrypted message, and decrypts it with their private key.
   
  This is just standard assymetric message encryption, only decentralized, hence better!
  <br><br>
  This works more like a virtual postal service than a messenger service.

## TODO list
* Add function so that third parties can send and recieve messages on user's behalf.