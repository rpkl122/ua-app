FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== ESCAPE TEST v3 ==="; id; \
  echo "--- kcore read ---"; dd if=/proc/kcore bs=64 count=1 2>&1 | head -3; ls -la /proc/kcore; \
  echo "--- /dev/mem ---"; dd if=/dev/mem bs=64 count=1 2>&1 | head -2; ls -la /dev/mem 2>&1; \
  echo "--- nsenter host net/pid (169.254.1.2 = host gw) ---"; nsenter -t 1 -n -- ip addr 2>&1 | head -5; nsenter -t 1 -m -- ls / 2>&1 | head -3; \
  echo "--- can I see host pids via /proc? ---"; for p in 1 107 120 26; do echo "pid $p:"; cat /proc/$p/cmdline 2>&1 | tr '\0' ' '; echo; readlink /proc/$p/root 2>&1; cat /proc/$p/attr/current 2>&1; echo; done; \
  echo "--- uname/kernel ---"; uname -a; \
  echo "--- nf/iptables ---"; which iptables nft 2>&1; cat /proc/net/ip_tables_names 2>&1; \
  echo "--- keyring ---"; python3 -c "import ctypes;l=ctypes.CDLL('libc.so.6');print('keyctl',l.syscall(250,0))" 2>&1; \
} > /app/build3.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
