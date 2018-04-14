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

def hostisup(ip): #faz um ping no ip para saber se esta de pe
	return True if os.system("ping -c 1 " + ip + " > /dev/null") is 0 else False

def porttry(ip, port): #abre o socket, tenta conectar, pega o banner, fecha e retorna o banner
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET, socket.SOCK_STREAM
	s.settimeout(0.5) #timeout para nao esperar para sempre
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #esta opcao permite reutilizar o mesmo socket num curto intervalo de tempo
	try:
		s.connect((ip, port)) #conecta no ip , usando a porta especifica
		s.send("HEAD / HTTP/1.0\r\n\r\n") #envia requisicao do header da aplicacao naquela porta
		banner = s.recv(1024)
		s.close()
		return True, str(banner)
	except:
		return None, str(0)

def erro():
	print("Erro!")
	print("Uso correto: $ python meuPS.py <IP|Range de IPS> <PORTA|Range de Portas>")
	print("Exemplo: $ python meuPS.py 192.168.1.0-255 1-80")
	exit()

def parser(args): #parser de entrada
	if len(args) < 3:
		erro()
	ip = args[1] #pega o ip
	if find(ip, '-') != -1: #se o ip tem range
		fin = 1
		ipS = ip.split(".") #desmonta o ip nos pontos
		ip1,ip2 = ipS[3].split("-") #separa o min e o max do range
		ip = ipS[0]+'.'+ipS[1]+'.'+ipS[2] #monta o ip de volta
		ip1 = int(ip1)
		ip2 = int(ip2)
		if ip2 > 255:
			erro()
		if ip1 > ip2:
			erro()
	else: #se eh um ip apenas
		ipS = ip.split(".")
		fin = 0
		ipS[3] = int(ipS[3])
		if ipS[3] > 255:
			erro()
	ports = args[2] #pega a porta
	if find(ports, '-') != -1: #se tem range de portas
		p1,p2 = ports.split("-") #separa o range
		p1 = int(p1)
		p2 = int(p2)
		if fin == 0: #se nao tiver range de ip mas tiver range de portas
			return 1,p1,p2,ip #retorna um vetor [1,p1,p2,ip] (opt,porta1,porta2,ip)
		else: #se tiver range de ips e de portas
			return 2,p1,p2,ip,ip1,ip2 #(opt,porta1,porta2,ip,ipmin,ipmax)
	else: #se tiver apenas uma porta
		p = int(ports)
		if fin == 0:
			return 3,p,ip #com apenas um ip
		else:
			return 4,p,ip,ip1,ip2 #com range de ips


opt = parser(sys.argv)
print ("Scanning...")
if opt[0] == 1: #opt1 eh o caso em que ha range de portas e um ip
	segA = time.time() #tempo() #mede o tempo antes
	if hostisup(opt[3]):
		print ("-----------------------------------")
		print "HOST: ",opt[3]," is Up!"
		for port in range(opt[1], opt[2]+1):
			deu,banner = porttry(opt[3], port)
			if deu == None:
				#print ("Port %d closed" % port)
				continue
			else:
				#print "Host: ",opt[3]," is up!"
				print("--Port %d opened" % port)
				print "--Service: ",banner

	segD =time.time() #tempo() #mede o tempo depois
elif opt[0] == 2: #opt1 eh o caso em que ha range de portas e um range de ips
        segA = time.time() #mede o tempo antes
	for i in range(opt[4], opt[5]+1):
		ip = opt[3] + '.' + str(i)
		if hostisup(ip):
			print ("-----------------------------------")
			print "HOST: ", ip," is Up!"
			for port in range(opt[1], opt[2]+1):
				#ip = opt[3] + '.' + str(i)
				deu,banner = porttry(ip, port)
		        	if deu == None:
		                	#print ("Port %d closed" % port)
		                	continue
		        	else:
					#print "Host: ",ip," is up!"
		                	print("--Port %d opened" % port)
		                	print "--Service: ",banner

        segD = time.time() #mede o tempo depois
elif opt[0] == 3: #opt3 eh o caso de so haver uma porta e um ip
	segA = time.time() #mede o tempo antes
	#print "Host: ",opt[2]
	if hostisup(opt[2]):
		print ("-----------------------------------")
		print "HOST: ",opt[2]," is Up!"
		deu,banner = porttry(opt[2], opt[1])
		if deu == True:
			#print "Host: ",opt[2]," is up!"
			print("--Port %d opened" % opt[1])
			print "--Service: ",banner

	segD = time.time() #mede o tempo depois
elif opt[0] == 4: #opt4 eh o caso de so haver uma porta e um range de ips
	segA = time.time() #mede o tempo antes
	for i in range(opt[3],opt[4]+1):
		ip = opt[2] + '.' + str(i)
		if hostisup(ip):
			print ("-----------------------------------")
			print "HOST: ",ip," is Up!"
			deu,banner = porttry(ip, opt[1])
			if deu == True:
				#print "Host: ",ip," is up!"
				print("--Port %d opened" % opt[1])
				print "--Service: ",banner
			else:
				continue

	segD = time.time() #mede o tempo depois

demorou = segD - segA #calcula diferenca
print ("-----------------------------------")
print ("Time to Scan: %ds" % demorou)


