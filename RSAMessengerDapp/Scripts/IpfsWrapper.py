import ipfshttpclient

client = ipfshttpclient.connect()

def add(file_loc):
    res = client.add(file_loc)
    return res['Hash']

def cat(hash):
    return client.cat(hash)