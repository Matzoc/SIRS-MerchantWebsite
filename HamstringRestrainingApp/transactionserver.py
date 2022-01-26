from ast import Expression
import os
import asyncio
from string import printable
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
import hashlib
from flask_login import UserMixin

from communication import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String, BigInteger, Float
from sqlalchemy import Column


Base = declarative_base()


class Transactionalchemy(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    transactionID = Column(String(97), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(97), nullable=False)
    clientemail = Column(String(100), nullable=False)
    status = Column(String(100), default="UNPAID", nullable=False)


engine = create_engine(
    'mysql://root:password@' + "172.18.2.4" + '/test',
    echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


async def pisHandler(websocket):
    currentTimestamp = getTimestamp() - 100
    private_key = ''
    with open("/code/certs/merchant.key", "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), None)

    # ---- PisCertificate ----

    request = await websocket.recv()
    currentTimestamp, request = parsePacket(request, currentTimestamp, 'RAW')
    print(request)

    if request["data"]["message"] == "GET CERTIFICATE":
        with open("/code/certs/merchant.crt", "r") as cert:
            # cert = load_pem_x509_certificate(bytes(cert, 'utf-8'))
            currentTimestamp, response = createPacket(
                {"message": cert.read()}, 'RAW', signer=private_key.sign)
            await websocket.send(response)
    else:
        print("Invalid request syntax")
        return

    # ---- MerchantCertificate ----

    response = await websocket.recv()
    currentTimestamp, response = parsePacket(response, currentTimestamp, 'RAW')

    print(response)

    if not verifyCertificate(response["data"]["message"]):
        print("PIS certificate is invalid")
        return

    cert = load_pem_x509_certificate(
        bytes(response["data"]["message"], 'utf-8'))

    # ---- SecretKey exchange ----

    aes_key = os.urandom(32)
    aes_iv = os.urandom(16)

    data = {"key": base64.b64encode(aes_key).decode(
    ), "iv": base64.b64encode(aes_iv).decode()}

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(aes_iv))
    encryptor = cipher.encryptor()

    currentTimestamp, response = createPacket(
        data, 'RSA', encryptor=cert.public_key().encrypt, signer=private_key.sign)

    await websocket.send(response)

    # ----- Create transaction ----

    request = await websocket.recv()
    currentTimestamp, request = parsePacket(
        request, currentTimestamp, 'AES', cipher.decryptor(), verifier=cert.public_key().verify)

    transaction = session.query(Transactionalchemy).filter_by(
        transactionID=request["data"]["transactionID"]).first()

    transaction.status = "PAID"
    session.commit();



    data = {"message": "OK"}

    currentTimestamp, response = createPacket(
        data, 'AES', cipher.encryptor(), signer=private_key.sign)

    await websocket.send(response)

    print(request["data"])


start_server = websockets.serve(pisHandler, "0.0.0.0", 10500)

print("Transaction server running")

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
