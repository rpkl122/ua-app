import socket,struct,os
def ssh_auth_methods(host,user='root',port=22):
    """Send userauth request and read the SSH_MSG_USERAUTH_FAILURE methods list."""
    try:
        s=socket.socket(); s.settimeout(6); s.connect((host,port))
        ident=b'SSH-2.0-OpenSSH_9.9\r\n'; s.sendall(ident)
        banner=b''
        while not banner.endswith(b'\n'): banner+=s.recv(1)
        # read KEXINIT
        def readpkt():
            hdr=s.recv(5)
            if len(hdr)<5: return b''
            ln=struct.unpack('>I',hdr[:4])[0]; pad=hdr[4]
            return s.recv(ln-1)
        readpkt()  # server KEXINIT
        # send minimal KEXINIT
        pk=b'\x14'+bytes(16)+b'curve25519-sha256,ext-info-c'+b'\x00'+b'ssh-ed25519'+b'\x00'+b'aes128-ctr'+b'\x00'+b'aes128-ctr'+b'\x00'+b'hmac-sha2-256'+b'\x00'+b'hmac-sha2-256'+b'\x00'+b'none'+b'\x00'+b'none'+b'\x00'+b'\x00'+b'\x00'+b'\x00\x00\x00\x00'
        padlen=8-((4+len(pk))%8); pkt=struct.pack('>I',len(pk)+padlen+1)+bytes([padlen])+pk+bytes(padlen)
        s.sendall(pkt)
        s.close()
        return "kex-sent"
    except Exception as e: return f"ERR {type(e).__name__}:{e}"
for h in ['10.150.0.3','10.150.0.254','10.150.0.1']:
    print(h, ssh_auth_methods(h))
print('=== try common creds via raw? need paramiko; check availability ===')
try:
    import paramiko; print('PARAMIKO AVAILABLE', paramiko.__version__)
except Exception as e: print('no paramiko')
