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
  
  This is just standard assymetrically encrypted messaging, only decentralized, hence better!
  <br><br>
  RSA encryption is only worth a damn if the keys are at least 2048 bits long. While one can store those keys on the blockchain, that's 256 bytes (plus bytes needed to store the public exponent) worth of blockchain memory being altered, resulting in a high gas price.
  <br><br>
  Here, we have an alternative: upload the public key to IPFS and store the CID on the blockchain instead, which should result in a significanlty lower gas price (theoretically).
  <br><br>
  The message itself is a `.json` with the following format:
  ```
    {
        'from' : ... ,
        'to'   : ... ,
        'title': ... ,
        'body' : ...
    }
  ```

## Important!!!
  The frontend is merely for demonstration. It should not be used seriously. It is in fact, a terrible frontend since it stores not only the private RSA keys for its users, it also stores&ndash;although immediately deletes after creation&ndash;private messages, encrypted or no. Then there's the fact that it handles and stores the addresses and private-keys of its users in the database.