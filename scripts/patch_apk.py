import argparse
import hashlib
import os
import re
import struct
import subprocess
import time
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ZIPALIGN = r"C:\Users\HeliumMarcos\Documents\Codex\2026-11-07\ana-2\work\android-tools\sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\HeliumMarcos\Documents\Codex\2026-11-07\ana-2\work\android-tools\sdk\build-tools\34.0.0\apksigner.bat"
KEYSTORE = r"C:\Users\HeliumMarcos\.android\debug.keystore"
DEFAULT_APK = Path(r"C:\Users\HeliumMarcos\Documents\ChatGPT\TizenTubeCobalt\work\recovery\TizenTube-L1-arm.apk")

parser = argparse.ArgumentParser(description="Patch TubeRush APK versionName, versionCode, and u.js ref")
parser.add_argument("--version-name", required=True, help="e.g. 2.0.8")
parser.add_argument("--version-code", type=int, required=True, help="e.g. 208")
parser.add_argument("--ref", default="main", help="Git ref for jsDelivr u.js (default: main)")
parser.add_argument("--apk", type=Path, default=DEFAULT_APK)
args = parser.parse_args()

u_bytes = (REPO / "u.js").read_bytes()
sha = hashlib.sha256(u_bytes).hexdigest()

if args.ref == "main":
    try:
        purge_req = urllib.request.Request(
            "https://purge.jsdelivr.net/gh/HeliumMarcos/TubeRush@main/u.js",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        urllib.request.urlopen(purge_req, timeout=15).read()
    except Exception as exc:
        print("Purge warning:", exc)

cdn_url = f"https://cdn.jsdelivr.net/gh/HeliumMarcos/TubeRush@{args.ref}/u.js"
for attempt in range(5):
    req = urllib.request.Request(f"{cdn_url}?v={int(time.time()*1000)}", headers={"User-Agent": "Mozilla/5.0"})
    cdn_b = urllib.request.urlopen(req, timeout=15).read()
    if hashlib.sha256(cdn_b).hexdigest() == sha:
        print(f"CDN @{args.ref} verified:", len(cdn_b))
        break
    print(f"Waiting for jsDelivr purge ({attempt + 1}/5): got {len(cdn_b)} vs {len(u_bytes)}")
    time.sleep(4)
else:
    raise SystemExit(f"CDN @{args.ref} hash mismatch after retries")

SLOT_1_LEN = len(b"https://cdn.jsdelivr.net/gh/HeliumMarcos/TubeRush@main/u.js?v=") + 7
SLOT_2_LEN = len(b"https://cdn.jsdelivr.net/gh/HeliumMarcos/TubeRush@main/u.js") + 2

new1 = f"https://cdn.jsdelivr.net/gh/HeliumMarcos/TubeRush@{args.ref}/u.js?v=".encode("ascii")
new2 = f"https://cdn.jsdelivr.net/gh/HeliumMarcos/TubeRush@{args.ref}/u.js".encode("ascii")
assert len(new1) <= SLOT_1_LEN and len(new2) <= SLOT_2_LEN
new1 = new1 + b"\x00" * (SLOT_1_LEN - len(new1))
new2 = new2 + b"\x00" * (SLOT_2_LEN - len(new2))

pat1 = re.compile(rb"https://cdn\.jsdelivr\.net/gh/HeliumMarcos/TubeRush@[^/]+/u\.js\?v=\x00*")
pat2 = re.compile(rb"https://cdn\.jsdelivr\.net/gh/HeliumMarcos/TubeRush@[^/]+/u\.js(?!\?v=)\x00*")
ver_pat = re.compile(rb"2\x00\.\x000\x00\.\x00[0-9]\x00")

apk_path = args.apk
unaligned = str(apk_path) + ".unaligned"
with zipfile.ZipFile(apk_path, "r") as zin, zipfile.ZipFile(unaligned, "w") as zout:
    for item in zin.infolist():
        if item.filename.startswith("META-INF/"):
            continue
        data = zin.read(item.filename)
        if item.filename == "lib/armeabi-v7a/libchrobalt.so":
            m1 = pat1.search(data)
            assert m1 and len(m1.group(0)) == SLOT_1_LEN, f"Slot 1 match error: {m1}"
            data = data[:m1.start()] + new1 + data[m1.end():]
            m2 = pat2.search(data)
            assert m2 and len(m2.group(0)) == SLOT_2_LEN, f"Slot 2 match error: {m2}"
            data = data[:m2.start()] + new2 + data[m2.end():]
        elif item.filename == "AndroidManifest.xml":
            old_ver_m = ver_pat.search(data)
            assert old_ver_m, "versionName UTF-16LE pattern not found"
            new_ver_b = args.version_name.encode("utf-16le")
            assert len(new_ver_b) == len(old_ver_m.group(0)), "versionName byte length must match"
            data = data.replace(old_ver_m.group(0), new_ver_b)

            vc_pat = re.compile(rb"\xff\xff\xff\xff\x08\x00\x00\x10(.{4})", re.DOTALL)
            vc_matches = list(vc_pat.finditer(data))
            assert len(vc_matches) == 1, f"Expected 1 versionCode attr, found {len(vc_matches)}"
            m = vc_matches[0]
            old_vc = struct.unpack("<I", m.group(1))[0]
            data = data[:m.start(1)] + struct.pack("<I", args.version_code) + data[m.end(1):]
            print(f"Updated AndroidManifest.xml: versionName={args.version_name}, versionCode {old_vc} -> {args.version_code}")
        zout.writestr(item, data, compress_type=item.compress_type)

subprocess.run([ZIPALIGN, "-p", "-f", "4", unaligned, str(apk_path)], check=True)
os.remove(unaligned)
subprocess.run([APKSIGNER, "sign", "--ks", KEYSTORE, "--ks-pass", "pass:android", "--key-pass", "pass:android", "--ks-key-alias", "androiddebugkey", str(apk_path)], check=True)
subprocess.run([APKSIGNER, "verify", str(apk_path)], check=True)
print(f"Built & verified v{args.version_name} (code {args.version_code}) APK:", os.path.getsize(apk_path))
