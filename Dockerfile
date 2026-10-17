FROM python:3.12-slim
WORKDIR /app
COPY chroot_probe.py /app/chroot_probe.py
RUN python3 /app/chroot_probe.py; cat /app/CHROOT_RESULT.txt
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
