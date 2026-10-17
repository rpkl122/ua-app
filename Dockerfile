FROM python:3.12-alpine
WORKDIR /app
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
