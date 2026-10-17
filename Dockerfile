FROM python:3.12-slim
WORKDIR /app
COPY app.py rogue_mysql.py /app/
CMD ["python3", "app.py"]
