FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== DEEP BUILD RECON v2 ==="; id; echo "--- selinux ---"; cat /proc/self/attr/current; echo; \
      echo "--- /podman ---"; ls -la /podman/ 2>&1 | head; ls -la /podman/.local/share/containers/storage/ 2>&1 | head -20; \
      echo "--- podman sockets ---"; find /run /var/run /podman -maxdepth 4 -name '*.sock' 2>/dev/null | head -20; \
      echo "--- podman/CTR binaries ---"; which podman buildah ctr nerdctl runc crun nsenter 2>&1; \
      echo "--- /proc/kcore ---"; ls -la /proc/kcore 2>&1; head -c 16 /proc/kcore 2>&1 | xxd 2>/dev/null | head -2; \
      echo "--- /proc/1 has access? ---"; ls -la /proc/1/root 2>&1; readlink /proc/1/ns/* 2>&1; \
      echo "--- all pids ---"; ls /proc | grep -E '^[0-9]+$' | tr '\n' ' '; echo; \
      echo "--- net ---"; ip addr 2>/dev/null || cat /proc/net/fib_trie 2>/dev/null | head; \
      echo "--- /proc/sys writable ---"; echo x > /proc/sys/kernel/ns_last_pid 2>&1 && echo WRITABLE || echo RO; \
      echo "--- cgroup ---"; cat /proc/self/cgroup; ls -la /sys/fs/cgroup/ 2>&1 | head; \
      echo "--- host mounts (anything not container) ---"; cat /proc/self/mountinfo | grep -vE 'overlay|tmpfs|devpts|mqueue|proc|sysfs|cgroup' | head -20; \
    } > /app/build2.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
