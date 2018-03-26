import socket
import sys
import os
import time

def find(str, ch): #encontra um char especifico no meio de uma string
    indice = 0
    while indice < len(str):
        if str[indice] == ch:
            return indice
        indice = indice + 1
    return -1

def tempo(): #transforma o minuto e segundo atual em um numero para contagem de tempo
	tmp = time.asctime(time.localtime(time.time()))
	min = tmp[14] + tmp[15]
	min = int(min)
	min = min*60
	seg = tmp[17] + tmp[18]
	seg = int(seg)
	seg = min + seg
	return seg

def hostisup(ip):
	return True if os.system("ping -c 1 " + ip + " > /dev/null") is 0 else False
	#HOST_UP  = True if os.system("ping -c 1 " + ip + " > /dev/null") is 0 else False
	#if HOST_UP == True:
	#	print "Host: ",ip," is up!"

def porttry(ip, port): #abre o socket, tenta conectar, pega o banner, fecha e retorna o banner
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET, socket.SOCK_STREAM
	s.settimeout(0.5)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		s.connect((ip, port))
		s.send("HEAD / HTTP/1.0\r\n\r\n")
		banner = s.recv(1024)
		s.close()
		return True, str(banner)
	except:
		return None, str(0)
def parser(args): #parser de entrada
	if len(args) < 3:
		print("Erro! ")
		print("Uso correto: $ python meuPS.py <IP> <PORTA>")
		exit()
	ip = args[1]
	if find(ip, '-') != -1:
		fin = 1
		ipS = ip.split(".")
		ip1,ip2 = ipS[3].split("-")
		ip = ipS[0]+'.'+ipS[1]+'.'+ipS[2]
		ip1 = int(ip1)
		ip2 = int(ip2)
	else:
		fin = 0
	ports = args[2]
	if find(ports, '-') != -1:
		p1,p2 = ports.split("-")
		p1 = int(p1)
		p2 = int(p2)
		if fin == 0:
			return 1,p1,p2,ip #retorna um vetor [1,p1,p2,ip]
		else:
			return 2,p1,p2,ip,ip1,ip2
	else:
		p = int(ports)
		if fin == 0:
			return 3,p,ip
		else:
			return 4,p,ip,ip1,ip2


opt = parser(sys.argv)
op =[]
print ("Scanning...")
if opt[0] == 1: #opt1 eh o caso em que ha range de portas e um ip
	segA = tempo() #mede o tempo antes
	if hostisup(opt[3]):
		print "Host: ",opt[3]," is up!"
		for port in range(opt[1], opt[2]+1):
			deu,banner = porttry(opt[3], port)
			if deu == None:
				#print ("Port %d closed" % port)
				continue
			else:
				#print "Host: ",opt[3]," is up!"
				print("Port %d opened" % port)
				op.append(port)
				print "Service: ",banner
	segD = tempo() #mede o tempo depois
elif opt[0] == 2: #opt1 eh o caso em que ha range de portas e um range de ips
        segA = tempo() #mede o tempo antes
	for i in range(opt[4], opt[5]+1):
		ip = opt[3] + '.' + str(i)
		if hostisup(ip):
			print "Host: ", ip," is up!"
			for port in range(opt[1], opt[2]+1):
				#ip = opt[3] + '.' + str(i)
				deu,banner = porttry(ip, port)
		        	if deu == None:
		                	#print ("Port %d closed" % port)
		                	continue
		        	else:
					#print "Host: ",ip," is up!"
		                	print("Port %d opened" % port)
		                	op.append(port)
		                	print "Service: ",banner
        segD = tempo() #mede o tempo depois
elif opt[0] == 3: #opt3 eh o caso de so haver uma porta e um ip
	segA = tempo() #mede o tempo antes
	#print "Host: ",opt[2]
	if hostisup(opt[2]):
		print "Host: ",opt[2]," is up!"
		deu,banner = porttry(opt[2], opt[1])
		if deu == True:
			#print "Host: ",opt[2]," is up!"
			print("Port %d opened" % opt[1])
			op.append(opt[1])
			print "Service: ",banner
	segD = tempo() #mede o tempo depois
elif opt[0] == 4: #opt4 eh o caso de so haver uma porta e um range de ips
	segA = tempo() #mede o tempo antes
	for i in range(opt[3],opt[4]+1):
		ip = opt[2] + '.' + str(i)
		if hostisup(ip):
			print "Host: ",ip," is up!"
			deu,banner = porttry(ip, opt[1])
			if deu == True:
				#print "Host: ",ip," is up!"
				print("Port %d opened" % opt[1])
				op.append(opt[1])
				print "Service: ",banner
			else:
				continue
	segD = tempo() #mede o tempo depois

demorou = segD - segA #calcula diferenca

#print ("Opened ports: "), op
print ("Demorou %ds" % demorou)


