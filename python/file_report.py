#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
from collections import Counter
from pathlib import Path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def scan(root: Path) -> None:
    files = [p for p in root.rglob('*') if p.is_file()]
    extensions = Counter(p.suffix.lower() or '[no extension]' for p in files)
    print(f'Scanned: {root}')
    print(f'Files: {len(files)}')
    print('\nExtensions:')
    for ext, count in extensions.most_common():
        print(f'  {ext}: {count}')
    print('\nFirst files with SHA-256:')
    for path in files[:5]:
        print(f'  {path.name}: {sha256(path)[:16]}...')


if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    scan(target)
