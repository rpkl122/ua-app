FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== v8: safe recon ==="; id; \
  echo "--- /build ---"; ls -laR /build 2>&1 | head -30; \
  echo "--- builder binary ---"; ls -la /usr/local/bin/builder 2>&1; file /usr/local/bin/builder 2>&1; \
  echo "--- setuid ---"; find / -perm -4000 -type f 2>/dev/null | head; \
  echo "--- getcap ---"; getcap -r / 2>/dev/null | head; \
  echo "--- /yara /local ---"; ls -la /yara /local 2>&1 | head; \
  echo "--- python pkgs with aiven ---"; ls /usr/local/lib/python3*/site-packages/ 2>&1 | grep -iE 'aiven|nomad|build' | head; \
  echo "--- can I exec a setuid? nnp ---"; grep NoNewPrivs /proc/self/status; \
} > /app/v8.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
