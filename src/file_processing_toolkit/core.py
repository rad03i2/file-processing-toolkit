from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
import hashlib
import os
import uuid

@dataclass(frozen=True)
class FileRecord:
    path: str
    size: int
    extension: str
    modified_ns: int
    def to_dict(self): return asdict(self)

def _root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists(): raise FileNotFoundError(f"Path does not exist: {p}")
    if not p.is_dir(): raise NotADirectoryError(str(p))
    return p

def scan(path: str | Path, *, recursive: bool = True, min_size: int = 0, extension: str | None = None) -> list[FileRecord]:
    if min_size < 0: raise ValueError("min_size must be >= 0")
    root = _root(path); ext = extension.lower() if extension else None
    if ext and not ext.startswith("."): ext = "." + ext
    iterator = root.rglob("*") if recursive else root.iterdir()
    out=[]
    for p in iterator:
        try:
            if p.is_symlink() or not p.is_file(): continue
            st=p.stat(); suffix=p.suffix.lower()
            if st.st_size >= min_size and (ext is None or suffix == ext):
                out.append(FileRecord(str(p), st.st_size, suffix, st.st_mtime_ns))
        except OSError: continue
    return sorted(out, key=lambda r: r.path.casefold())

def hash_file(path: str | Path, algorithm: str = "sha256", chunk_size: int = 1024 * 1024) -> str:
    if chunk_size <= 0: raise ValueError("chunk_size must be positive")
    try: h=hashlib.new(algorithm)
    except ValueError as e: raise ValueError(f"Unsupported hash algorithm: {algorithm}") from e
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""): h.update(chunk)
    return h.hexdigest()

def find_duplicates(path: str | Path, *, recursive: bool = True, algorithm: str = "sha256") -> list[list[str]]:
    by_size=defaultdict(list)
    for r in scan(path, recursive=recursive): by_size[r.size].append(r.path)
    groups=[]
    for candidates in by_size.values():
        if len(candidates)<2: continue
        by_hash=defaultdict(list)
        for p in candidates: by_hash[hash_file(p, algorithm)].append(p)
        groups.extend(sorted(v) for v in by_hash.values() if len(v)>1)
    return sorted(groups, key=lambda g: (-len(g), g[0]))

def plan_rename(path: str | Path, *, prefix: str = "file-", start: int = 1, width: int = 3) -> list[tuple[str,str]]:
    if start < 0 or width < 1: raise ValueError("start must be >= 0 and width >= 1")
    root=_root(path); records=scan(root, recursive=False); plan=[]; targets=set()
    for i,r in enumerate(records,start):
        src=Path(r.path); dst=root / f"{prefix}{i:0{width}d}{src.suffix}"
        key=os.path.normcase(str(dst))
        if key in targets: raise ValueError(f"Rename collision: {dst.name}")
        targets.add(key); plan.append((str(src),str(dst)))
    sources={os.path.normcase(a) for a,_ in plan}
    for _,dst in plan:
        if Path(dst).exists() and os.path.normcase(dst) not in sources: raise FileExistsError(dst)
    return plan

def apply_rename(plan: list[tuple[str,str]]) -> None:
    if not plan: return
    temps=[]
    try:
        for src,dst in plan:
            s=Path(src); t=s.with_name(f".{s.name}.{uuid.uuid4().hex}.rename-tmp")
            s.rename(t); temps.append((t,Path(dst),s))
        for t,dst,_ in temps: t.rename(dst)
    except Exception:
        for t,_,src in reversed(temps):
            if t.exists() and not src.exists(): t.rename(src)
        raise
