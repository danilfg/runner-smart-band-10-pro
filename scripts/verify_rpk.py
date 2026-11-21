#!/usr/bin/env python3
"""Ensure the installable RPK really bundles the new character resource paths."""
from pathlib import Path
import hashlib
import sys
import zipfile
root=Path(__file__).resolve().parents[1]
rpk=Path(sys.argv[1])
if not zipfile.is_zipfile(rpk):
    raise SystemExit('Invalid RPK: not a ZIP archive')
names=[f'hero_{hero}{pose}_v3.png' for hero in ('boy','gecko') for pose in ('','_run','_duck')]
with zipfile.ZipFile(rpk) as z:
    entries=z.namelist()
    for name in names:
        matches=[n for n in entries if n.split('/')[-1]==name]
        if len(matches)!=1:
            raise SystemExit(f'RPK image {name}: expected 1, found {len(matches)}')
        source=(root/'src'/'common'/name).read_bytes()
        packaged=z.read(matches[0])
        if hashlib.sha256(source).digest()!=hashlib.sha256(packaged).digest():
            raise SystemExit(f'RPK packed wrong bytes: {name}')
    print('Verified six V3 PNG images inside RPK:',rpk)
