# RSA Messenger Dapp
### Messenger dapp on Ethereum with assymetric encryption

## Introduction
  The idea is to create an online messenger service without relying on centralized servers for successful transmission and privacy of messages. Messages can be transmitted between different frontend platforms as long as they tap into the same messenger contract.<br><br>
  This dapp works as such:
1. When user <b>A</b> registers with the dapp, they generate a public and private key pair.
2. The public key is stored on the ethereum blockchain. The private key is kept by <b>A</b> for safe keeping.
3. If a user <b>B</b> wants to message <b>A</b>, they request the public key from the blockchain, and uses it to encrypt their message.
4. The encrypted messages is stored on a decentralized storage system (in this project, IPFS is used). The CID of the message is stored on the blockchain.
5. <b>A</b> requests the message CID from the blockchain, gets the encrypted message, and decrypts it with their private key.
   
  This is just standard assymetric encryption, only decentralized, hence better!
  <br><br>
  RSA encryption is only worth a damn if the keys are at least 2048 bits long. While one can store those keys on the blockchain, that's 256 bytes (plus bytes needed to store the public exponent) worth of blockchain memory being altered, resulting in a high gas price.
  <br><br>
  Here, we have an alternative: upload the public key to IPFS and store the CID on the blockchain instead, which should result in significanlty a lower gas price (theoretically).

## Description for 'method-3' branch
Using <b>web3-auth</b> and <b>web3.py</b>
* Create an account with an ethereum address from some third party wallet (will use just Metamask for now, since its convenient).
* login via `window.ethereum` or perhaps <b>Wallet Connect</b> with the <b>private key</b>.
* Use a <b>Alchemy.api</b> node to interact with ethereum

The whole purpose of this project is to
<ol type='A'>
  <li>Learn and use basic Django.</li>
  <li>Use web3.py with it.</li>
</ol>
Instead of defaulting to the usual <b>React.js</b> with some javascript-based ethereum provider.

## Important!!!
  The frontend is merely for demonstration. It should not be used seriously.

## TODO list
#### Ordered by Importance
* Create frontend using Django, web3.py, and eth-account (currently leaning towards creating an ethereum address with a signup).
* Pin messages and public-key using Pinata.
* Deploy to test net.
* Add function so that third parties can send and recieve messages on user's behalf.
* (Maybe) Implement a version where the public keys are stored on the blockchain and compare gas prices.
* Entrusting private servers for safe keeping of private keys is far from ideal. Need to think of alternative methods for private key storage.
