from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json

# Error handling required
def encrypt(data, pem, file_loc):
    assert(file_loc[-4:]=='.bin') #The encrypted file must be a binary file

    encoded_data = json.dumps(data, indent=4).encode('utf-8')

    # Encrypt session key with RSA key
    recipient_key = RSA.import_key(pem)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    session_key = get_random_bytes(16)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt text with session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(encoded_data)

    # Write out the ciphertext in the given file location
    with open(file_loc, 'wb') as file_out:
        [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

def decrypt(pem, passphrase, encrypted_data):
    # the key is saved as a string, not a bytestring. Need some way to save this differently
    private_key = RSA.import_key(pem.encode('utf-8'), passphrase=passphrase)
    
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