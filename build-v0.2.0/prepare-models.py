from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path


metadata = Path(__file__).parent / "model-metadata"
destination = Path(sys.argv[1])
destination.mkdir(parents=True, exist_ok=False)
sources = json.loads((metadata / "MODEL_SOURCES.json").read_text(encoding="utf-8"))
for file in metadata.iterdir():
    shutil.copy2(file, destination / file.name)

base = sources["sensevoice"]["source"] + "/resolve/" + sources["sensevoice"]["revision"]
for name in ["model.int8.onnx", "tokens.txt"]:
    with urllib.request.urlopen(base + "/" + name, timeout=120) as response:
        with (destination / name).open("wb") as output:
            shutil.copyfileobj(response, output)

archive = destination.parent / "punctuation-model.tar.bz2"
with urllib.request.urlopen(sources["punctuation"]["source"], timeout=120) as response:
    with archive.open("wb") as output:
        shutil.copyfileobj(response, output)
with archive.open("rb") as stream:
    digest = hashlib.file_digest(stream, "sha256").hexdigest()
if digest != sources["punctuation"]["archive_sha256"]:
    raise SystemExit("Punctuation model archive checksum mismatch")
with tarfile.open(archive, "r:bz2") as bundle:
    matches = [member for member in bundle.getmembers() if member.isfile() and Path(member.name).name == "model.int8.onnx"]
    if len(matches) != 1:
        raise SystemExit("Expected exactly one punctuation model")
    with bundle.extractfile(matches[0]) as source:
        with (destination / "punctuation.int8.onnx").open("wb") as output:
            shutil.copyfileobj(source, output)

for name, expected in sources["files"].items():
    file = destination / name
    with file.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if file.stat().st_size != expected["bytes"] or actual != expected["sha256"]:
        raise SystemExit("Model resource checksum mismatch: " + name)
print("Prepared the exact SenseVoice and punctuation resources used by v0.2.0")
