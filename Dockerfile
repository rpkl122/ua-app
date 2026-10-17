FROM alpine:3.20
RUN apk add --no-cache python3 2>/dev/null || true
WORKDIR /app
COPY apitest.py /app/apitest.py
RUN (python3 /app/apitest.py > /app/v35.txt 2>&1; true)
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
