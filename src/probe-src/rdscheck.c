// written by Leif Nixon <nixon@nsc.liu.se>
// exit codes modified for Nagios shake

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>

#ifndef PF_RDS
 #define PF_RDS 28
#endif

int main (int argc, char *argv)
{

       int s;

       s = socket(PF_RDS, SOCK_SEQPACKET, 0);

       if(s < 0) {
               printf("OK: Could not open socket -- module probably blacklisted.\n");
               exit(0);
       }
       printf("ERROR: Socket opened successfully.\n");
       exit(2);
}

