from socket import *
import datetime

serverSocket = socket(AF_INET, SOCK_STREAM) 

serverPort = 6789
serverSocket.bind(('192.168.29.196',serverPort))
serverSocket.listen(5)

while True:
	print ('Ready to serve...')
	connectionSocket, addr = serverSocket.accept()
	print ("addr:\n", addr)
	try:
		message = connectionSocket.recv(1024)#Fill in start #Fill in end 
		print ("message: \n", message)
		filename = message.split()[1]
		f = open(filename[1:])
		outputdata = f.read() 
		print ("outputdata:", outputdata)
		now = datetime.datetime.now()
		
		first_header = "HTTP/1.1 200 OK"
		
		header_info = {
			"Date": now.strftime("%Y-%m-%d %H:%M"),
			"Content-Length": len(outputdata),
			"Keep-Alive": "timeout=%d,max=%d" %(10,100),
			"Connection": "Keep-Alive",
			"Content-Type": "text/html"
		}
		
		following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
		print ("following_header:", following_header)
		
		connectionSocket.send(b'\nHTTP/1.1 200 OK\n\n')
 		
		for i in range(0, len(outputdata)):
			connectionSocket.send(bytes(outputdata[i],'utf-8'))
		connectionSocket.close()
	except IOError:
		connectionSocket.send(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>404 Not Found<h1></body></html>")
		
		connectionSocket.close()
		
serverSocket.close()