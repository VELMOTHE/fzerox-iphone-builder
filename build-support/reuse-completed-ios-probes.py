#!/usr/bin/env python3
"""Reuse completed compiler capability probes from the exact same Apple SDK."""
import hashlib, io, os, re, sys, urllib.request, zipfile
from pathlib import Path
url = "https://api.github.com/repos/VELMOTHE/fzerox-iphone-builder/actions/artifacts/14246274575/zip"
request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
request.add_unredirected_header("Authorization", "Bearer " + os.environ["GH_TOKEN"])
with urllib.request.urlopen(request, timeout=120) as response:
    data = response.read(16 * 1024 * 1024 + 1)
assert hashlib.sha256(data).hexdigest() == "c26ad8884dadcf2733afa04d91b4aa1157a1274ca17135b2a5451f0710184c0e"
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    names = [n for n in archive.namelist() if n.endswith("CMakeCache.txt")]
    assert len(names) == 1
    cache = archive.read(names[0]).decode()
assert "iphoneos26.2" in cache
allowed = re.compile(r"^(HAVE_|CHECK_CPU_|COMPILER_SUPPORTS_|SIZEOF_|STDC_HEADERS|CMAKE_HAVE_|SDL_CPU_)")
rows = []
for line in cache.splitlines():
    match = re.fullmatch(r"([A-Za-z0-9_]+):INTERNAL=(.*)", line)
    if not match:
        continue
    key, value = match.groups()
    if allowed.match(key) and (value in ("", "TRUE", "FALSE") or re.fullmatch(r"[0-9]+", value)):
        rows.append('set(' + key + ' "' + value + '" CACHE INTERNAL "Verified iOS 26.2 arm64 probe" FORCE)')
assert len(rows) >= 200, len(rows)
Path(sys.argv[1]).write_text("# Exact Xcode 26.3 / iPhoneOS 26.2 arm64, completed CI probes.\n" + "\n".join(rows) + "\n")
print("Reused", len(rows), "completed probes; no game data or compiler output reused.")
