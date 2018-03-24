#!/usr/bin/python  
import socket  
import sys  
import os  
#grab the banner  
def grab_banner(ip_address,port):  
	try:
		s=socket.socket()  
		s.connect((ip_address,port))  
		banner = s.recv(1024)  
		print ip_address + ':' + banner  
	except:
		return

def main():
	portList = [21,22,25,80,110]  
	#for x in range(0,255):  
	for port in portList:  
		ip_address = sys.argv[1]
		#ip_address = '192.168.0.' + str(x)  
		grab_banner(ip_address,port)  
if __name__ == '__main__':  
	main() 
