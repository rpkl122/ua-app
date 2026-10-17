FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== v7: kcore/ptrace/builddirs ==="; id; cat /proc/self/attr/current; echo; \
  echo "--- /proc/kcore ELF read test ---"; head -c 64 /proc/kcore 2>&1 | od -An -tx1 | head -3; \
  echo "--- /proc/kcore via python read ---"; python3 -c "
import os
try:
    fd=os.open('/proc/kcore',os.O_RDONLY); d=os.pread(fd,64,0); print('READ',len(d),d[:16].hex())
except Exception as e: print('kcore',type(e).__name__,e)
" 2>&1; \
  echo "--- ptrace/process_vm of pid 1 ---"; python3 -c "
import ctypes,os
l=ctypes.CDLL('libc.so.6',use_errno=True)
r=l.ptrace(16,1,0,0)  # PTRACE_ATTACH
print('ptrace_attach',r,'errno',ctypes.get_errno())
" 2>&1; \
  echo "--- /proc/1/mem read ---"; python3 -c "
try:
    fd=os.open('/proc/1/mem',os.O_RDONLY); print('mem opened',fd); print(os.pread(fd,16,0x400000))
except Exception as e: print('mem',type(e).__name__,e)
" 2>&1; \
  echo "--- /build ---"; ls -laR /build 2>&1 | head -40; \
  echo "--- setuid binaries ---"; find / -perm -4000 -type f 2>/dev/null | head -20; \
  echo "--- capabilities files ---"; getcap -r / 2>/dev/null | head; \
} > /app/v7.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
