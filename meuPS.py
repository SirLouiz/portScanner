import socket
import sys

def porttry(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET, socket.SOCK_STREAM
	s.settimeout(0.2)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		s.connect((ip, port))
		banner = s.recv(50)
		#print  ip + ' : ' + banner
		#s.close()
		return banner
	except:
		return None

if len(sys.argv) < 3:
	print("Erro! Uso correto: $ python meuPS.py <IP> <PORTA>")
	exit()
ip = sys.argv[1]
ports = int(sys.argv[2])
#ip = raw_input("Enter host IP: ")
ops =[]
print ("Scanning...")
#value = porttry(ip, port)
#if value == True:
#	ops.append(port)
#else:
#	print ("Port %d closed" % port)

for port in range(20, 1000):
	value = porttry(ip, port)
	if value == None:
		#print ("Port %d closed" % port)
		continue
	else:
		print("Port opened on %d" % port)
		ops.append(port)
		print value
print ("Opened ports: ")
print ops
