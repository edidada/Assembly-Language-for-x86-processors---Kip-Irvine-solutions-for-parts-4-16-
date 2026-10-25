#!/usr/bin/env python3
"""Sanity checks for the generated source tree.

The real build check is performed by JWasm in the GitHub Actions workflow.
This script makes sure that the conversion did not silently drop a snippet and
that every source file still looks like compilable MASM/C++ instead of a raw
text dump.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOLUTIONS = ROOT / "solutions"
MANIFEST = SOLUTIONS / "manifest.json"
SOURCE_SUFFIXES = {".asm", ".cpp"}

CPP_MAIN = re.compile(r"(?im)^\s*(?:int|void)\s+main\s*\(")
ASM_END = re.compile(r"(?im)^\s*END\b")
ASM_PROC = re.compile(r"(?im)^\s*[A-Za-z_$?][\w$?]*\s+PROC\b")
ASM_ENDP = re.compile(r"(?im)^\s*[A-Za-z_$?][\w$?]*\s+ENDP\b")
LEFTOVER_SEPARATOR = re.compile(r"(?m)^\s*={5,}")


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.is_file():
        print(f"error: missing {MANIFEST.relative_to(ROOT)}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources: dict[str, list[str]] = manifest.get("sources", {})

    txt_files = {p.name for p in ROOT.glob("*.txt")}
    if set(sources) != txt_files:
        for missing in sorted(txt_files - set(sources)):
            errors.append(f"source snippet not in manifest: {missing}")
        for extra in sorted(set(sources) - txt_files):
            errors.append(f"manifest references missing snippet: {extra}")

    listed: set[str] = set()
    for snippet, outputs in sorted(sources.items()):
        if not outputs:
            errors.append(f"{snippet}: no source files were generated")
            continue
        for relative in outputs:
            if relative in listed:
                errors.append(f"{relative}: generated more than once")
                continue
            listed.add(relative)
            path = SOLUTIONS / relative
            if not path.is_file():
                errors.append(f"{relative}: file does not exist")
                continue
            text = path.read_text(encoding="utf-8")
            if not text.strip():
                errors.append(f"{relative}: file is empty")
                continue
            if LEFTOVER_SEPARATOR.search(text):
                errors.append(f"{relative}: contains an unconverted '=' section separator")

            if path.suffix == ".asm":
                if not ASM_END.search(text):
                    errors.append(f"{relative}: missing END directive")
                procs = len(ASM_PROC.findall(text))
                endps = len(ASM_ENDP.findall(text))
                if procs != endps:
                    errors.append(f"{relative}: {procs} PROC(s) but {endps} ENDP(s)")
            elif path.suffix == ".cpp":
                if not CPP_MAIN.search(text):
                    errors.append(f"{relative}: missing main() function")

    actual = {
        p.relative_to(SOLUTIONS).as_posix()
        for p in SOLUTIONS.rglob("*")
        if p.is_file() and p.suffix in SOURCE_SUFFIXES
    }
    for orphan in sorted(actual - listed):
        errors.append(f"{orphan}: source file is not referenced by the manifest")
    for missing in sorted(listed - actual):
        if not (SOLUTIONS / missing).is_file():
            errors.append(f"{missing}: manifest entry has no file")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"{len(errors)} validation error(s)", file=sys.stderr)
        return 1

    print(
        f"validated {len(sources)} snippets -> {len(actual)} source files "
        f"({sum(1 for p in actual if p.endswith('.asm'))} MASM, "
        f"{sum(1 for p in actual if p.endswith('.cpp'))} C++)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
