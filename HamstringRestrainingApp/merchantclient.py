import websockets
import base64
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from communication import *


async def createTransaction(price, currency, bankAccount):
    currentTimestamp = getTimestamp() - 5000
    private_key = ''

    with open("/code/certs/merchant.key", "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), None)

    websocket = await websockets.connect("ws://172.18.1.3:8755")

    request = await sendPacket(
        websocket, {"message": "GET CERTIFICATE"}, 'RAW')

    with open("certs/merchant.crt", "r") as cert:
        request = await sendPacket(
            websocket, {"message": cert.read()}, 'RAW')


    currentTimestamp, response = await getPacket(websocket, currentTimestamp, 'RAW')


    if not verifyCertificate(response["data"]["message"], "/code/certs/myCA.pem"):
        print("PIS certificate is invalid")
        return

    cert = load_pem_x509_certificate(response["data"]["message"].encode())

    # ---- SecretKey exchange ----

    currentTimestamp, response = await getPacket(websocket, currentTimestamp, 'RSA', decryptor=private_key.decrypt, verifier=cert.public_key().verify)


    aes_key = base64.b64decode(response["data"]["key"])
    aes_iv = base64.b64decode(response["data"]["iv"])

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(aes_iv))

    # ---- Send payment information to create transaction ----

    data = {"currency": currency, "price": price, "bankAccount": bankAccount}

    response = await sendPacket(
        websocket, data, 'AES', cipher.encryptor(), signer=private_key.sign)


    # ---- Get transactionID  ----

    currentTimestamp, request = await getPacket(
        websocket, currentTimestamp, 'AES', decryptor=cipher.decryptor(), verifier=cert.public_key().verify)

    return request["data"]["transactionID"]
