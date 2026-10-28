import re, sys, os, struct, time

if len(sys.argv) < 2:
    print("Usage: python clean_exe.py <target.exe>")
    sys.exit(1)

TARGET = sys.argv[1]

with open(TARGET, "rb") as f:
    data = bytearray(f.read())

patterns = [b"Nuitka", b"nuitka", b"NUITKA", b"__compiled__", b"__nuitka"]

for p in patterns:
    idx = 0
    while True:
        pos = data.find(p, idx)
        if pos == -1: break
        data[pos:pos+len(p)] = b'\x00' * len(p)
        idx = pos + len(p)

pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
ts_offset  = pe_offset + 8
new_ts     = int(time.time()) - 60 * 60 * 24 * 30
struct.pack_into("<I", data, ts_offset, new_ts)

out = TARGET.replace(".exe", "_clean.exe")
with open(out, "wb") as f:
    f.write(data)

print(f"[+] Saved clean binary: {out}")
