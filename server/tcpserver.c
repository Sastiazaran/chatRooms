/*

   Lectura remota de una palabra para devolver el numero de vocales usando sockets pertenecientes
   a la familia TCP, en modo conexion.
   Codigo del servidor

   Nombre Archivo: tcpserver.c
   Archivos relacionados: num_vocales.h tcpclient.c 
   Fecha: Febrero 2023

   Compilacion: cc tcpserver.c -lnsl -o tcpserver
   Ejecución: ./tcpserver
*/

#include <stdio.h>
/* The following headers was required in old or some compilers*/
//#include <sys/types.h>
//#include <sys/socket.h>
//#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>	// it is required to call signal handler functions
#include <unistd.h>  // it is required to close the socket descriptor
#include <stdbool.h>
#include <dirent.h>
#include "authentication.h"
#include "chats.h"
//#include "utilities.h"


#define  DIRSIZE   2048      /* longitud maxima parametro entrada/salida */
#define  PUERTO    5000	     /* numero puerto arbitrario */

int                  sd, sd_actual;  /* descriptores de sockets */
int                  addrlen;        /* longitud direcciones */
struct sockaddr_in   sind, pin;      /* direcciones sockets cliente u servidor */


/*  procedimiento de aborte del servidor, si llega una senal SIGINT */
/* ( <ctrl> <c> ) se cierra el socket y se aborta el programa       */
void aborta_handler(int sig){
   printf("....abortando el proceso servidor %d\n",sig);
   close(sd);  
   close(sd_actual); 
   exit(1);
}


int main(){
  
	char  dir[DIRSIZE];	     /* parametro entrada y salida */

	/*
	When the user presses <Ctrl + C>, the aborta_handler function will be called, 
	and such a message will be printed. 
	Note that the signal function returns SIG_ERR if it is unable to set the 
	signal handler, executing line 54.
	*/	
   if(signal(SIGINT, aborta_handler) == SIG_ERR){
   	perror("Could not set signal handler");
      return 1;
   }
       //signal(SIGINT, aborta);      /* activando la senal SIGINT */

/* obtencion de un socket tipo internet */
	if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		perror("socket");
		exit(1);
	}

/* asignar direcciones en la estructura de direcciones */
	sind.sin_family = AF_INET;
	sind.sin_addr.s_addr = INADDR_ANY;   /* INADDR_ANY=0x000000 = yo mismo */
	sind.sin_port = htons(PUERTO);       /*  convirtiendo a formato red */

/* asociando el socket al numero de puerto */
	if (bind(sd, (struct sockaddr *)&sind, sizeof(sind)) == -1) {
		perror("bind");
		exit(1);
	}

/* ponerse a escuchar a traves del socket */
	if (listen(sd, 5) == -1) {
		perror("listen");
		exit(1);
	}

	int max = 100000;
	pid_t child_pid;
	for (int i = 0; i < max; ++i)
	{
	/* esperando que un cliente solicite un servicio */
		if ((sd_actual = accept(sd, (struct sockaddr *)&pin, &addrlen)) == -1) {
			perror("accept");
			exit(1);
		}

		child_pid = fork();
		if (child_pid==0)
		{
			break; //is child
		} else {
			close(sd_actual); //is parent
		}
	}

	if (child_pid==0)
	{
		bool whil = true;
	while(whil){

	/* tomar un mensaje del cliente */
		if (recv(sd_actual, dir, sizeof(dir), 0) == -1) {
			perror("recv");
			exit(1);
		}

		/*IMPRIME EL MENSAJE A DESCIFRAR*/
		cypher(dir);
		printf("Deciphered: %s\n", dir);

	/* leyendo el directorio */
		//num_vocales(dir);
		int eventInt = event(dir);
		printf("\nEvent:%d\n",eventInt);
		switch(eventInt){
			case 1:
				auth(dir);
				break;
			case 2:
				creargrupo(dir);
				whil = false;
				break;
			case 3:
				getusers(dir);
				break;
			case 4:
				getuserchats(dir);
				break;
			case 5:
				getchats(dir);
				break;
			case 6:
				creargrupo(dir);
				break;
			case 7:
				getadminchats(dir);
				break;
			case 8:
				addUser(dir);
				break;
			case 9:
				deleteUser(dir);
				break;
			case 10:
				getchat(dir);
				break;
			case 11:
				messageSent(dir);
				break;
			case 12:
				registerUser(dir);
				break;
		}
		printf("Sending...: %s\n", dir);
		/* Encriptación mensaje */
		cypher(dir);
		

	/* enviando la respuesta del servicio */
		if ( send(sd_actual, dir, strlen(dir), 0) == -1) {
			perror("send");
			exit(1);
		}
	}

	/* cerrar los dos sockets */
	close(sd_actual);  
	close(sd);
	printf("Conexion cerrada\n");
	} else {
		close(sd);
	}
	return 0;
}
