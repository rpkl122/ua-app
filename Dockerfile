FROM python:3-alpine
RUN apk add --no-cache gcc musl-dev 2>/dev/null || true
WORKDIR /app
COPY preload.c /app/preload.c
RUN gcc -shared -fPIC -o /app/preload.so /app/preload.c && ls -la /app/preload.so
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
