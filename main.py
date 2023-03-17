import tkinter as tk
import json
import hashlib
import base64
import JsonMq
jsonMqService = JsonMq.JsonMq()
maxLenMessageConst = 100000

def strUrlEncode(strData: str):
    return base64.urlsafe_b64encode(strData.encode()).decode()

def strUrlDecode(strData: str):
    return base64.urlsafe_b64decode(strData.encode()).decode()
    
def send_registration_data():
    if len(login.get()) == 0 or len(password.get()) == 0 :
        label['text'] = 'Please enter data'
        return
    jsonMessage = json.dumps({"Type": "RegistrationRequest","username": strUrlEncode(login.get()) , "password":strUrlEncode(password.get())})
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
    shaObj = hashlib.sha256()
    shaObj.update(keyWord)
    shaObj.update(hash1Round)
    hash2Round = shaObj.digest()
    hashEncoded = base64.urlsafe_b64encode(hash2Round)
    jsonMessage = json.dumps({"Type": "GetAuthResult","username":strUrlEncode(login.get()), "hash":hashEncoded.decode()})
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