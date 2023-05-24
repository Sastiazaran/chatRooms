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