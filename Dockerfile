FROM python:3.12-slim
WORKDIR /app
COPY kaslr.py /app/kaslr.py
RUN (python3 /app/kaslr.py > /app/KASLR.txt 2>&1; true)
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
