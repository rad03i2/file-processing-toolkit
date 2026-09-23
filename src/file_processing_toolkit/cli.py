from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from . import __version__, __author__
from .core import scan, hash_file, find_duplicates, plan_rename, apply_rename

def parser():
    p=argparse.ArgumentParser(prog="file-toolkit", description="Safe local file processing toolkit")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__} — {__author__}")
    s=p.add_subparsers(dest="command", required=True)
    a=s.add_parser("scan"); a.add_argument("path"); a.add_argument("--flat",action="store_true"); a.add_argument("--min-size",type=int,default=0); a.add_argument("--extension"); a.add_argument("--json",action="store_true")
    a=s.add_parser("hash"); a.add_argument("path"); a.add_argument("--algorithm",default="sha256")
    a=s.add_parser("duplicates"); a.add_argument("path"); a.add_argument("--algorithm",default="sha256"); a.add_argument("--json",action="store_true")
    a=s.add_parser("rename"); a.add_argument("path"); a.add_argument("--prefix",default="file-"); a.add_argument("--start",type=int,default=1); a.add_argument("--width",type=int,default=3); a.add_argument("--apply",action="store_true",help="Apply the displayed plan; default is preview only")
    return p

def main(argv=None):
    args=parser().parse_args(argv)
    try:
        if args.command=="scan":
            rows=scan(args.path,recursive=not args.flat,min_size=args.min_size,extension=args.extension)
            if args.json: print(json.dumps([r.to_dict() for r in rows],ensure_ascii=False,indent=2))
            else:
                for r in rows: print(f"{r.size:>12}  {r.path}")
                print(f"Files: {len(rows)} | Bytes: {sum(r.size for r in rows)}")
        elif args.command=="hash": print(hash_file(args.path,args.algorithm), args.path)
        elif args.command=="duplicates":
            groups=find_duplicates(args.path,algorithm=args.algorithm)
            if args.json: print(json.dumps(groups,ensure_ascii=False,indent=2))
            else:
                for n,g in enumerate(groups,1): print(f"Group {n}:\n  " + "\n  ".join(g))
                print(f"Duplicate groups: {len(groups)}")
        else:
            plan=plan_rename(args.path,prefix=args.prefix,start=args.start,width=args.width)
            for src,dst in plan: print(f"{Path(src).name} -> {Path(dst).name}")
            if args.apply: apply_rename(plan); print(f"Applied {len(plan)} rename(s).")
            else: print("Preview only. Add --apply to perform these renames.")
        return 0
    except (OSError,ValueError) as e:
        print(f"error: {e}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
