FROM python:3.12-alpine
WORKDIR /app
COPY regcheck.py /app/regcheck.py
RUN python3 /app/regcheck.py > /app/v24.txt 2>&1 || true
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
