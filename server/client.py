# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server
username = ""
token = ""

def xor(a,b):
    q = a ^ b
    return q

def cifrar(palabra):
  llave = 'K'
  result = ""
  for i in range(len(palabra)):
    #print(ord(palabra[i]))
    letra = palabra[i]
    result+=chr((xor(ord(letra), ord(llave))))
  return result

def auth(s):
  global username
  print("Ingrese sus datos")
  print("Username:")
  user = input()
  print("Password:")
  password = input()
  
  msg = "auth|"
  msg = user + "|" + password + "\0"
  msg = cifrar(msg)

  print("Enviando: %s " %(msg))
  s.send(msg.encode())

  data = s.recv(1024)
  data = cifrar(data.decode())

  if "Denied" in data:
    user = ""
    return 0
  else:   
    username = user 
    return data #return token on data
  
def group(s):
  global username
  print("Ingrese el nombre del grupo:")
  groupName = input()
  msg = "creargrupo|"
  msg += username + "|" + groupName + "\0"
  print("Enviando: %s " %(msg))
  msg = cifrar(msg)
  s.send(msg.encode())

  data = s.recv(1024)
  data = cifrar(data.decode())
  print(data)
  

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  '''
  print("Username:")
  user = input()
  print("Password:")
  password = input()

  message = "auth|"
  message += user + "|" + password + "\0"
  message = cifrar(message)
  print("Enviando: %s " %(message))
  s.send(message.encode())
  
  data = s.recv(1024)
  data = cifrar(data.decode())
  print("Access " + data)
  '''

  #'''
  loop = True
  while loop:
    if token == "":
      token = auth(s)
      print(token)
      if token == 0:
        token = ""
    else:
      group(s)
      loop = False
      
  '''
    print("Username:")
    user = input()
    print("Password:")
    password = input()

    ##Cifrador de mensaje
    cifrado = []
    size = 0
    print("Ingresa la palabra a cifrar: ")
    #Minimo de 24 caracteres
    palabra = input()
    size = len(palabra)

    cifrar(palabra, 'K')
    mensaje=''.join([chr(i) for i in cifrado])
    print(mensaje)
    cifrado.clear()

    message = user+"|"+password+"|"+mensaje+"\0"
    print("Enviando: %s " %(message))
    s.send(message.encode())
  
    data = s.recv(1024)
    '''
    #'''

#print(f"Received {data!r}")
#print("Access %s " %(data.decode()))