#coding:utf_8
import socket

class useUdp:
	def __init__(self,str="kaigi"):
		if str is "of":
			self.host = "127.0.0.1"
			self.port = 1230
		elif str is "kaigi":
			self.host = "127.0.0.1"
			self.port = 1230
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.connect((self.host,self.port))
		
	def sendData(self,data):
		self.sock.sendto(data,(self.host, self.port))
		
	def closeSocket(self):
		self.sock.close()
		
if __name__ == "__main__":
    sock = useUdp("of")
    sock.sendData(play)
    sock.closeSocket()