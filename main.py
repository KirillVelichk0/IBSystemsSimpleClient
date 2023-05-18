import sys, os
lib_path = os.path.abspath(os.path.join(__file__, '..', 'cppGenerator'))
sys.path.append(lib_path)
from cppGenerator.caller import Generator as CppGen


import tkinter as tk
import json
import hashlib
import base64
import JsonMq
import random
import numpy as np
from DiffiHelman import DiffieHelm
jsonMqService = JsonMq.JsonMq()
jsonMqService.SecureChannel()
maxLenMessageConst = 100000

def GetBase():
    return (115, 2003000168)

def GenSecretKey()->int:
    return random.randint(1000, 2000000000)

def GenPreKey(myKey: int, a, p)->int:
    return pow(a, myKey, p)

def GenFinalKey(anotherKey: int, mySecret: int, p) -> int:
    return pow(anotherKey, mySecret, p)


def DiffiHelman():
    helm = DiffieHelm()
    helm.generate_parameters_client()
    secret = helm.a
    a = helm.g
    p = helm.p
    pre_key = GenPreKey(secret, a, p)
    print("A " + str(a))
    print("P " + str(p))
    print("secret " + str(secret))
    print("pre_key " + str(pre_key))
    jsonToSend = json.dumps({
        'Type': 'Helman',
        'Key': pre_key,
        'A': a,
        'P': p
    })
    jsonMqService.Send(jsonToSend)
    responseJson = json.loads(jsonMqService.Get())
    server_key = int(responseJson['Key'])
    print('ServerKey ' + str(server_key))
    final = GenFinalKey(server_key, secret, p)
    print(final)
    return final



class Rc4:
    def __init__(self, seed: int):
        self.gen = CppGen()
        self.gen.SetSeed(seed)

    def CryptDectypt(self, data: bytes):
        finalBytes = bytearray()
        for i in range(0, len(data)):
            curByte = data[i: i+1]
            r8b = self.gen.TryGen()
            helpByte = bytearray()
            helpByte.append(r8b)
            helpByte = bytes(helpByte)
            print(r8b)
            curByte = bytes(a ^ b for (a, b) in zip(curByte, helpByte))
            curByte = curByte[0]
            finalBytes.append(curByte)
        return bytes(finalBytes)



jsonMqService.cipher = Rc4(DiffiHelman())


def strUrlEncode(strData: str):
    return base64.urlsafe_b64encode(strData.encode()).decode()

def strUrlDecode(strData: str):
    return base64.urlsafe_b64decode(strData.encode()).decode()
    
def send_registration_data():
    if len(login.get()) == 0 or len(password.get()) == 0 :
        label['text'] = 'Please enter data'
        return
    jsonMessage = json.dumps({"Type": "RegistrationRequest",
                              "username": strUrlEncode(login.get()) , "password":strUrlEncode(password.get())})
    print(jsonMessage)
    result = jsonMqService.Send(jsonMessage)
    label['text'] = result

def send_auth_data():
    if len(login.get()) == 0 or len(password.get()) == 0 :
        label['text'] = 'Please enter data'
        return
    jsonMessage = json.dumps({"Type": "GetKeyWordRequest","username":strUrlEncode(login.get())})
    jsonMqService.Send(jsonMessage)
    print("Json sended")
    try:
        gettedJson = jsonMqService.Get()
        print(gettedJson)
    except:
        print("Cant get")
        return
    try:
        keyWordJson = json.loads(gettedJson)
        print("keyWordJson " + str(keyWordJson))
    except:
        print("Not json")
        return
    keyWord = base64.urlsafe_b64decode(str(keyWordJson["KeyWord"]))
    shaObj = hashlib.sha256()
    shaObj.update(password.get().encode())
    hash1Round = shaObj.digest()
    print(hash1Round)
    shaObj = hashlib.sha256()
    shaObj.update(keyWord)
    shaObj.update(hash1Round)
    hash2Round = shaObj.digest()
    print(hash2Round)
    hashEncoded = base64.urlsafe_b64encode(hash2Round)
    jsonMessage = json.dumps({"Type": "GetAuthResult","username":strUrlEncode(login.get()), "hash":hashEncoded.decode()})
    print(jsonMessage)
    jsonMqService.Send(jsonMessage)
    try:
        authResult = json.loads(jsonMqService.Get())
    except:
        print("Not json")
        return
    print("Auth result " + str(authResult["Answer"]))
    #label['text'] = result
root = tk.Tk()
root.title("Best app")
root.geometry("500x500") 
login = tk.Entry()
login.pack(anchor=tk.NW, padx=6, pady=6)
password = tk.Entry()
password.pack(anchor=tk.NW, padx=6, pady=6)
btnR = tk.Button(text="Registrate", command=send_registration_data)
btnR.pack(anchor=tk.NW, padx=6, pady=6)
btnA = tk.Button(text="Authentificate", command=send_auth_data)
btnA.pack(anchor=tk.NW, padx=6, pady=6)
label = tk.Label()
label.pack(anchor=tk.NW, padx=6, pady=6)
  
root.mainloop()