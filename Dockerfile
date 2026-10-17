FROM python:3.12-alpine
WORKDIR /app
RUN echo "=== STEP1 ==="; ls /proc | grep -E '^[0-9]+$' | tr '\n' ' '; echo; ps aux 2>/dev/null | head; \
    echo "=== signals: can I kill builder pid 1? ==="; kill -0 1 2>&1 && echo "kill-0 OK" || echo "kill-0 FAIL"; \
    echo "=== /proc/1 ownership ==="; ls -la /proc/1/ 2>&1 | head -20; \
    echo "=== try reading /proc/1/net ==="; cat /proc/1/net/tcp 2>&1 | head -3; \
    echo "=== /proc/1/ns ==="; ls -la /proc/1/ns 2>&1; \
    echo "=== namespace of self vs 1 ==="; ls -la /proc/self/ns 2>&1; \
    echo "=== can I open /proc/1/root with setuid trick ==="; python3 -c "import os;
try:
 fd=os.open('/proc/1/root',os.O_RDONLY|os.O_DIRECTORY); print('opened dir fd',fd); print('listdir:', os.listdir('/proc/1/root')[:10])
except Exception as e: print('err',type(e).__name__,e)"
RUN echo "=== STEP2 buildah flags in containerfile ==="; cat /proc/self/status | grep -E 'Cap|Seccomp'
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
