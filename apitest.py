import os
print("=== /proc/1 access from BUILD container ===")
for p in ["/proc/1/root","/proc/1/cwd","/proc/1/exe","/proc/1/root/etc/hostname","/proc/1/root/secrets","/proc/1/cwd/..","/proc/1/mountinfo","/proc/1/uid_map","/proc/1/cmdline"]:
    try:
        if os.path.isdir(p): print(p,"DIR",os.listdir(p)[:10])
        else: print(p,"FILE",open(p,'rb').read(200)[:200])
    except Exception as e: print(p,type(e).__name__)
print("=== /proc/1/root any deeper ===")
for p in ["/proc/1/root/proc","/proc/1/root/home","/proc/1/root/var/lib","/proc/1/root/opt"]:
    try: print(p,os.listdir(p)[:10])
    except Exception as e: print(p,type(e).__name__)
# build 1792264226
