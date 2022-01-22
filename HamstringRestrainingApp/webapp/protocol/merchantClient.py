import hashlib
import asyncio
import websockets
import json
import base64
from cryptography.x509 import load_pem_x509_certificate, ocsp
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime
import urllib.parse

from communication import *


async def hello():
    currentTimestamp = getTimestamp() 
    private_key = ''
    
    with open("certs/merchant.key", "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), None)

    websocket = await websockets.connect("ws://localhost:8755")

    currentTimestamp, request = createPacket(
                {"message" : "GET CERTIFICATE"}, 'RAW', signer=private_key.sign)
    
    await websocket.send(request)

    with open("certs/merchant.crt", "r") as cert:
        currentTimestamp, request = createPacket(
                {"message" : cert.read()}, 'RAW', signer=private_key.sign)
    
    await websocket.send(request)

    

    response = await websocket.recv()
    currentTimestamp, response = parsePacket(response, currentTimestamp, 'RAW')

    print(response)

    if not verifyCertificate(response["data"]["message"]):
        print("PIS certificate is invalid")
        return

    cert = load_pem_x509_certificate(response["data"]["message"].encode())

    # ---- SecretKey exchange ----

    response = await websocket.recv()
    currentTimestamp, response = parsePacket(response, currentTimestamp, 'RSA', decryptor=private_key.decrypt, verifier=cert.public_key().verify)

    print(response)

    aes_key = base64.b64decode(response["data"]["key"])
    aes_iv = base64.b64decode(response["data"]["iv"])


    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(aes_iv))
    encryptor = cipher.encryptor()

    data = {"currency" : "dollar", "price" : 500, "bankAccount" : "1283728193993"}


    currentTimestamp, response = createPacket(
        data, 'AES', cipher.encryptor(), signer=private_key.sign)


    await websocket.send(response)

    #cert = load_pem_x509_certificate(bytes(cert, 'utf-8'))

    request = await websocket.recv()
    currentTimestamp, request = parsePacket(
        request, currentTimestamp, 'AES', decryptor=cipher.decryptor(), verifier=cert.public_key().verify)

    print(request)



asyncio.run(hello())