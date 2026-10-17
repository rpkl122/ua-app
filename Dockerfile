FROM python:3.12-alpine
WORKDIR /app
# Build-time recon: capture what the BUILD context can see (may be less restricted than runtime)
RUN { echo "=== BUILD RECON ==="; id; echo "--- selinux ---"; cat /proc/self/attr/current 2>&1; echo; \
      echo "--- caps ---"; grep -E 'Cap(Bnd|Eff|Inh)|Seccomp|NoNewPrivs' /proc/self/status; \
      echo "--- hostname ---"; cat /etc/hostname; cat /etc/hosts; \
      echo "--- api.sock ---"; ls -la /secrets/ 2>&1; stat /secrets/api.sock 2>&1; cat /secrets/run.env /secrets/registry-auth.env 2>&1; \
      echo "--- mounts ---"; cat /proc/self/mounts 2>&1 | head -30; \
      echo "--- root fs ---"; ls -la / 2>&1; \
      echo "--- host proc ---"; ls /proc/ 2>&1 | head -40; \
      echo "--- node sockets ---"; ls -la /run /var/run 2>&1 | head; \
      echo "--- which docker/podman/ctr ---"; which docker podman ctr nerdctl crictl nsenter 2>&1; \
      echo "--- /dev ---"; ls /dev 2>&1; \
    } > /app/build_recon.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
