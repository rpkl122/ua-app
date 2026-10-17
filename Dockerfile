FROM python:3.12-slim
RUN echo cachebust-$(date +%s) > /tmp/cb
WORKDIR /app
COPY apitest.py /app/apitest.py
RUN (python3 /app/apitest.py > /app/v36.txt 2>&1; true)
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
