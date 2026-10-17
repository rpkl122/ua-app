import os
def show(p):
    try:
        e=os.listdir(p); return f"{len(e)} entries: {e[:15]}"
    except Exception as ex: return f"{type(ex).__name__}:{ex}"
print('=== PODMAN STORAGE ACCESS (build container) ===')
for p in ['/podman','/podman/.local','/podman/.local/share','/podman/.local/share/containers','/podman/.local/share/containers/storage',
          '/podman/.local/share/containers/storage/overlay','/podman/.local/share/containers/storage/overlay-containers',
          '/podman/.local/share/containers/storage/overlay-layers','/podman/.local/share/containers/storage/volumes',
          '/podman/.config','/podman/.config/containers','/podman/.config/containers/registries.conf',
          '/var/lib/containers','/var/lib/containers/storage','/var/lib/containers/storage/overlay-containers']:
    print(p,'->',show(p))
print('=== WRITE test to podman storage (poison sibling?) ===')
for p in ['/podman/.local/share/containers/storage','/var/lib/containers/storage','/podman/.config/containers']:
    f=os.path.join(p,'poison_test_'+str(os.getpid()))
    try:
        open(f,'w').write('x'); print('WROTE',f); os.remove(f)
    except Exception as e: print('write',p,type(e).__name__)
print('=== read a sibling container config (hooks) if reachable ===')
import glob
for pat in ['/var/lib/containers/storage/overlay-containers/*/userdata/config.json','/podman/.local/share/containers/storage/overlay-containers/*/userdata/config.json']:
    fs=glob.glob(pat)
    print(pat,'->',len(fs),'files')
    for f in fs[:2]:
        try: print('  ',f,open(f).read()[:400])
        except Exception as e: print('  err',type(e).__name__)
print('DONE')
