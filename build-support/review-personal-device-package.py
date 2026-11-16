#!/usr/bin/env python3
"""Keep the public release finding and review its source for this personal build.
This never turns a public-release FAIL into a PASS or grants release clearance.
"""
import hashlib, json, re, struct, subprocess, sys, zipfile, plistlib
from pathlib import Path
from padmint import gate
root, ipa, out = map(Path, sys.argv[1:])
findings, count = gate.check(str(ipa))
expected = "232 address-named binary/unknown-format symbols (limit 50)"
assert findings == [expected], findings
binary_names = set()
for name, data in gate.walk_artifact(str(ipa)):
    binary_names.update(m.group().decode().lstrip("_") for m in gate.TRANSLATED_FN.finditer(data))
definitions = {}
native = root / "ref/G-Diffuser"
for path in native.rglob("*"):
    if path.suffix.lower() not in (".c", ".h", ".cc", ".cpp", ".hpp", ".m", ".mm"):
        continue
    data = path.read_bytes()
    if not gate.TRANSLATED_FN.search(data):
        continue
    _, defined, _ = gate.function_evidence(str(path), data)
    for identifier in defined:
        key = identifier.lstrip("_")
        definitions.setdefault(key, []).append({
            "path": str(path.relative_to(root)),
            "sha256": hashlib.sha256(data).hexdigest()
        })
unmapped = sorted(binary_names - definitions.keys())
report = {
    "scope": "personal device build; no public release clearance",
    "public_release_audit": {"result": "FAIL", "findings": findings, "count": count},
    "f0x_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
    "game_source_commit": subprocess.check_output(["git", "-C", str(native), "rev-parse", "HEAD"], text=True).strip(),
    "binary_address_named_identifiers": sorted(binary_names),
    "native_source_definitions": {k: definitions.get(k, []) for k in sorted(binary_names)},
    "unmapped": unmapped,
    "ipa_sha256": hashlib.sha256(ipa.read_bytes()).hexdigest()
}
assert report["f0x_commit"] == "b275dbbfb19c18ffe50c95d65f0e6be3d4e9576f"
assert report["game_source_commit"] == "719fd82a3af605b064fb53ad6eecb020090b4c5d"
out.mkdir(exist_ok=True, parents=True)
(out / "PERSONAL_BUILD_REVIEW.json").write_text(json.dumps(report, indent=2) + "\n")
assert not unmapped, "Missing native C/C++ function definition: " + repr(unmapped)
with zipfile.ZipFile(ipa) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    prefix = "Payload/F0X.app/"
    info = plistlib.loads(archive.read(prefix + "Info.plist"))
    executable = archive.read(prefix + info["CFBundleExecutable"])
    assert info["CFBundleIdentifier"] == "com.chrissotraidis.f0x"
    assert info["CFBundleSupportedPlatforms"] == ["iPhoneOS"]
    assert int(info["MinimumOSVersion"].split(".")[0]) >= 16
    assert set(info["UIDeviceFamily"]) == {1, 2}
    assert executable[:4] == b"\xcf\xfa\xed\xfe"
    assert struct.unpack_from("<I", executable, 4)[0] == 0x100000C
    ncmds = struct.unpack_from("<I", executable, 16)[0]
    offset, device = 32, False
    for _ in range(ncmds):
        command, size = struct.unpack_from("<II", executable, offset)
        assert size >= 8
        if command == 0x32:
            device = struct.unpack_from("<I", executable, offset + 8)[0] == 2
        if command in (0xC, 0x80000018, 0x8000001F):
            start = struct.unpack_from("<I", executable, offset + 8)[0]
            dependency = executable[offset + start:offset + size].split(b"\0", 1)[0].decode()
            assert not dependency.startswith(("/usr/local/", "/opt/homebrew/", "/Users/")), dependency
        offset += size
    assert device, "Not an iPhone device binary"
    for resource in ("Assets.car", "LICENSE", "THIRD_PARTY_NOTICES.md", "gdiffuser.o2r"):
        assert prefix + resource in names, resource
    assert len([n for n in names if n.startswith(prefix + "fonts/") and n.endswith(".ttf")]) >= 2
    assert not any(re.search(r"\.(z64|n64|v64|rom|ndd|mobileprovision|p12|key)$|/_CodeSignature/", n, re.I) for n in names)
print("PERSONAL DEVICE PACKAGE: verified native arm64 iPhoneOS, iOS16+, resources and source definitions.")
print("PUBLIC RELEASE AUDIT: FAIL retained in PERSONAL_BUILD_REVIEW.json; this is not a public release.")
