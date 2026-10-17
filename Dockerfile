FROM python:3-alpine
WORKDIR /app
COPY apitest.py /app/apitest.py
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
