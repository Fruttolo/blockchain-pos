import rsa
import hashlib
import time

def generate_keys():
    public_key, private_key = rsa.newkeys(512)
    return public_key, private_key

def sign(message, private_key):
    # Firma il messaggio utilizzando la chiave privata
    signature = rsa.sign(message.encode(), private_key, 'SHA-256')
    return signature

def verify_signature(message, signature, public_key):
    try:
        # Verifica la firma utilizzando la chiave pubblica
        rsa.verify(message.encode(), signature, public_key)
        return True
    except rsa.VerificationError:
        return False
    
def hash(string):
    return hashlib.sha256(string.encode()).hexdigest()   

def getTimestamp():
    return int(time.time())