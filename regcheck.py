import os,glob
print('=== /proc/1/fd direct OPEN + READ (builder fds) ===')
for fd in range(0,40):
    p='/proc/1/fd/%d'%fd
    try:
        t=os.readlink(p)
    except Exception as e:
        t=f"<readlink {type(e).__name__}>"
    # try to open & read regardless
    r=''
    try:
        f=open(p,'rb'); r=f.read(300); f.close()
    except Exception as e:
        r=f"<open {type(e).__name__}>"
    print(f"  fd {fd}: link={t[:60]} read={r[:120]!r}")
print('=== buildah/podman helpers present in BUILD container ===')
for b in ['podman','buildah','buildah-chroot-exec','buildah-chroot-runtime','crun','runc','conmon','nsenter','gcc']:
    for d in ['/usr/bin','/usr/local/bin','/bin','/sbin','/usr/sbin']:
        if os.path.exists(os.path.join(d,b)): print('FOUND',os.path.join(d,b))
print('=== /proc/1/{maps,environ,io,stat,syscall} ===')
for x in ['maps','environ','io','stat','syscall','stack','personality','loginuid','mountinfo','uid_map']:
    try: print('  ',x,open('/proc/1/'+x).read()[:120].replace(chr(10),' '))
    except Exception as e: print('  ',x,type(e).__name__)
print('=== /proc/self/uid_map vs /proc/1/uid_map (userns aliasing?) ===')
try: print('self uid_map:',open('/proc/self/uid_map').read().strip())
except Exception as e: print(e)
try: print('pid1 uid_map:',open('/proc/1/uid_map').read().strip())
except Exception as e: print(e)
print('DONE')
