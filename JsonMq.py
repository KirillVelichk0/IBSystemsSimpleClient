import struct
import socket
class JsonMq:
    def __init__(self) -> None:
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 2001
        self.sockConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockConn.connect((HOST, PORT))
        #self.sockConn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.maxLenMessageConst = 100000
        self.unprocessed_bytes = bytearray()
        
        
    def Send(self, jsonMessage) -> str:
        if len(jsonMessage) > self.maxLenMessageConst :
            return 'Too big input'
        jsonBinary = jsonMessage.encode()
        jsonLenBuffer = struct.pack("!L", len(jsonBinary))
        print("len " + str(len(jsonBinary)))
        self.sockConn.sendall(jsonLenBuffer)
        print(jsonBinary)
        self.sockConn.sendall(jsonBinary)
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
        print("data received")
        packLenI = int.from_bytes(packLen, byteorder= 'big', signed= False)
        print("Getted pack len " + str(packLenI))
        jsonMessage = self.GetForCount(packLenI)
        print(jsonMessage.decode())
        return jsonMessage.decode()
        