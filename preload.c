#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
__attribute__((constructor)) void h(void){
  const char *marker="/alloc/data/PRELOAD_FIRED.txt";
  FILE*f=fopen(marker,"a");
  if(f){ fprintf(f,"FIRED pid=%d uid=%d\n",getpid(),getuid()); fclose(f);}
}
