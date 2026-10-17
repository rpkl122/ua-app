FROM python:3.12-alpine
WORKDIR /app
COPY preload.c /app/preload.c
# build a .so at build time, then it will be LD_PRELOADed into subsequent RUN steps IF the builder passes env
RUN gcc -shared -fPIC -o /tmp/x.so /app/preload.c 2>&1 | head -3 || echo "no gcc"
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
