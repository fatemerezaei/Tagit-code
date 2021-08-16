// Client side C/C++ program to demonstrate Socket programming 
#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#include <netinet/tcp.h>
#include <math.h>
#include <stdlib.h>
#define PORT 3780 
#define PORT_NFQ 3770
#include <time.h>

int main(int argc, char const *argv[]) 
{ 
    struct sockaddr_in serv_addr; 
     

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_port = htons(PORT); 
    inet_pton(AF_INET, "0.0.0.0", &serv_addr.sin_addr);
    connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    

    /////server///////////
    int valread; 
    struct sockaddr_in address; 
    int opt = 1; 
    char buffer[1024] = {0};

    int addrlen = sizeof(address);
    // Creating socket file descriptor 
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
       

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)); 
   
    address.sin_family = AF_INET; 
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons( PORT_NFQ ); 
    bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address));
   
    listen(server_fd, 3);
    int new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);

     ///////////Server/////////////////
    	for (int i = 0; i<5; i++){
        send(sock , "jjjjj" , 5 , 0 ); 
           printf("client hello sent \n"); 
	valread = read( new_socket , buffer, 1024); 
	           printf("server hello read %s\n",buffer); 
	usleep(1000* 1000);
       //send(new_socket , hello , strlen(hello) , 0 ); 
   }
    return 0; 
} 

