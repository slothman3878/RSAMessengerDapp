## Things to Consider
Here are some implementation variations that are worth considering.
1. `ipfshttpclient.py` with `ipfs daemon` |vs| `js-ipfs`
   * for uploading and getting from IPFS
   - Using only python and a ipfs daemon running on the server has the benefit of using our own daemon.
   - Using only python requires exporting the keys and messages as files before uploading them to IPFS.
2. `eth_account` |vs| `django-web3-auth`
     * for User Creation/Authentication
     * Currently using `eth_account` where an account is created for a user. This is honestly a terrible design. If this were an actually dapp deployed on the ethereum main-net, users would prefer to use their own personal wallets for signing transactions.
     * `django-web3-auth` uses the user's private key to authenticate the users. This was what I had originally planned on using, but I haven't figured it out yet, unfortunately. Once I'm done with the `eth_account` implementation, I'll subsequently move to a User model that uses `django-web3-auth` or make my own based on the same principles. A javascript library like Onboard and WalletConnect to gain access to the private key for instance.
     * It occurs to me, however, that having third parties deal with one's private keys is in general a bad idea. It might be better to stick with javascript and send the transaction info to the wallets.

## TODO list
#### Ordered by Importance
* It works... Massive cleanup required.
* Write validator methods for all forms
* Error Handling... (IPFS and EVM error specifically). Right now there isn't any error handling whatsoever.
* Pin messages and public-key using Pinata.
* Deploy to test net.
* (Maybe) Implement a version where the public keys are stored on the blockchain and compare gas prices.
* Entrusting private servers for safe keeping of private keys is far from ideal. Need to think of alternative methods for private key storage.
* Alternative frontend using something like django-web3-auth so that users could use their own wallets instead of generating wallets for each account.
* Some way for users to view "Sent" Messages. Perhaps encrypting the "Sent" messages with their own public_keys and upload it to IPFS as well?
