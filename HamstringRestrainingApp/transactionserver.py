import os
import asyncio
import websockets
import base64
from cryptography.x509 import load_pem_x509_certificate, ocsp
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Float
from sqlalchemy import Column
from communication import *


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

#Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


async def pisHandler(websocket):
    currentTimestamp = getTimestamp() - 5000
    private_key = ''
    with open("/code/certs/merchant.key", "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), None)

    # ---- PisCertificate ----

    currentTimestamp, request = await getPacket(websocket, currentTimestamp, 'RAW')

    if request["data"]["message"] == "GET CERTIFICATE":
        with open("/code/certs/merchant.crt", "r") as cert:
            response = await sendPacket(websocket, {"message": cert.read()}, 'RAW')
    else:
        print("Invalid request syntax")
        return

    # ---- MerchantCertificate ----

    currentTimestamp, response = await getPacket(websocket, currentTimestamp, 'RAW')

    if not verifyCertificate(response["data"]["message"], "/code/certs/myCA.pem"):
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

    response = await sendPacket(
        websocket, data, 'RSA', encryptor=cert.public_key().encrypt, signer=private_key.sign)


    # ----- Get Info of paid transaction ----


    currentTimestamp, request = await getPacket(
        websocket, currentTimestamp, 'AES', cipher.decryptor(), verifier=cert.public_key().verify)

    transaction = session.query(Transactionalchemy).filter_by(
        transactionID=request["data"]["transactionID"]).first()
    transaction.status = "PAID"
    session.commit()

    print("[+] Transaction paid: " + str(request["data"]))

    # ----- OK ----

    data = {"message": "OK"}

    response = await sendPacket(
        websocket, data, 'AES', cipher.encryptor(), signer=private_key.sign)





start_server = websockets.serve(pisHandler, "0.0.0.0", 10500)

print("[+] Transaction server running")

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
