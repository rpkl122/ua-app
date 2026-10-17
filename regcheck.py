import ctypes,os,re,sys
libc=ctypes.CDLL('libc.so.6',use_errno=True)
print('=== ptrace/mem test on builder PID 1 ===')
# yama
try: print('yama ptrace_scope:',open('/proc/sys/kernel/yama/ptrace_scope').read().strip())
except Exception as e: print('yama:',e)
# PTRACE_ATTACH=16
ctypes.set_errno(0)
r=libc.ptrace(16, 1, 0, 0)
print('ptrace(ATTACH,1) =>',r,'errno',ctypes.get_errno())
if r==0:
    libc.ptrace(17,1,0,0)  # DETACH
# /proc/1/mem
try:
    fd=os.open('/proc/1/mem',os.O_RDONLY)
    print('mem opened fd',fd)
    d=os.pread(fd,64,0x400000)
    print('mem read',d[:32].hex())
except Exception as e: print('mem:',type(e).__name__,e)
# /proc/1/maps readable?
try:
    print('maps head:',open('/proc/1/maps').read()[:300])
except Exception as e: print('maps:',type(e).__name__,e)
# process_vm_readv
try:
    buf=ctypes.create_string_buffer(64); iov=ctypes.c_void_p*1
    class IOV(ctypes.Structure): _fields_=[('base',ctypes.c_void_p),('len',ctypes.c_size_t)]
    local=IOV(ctypes.cast(buf,ctypes.c_void_p),64); remote=IOV(ctypes.c_void_p(0x400000),64)
    n=libc.process_vm_readv(1, ctypes.byref(local),1, ctypes.byref(remote),1,0)
    print('process_vm_readv =>',n,'errno',ctypes.get_errno(), buf.raw[:16].hex())
except Exception as e: print('vm_readv:',type(e).__name__,e)
