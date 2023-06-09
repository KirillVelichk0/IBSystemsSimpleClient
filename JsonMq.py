import struct
import socket
import os
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class HelpPrint:
    def SetBox(self, boxE, boxD):
        self.boxE = boxE
        self.boxD = boxD

    def SetE(self, encr):
        from tkinter import END
        self.boxE.delete("1.0", END)
        self.boxE.insert("1.0", encr)

    def SetB(self, decr):
        from tkinter import END
        self.boxD.delete("1.0", END)
        self.boxD.insert("1.0", decr)


helper = HelpPrint()

def generate_keys():
    modulus_length = 2048

    key = RSA.generate(modulus_length)
    #print (key.exportKey())

    pub_key = key.publickey()
    #print (pub_key.exportKey())

    return key, pub_key


class JsonMq:
    def __init__(self) -> None:
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 2001
        self.sockConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockConn.connect((HOST, PORT))
        #self.sockConn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.maxLenMessageConst = 100000
        self.unprocessed_bytes = bytearray()
        self.cipher = None
    
    def SecureChannel(self):
        self.GenAndSendTriplet()
        return self.GetAndVerifyTriplet()
    
    def GenAndSendTriplet(self):
        (privkey, pubkey) = generate_keys()
        nonce = os.urandom(32)
        digest = SHA256.new(nonce)
        signature = pkcs1_15.new(privkey).sign(digest)
        self.SendBytes(signature)
        self.sockConn.sendall(nonce)
        pubkey_str = pubkey.export_key()
        self.SendBytes(pubkey_str)
        
        
        
    def GetAndVerifyTriplet(self):
        try:
            s = self.GetBytes()
            nonce = bytes(self.GetForCount(32))
            digest = SHA256.new(nonce)
            openKey = self.Get()
            openKey = RSA.import_key(openKey)
            pkcs1_15.new(openKey).verify(digest, s)
            print("Verify is very nice")
            return True
        except Exception as ex:
            print(str(ex))
            return False
            
        
        
    def Send(self, jsonMessage) -> str:
        if len(jsonMessage) > self.maxLenMessageConst :
            return 'Too big input'
        jsonBinary = jsonMessage.encode()
        jsonLenBuffer = struct.pack("!L", len(jsonBinary))
        if(self.cipher is not None):
            jsonLenBuffer = self.cipher.CryptDectypt(jsonLenBuffer)
            print("Message before encrypting "+ str(jsonMessage))
            helper.SetB(str(jsonMessage))
            jsonBinary = self.cipher.CryptDectypt(jsonBinary)
            helper.SetE(str(jsonBinary))
            print("Message after encrypting "+ str(jsonBinary))
        print("len " + str(len(jsonBinary)))
        self.sockConn.sendall(jsonLenBuffer)
        print(jsonBinary)
        self.sockConn.sendall(jsonBinary)
        return 'sended'
    
    def SendBytes(self, bytes_in):
        if len(bytes_in) > self.maxLenMessageConst :
            return 'Too big input'
        bytesLenBuffer = struct.pack("!L", len(bytes_in))
        if(self.cipher is not None):
            bytes_in = self.cipher.CryptDectypt(bytes_in)
            bytesLenBuffer = self.cipher.CryptDectypt(bytesLenBuffer)
        print("len " + str(len(bytes_in)))
        self.sockConn.sendall(bytesLenBuffer)
        print(bytes_in)
        self.sockConn.sendall(bytes_in)
        return 'sended'
    
    
    
    def GetForCount(self, count):
        count_bytes = 0
        resBytes = bytearray()
        if len(self.unprocessed_bytes) > 0:
            optimal_len = min(count, len(self.unprocessed_bytes))
            resBytes = self.unprocessed_bytes[0:optimal_len]
            self.unprocessed_bytes = self.unprocessed_bytes[optimal_len:]
            count_bytes = optimal_len
            print("Getting from unprocess " + str(resBytes))
            print(optimal_len)
            print(count)
        while count_bytes < count:
            print("Getting from socket")
            gettedBytes = bytearray(self.sockConn.recv(4096))
            print(gettedBytes)
            if(count_bytes + len(gettedBytes) > count):
                print("Many bytes")
                limSz = count - count_bytes
                resBytes += gettedBytes[0 : limSz]
                print(limSz)
                print(resBytes)
                self.unprocessed_bytes += gettedBytes[limSz: ]
                print("COpied to unprocessed " + str(self.unprocessed_bytes))
            else:
                print(str(resBytes))
                resBytes += gettedBytes
            print("Bytes getted")
            count_bytes += len(gettedBytes)
            print("Cur count " + str(count_bytes))
            print("Count " + str(count))
        print("Cycle ended")
        return resBytes
    
    
    def Get(self):
        print("Json getting started")
        packLen = self.GetForCount(4)
        if self.cipher is not None:
            packLen = self.cipher.CryptDectypt(bytes(packLen))
        print("data received")
        packLenI = int.from_bytes(packLen, byteorder= 'big', signed= False)
        print("Getted pack len " + str(packLenI))
        jsonMessage = self.GetForCount(packLenI)
        if self.cipher is not None:
            print("Message before decrypting " + str(bytes(jsonMessage)))
            helper.SetE(str(bytes(jsonMessage)))
            jsonMessage = self.cipher.CryptDectypt(jsonMessage)
            helper.SetB(jsonMessage.decode())
            print ("Message after decrypting " + jsonMessage.decode())
        print(jsonMessage.decode())
        return jsonMessage.decode()
    
    def GetBytes(self):
        print("Json getting started")
        packLen = self.GetForCount(4)
        if self.cipher is not None:
            packLen = self.cipher.CryptDectypt(packLen)
        print("data received")
        packLenI = int.from_bytes(packLen, byteorder= 'big', signed= False)
        print("Getted pack len " + str(packLenI))
        bytes_message = self.GetForCount(packLenI)
        if self.cipher is not None:
            bytes_message = self.cipher.CryptDectypt(bytes_message)
        return bytes(bytes_message)
        