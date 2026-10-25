#!/usr/bin/env python3
"""Convert the original .txt snippets into real source files.

The original repository stores every solution in a .txt file.  Most files are
plain MASM sources, a handful are C++ programs and eight chapter 13 files
contain several separately labelled snippets.  This script copies each code
snippet into ``solutions/partNN/`` and writes a manifest so the CI job can
verify that nothing was lost.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "solutions"

SEPARATOR = re.compile(r"^\s*=+(?P<label>[^=]*)=+\s*$")
CPP_MARKERS = re.compile(
    r'(?im)^\s*(?:#include\b|#define\b|extern\s+"C"|(?:int|void)\s+main\s*\(|__asm\b)'
)
CPP_CODE = re.compile(r"(?im)\b(?:std::|cout\s*<<|cin\s*>>|printf\s*\(|scanf\s*\()")
ASM_MARKERS = re.compile(
    r"(?im)^\s*(?:\.(?:386|486|586|686|model|code|data|stack|const)\b|"
    r"[A-Za-z_$?][\w$?]*\s+(?:PROC|ENDP)\b|"
    r"(?:INCLUDE|include)\s+\S+\.inc\b|"
    r"END\b)"
)
ASM_DIRECTIVE = re.compile(
    r"(?im)^\s*(?:\.(?:386|486|586|686|model|code|data|stack|const)\b|"
    r"[A-Za-z_$?][\w$?]*\s+(?:PROC|ENDP)\b|"
    r"(?:INCLUDE|include)\s+\S+\.inc\b)"
)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("c++", "cpp").replace("asm", "asm")
    value = re.sub(r"[^a-z0-9.]+", "-", value)
    return value.strip("-.")


def part_number(name: str) -> int:
    match = re.match(r"(\d+)", name)
    if not match:
        raise ValueError(f"cannot determine part number from {name!r}")
    return int(match.group(1))


def stem_slug(name: str) -> str:
    return slugify(Path(name).stem)


def classify(text: str) -> str | None:
    """Return 'cpp', 'asm' or None for a chunk that only contains notes."""
    has_cpp = bool(CPP_MARKERS.search(text) or CPP_CODE.search(text))
    has_asm = bool(ASM_MARKERS.search(text))
    if has_cpp:
        return "cpp"
    if has_asm:
        return "asm"
    return None


def default_name(label: str, extension: str, used: set[str]) -> str:
    base = slugify(label)
    if base in {"cpp", "c"}:
        base = "main"
    elif base == "asm":
        base = "module"
    if not base:
        base = "main"
    candidate = f"{base}.{extension}"
    index = 2
    while candidate in used:
        candidate = f"{base}-{index}.{extension}"
        index += 1
    used.add(candidate)
    return candidate


def split_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_label = ""
    current: list[str] = []
    for line in lines:
        match = SEPARATOR.match(line)
        if match:
            sections.append((current_label, current))
            current_label = match.group("label").strip()
            current = []
        else:
            current.append(line)
    sections.append((current_label, current))
    return sections


def clean(lines: list[str]) -> str:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(line.rstrip() for line in lines) + "\n"


# A few snippets were transcribed with defects that prevent them from
# assembling (an uncommented prose line, a truncated PROTO list, a byte-sized
# immediate that does not fit in DX, a missing PROC/ENDP pair, ...).  The fixes
# live here so that regenerating the sources keeps producing buildable code.
FIXUPS: dict[str, list[tuple[str, str]]] = {
    "part04/4.9.2-1.asm": [
        (
            "; p. 136 Algorithm workbench, ex. 1 - Write a sequence of MOV instructions that will exchange the upper and lower words in a\n"
            "doubleword variable named three.",
            "; p. 136 Algorithm workbench, ex. 1 - Write a sequence of MOV instructions that will exchange the upper and lower words in a\n"
            "; doubleword variable named three.",
        )
    ],
    "part04/4.9.2-2.asm": [
        (
            "registers\nfrom the order A,B,C,D to B,C,D,A.",
            "registers\n; from the order A,B,C,D to B,C,D,A.",
        )
    ],
    "part04/4.9.2-8.asm": [
        (
            "elements\nusing a scale factor with indexed addressing.",
            "elements\n; using a scale factor with indexed addressing.",
        )
    ],
    "part06/6.11.2-1.asm": [
        ("6.11.2 - 1\n\nINCLUDE Irvine32.inc", "; 6.11.2 - 1\n\nINCLUDE Irvine32.inc")
    ],
    "part11/11.8-4.asm": [
        (
            "CharBuffer:ptr byte,\n\n;CharOutput proc",
            "CharBuffer:ptr byte\n\n;CharOutput proc",
        )
    ],
    "part11/11.8-9a.asm": [
        (
            "CharBuffer:ptr byte,\n\nFileDate proto,",
            "CharBuffer:ptr byte\n\nFileDate proto,",
        )
    ],
    "part14/14.5-3.asm": [
        (".stack 100 h", ".stack 100h"),
        (
            ".code\n\n;set DS to the location of the data segment",
            ".code\n\nmain proc\n\n;set DS to the location of the data segment",
        ),
        (
            "mov ah, 4ch\nint 21h",
            "mov ah, 4ch\nint 21h\n\nmain endp\nend main",
        ),
    ],
    "part16/16.8-5.asm": [
        ("mov dx, 100000d; low word", "mov dx, 86A0h; low word of 100000d")
    ],
    "part16/16.8-5a.asm": [
        ("mov dx, 80000d; low word", "mov dx, 3880h; low word of 80000d")
    ],
    "part16/16.8-6.asm": [
        ("mov dx, 80000d; low word", "mov dx, 3880h; low word of 80000d")
    ],
    "part16/16.8-6a.asm": [
        ("mov dx, 500000d; low word", "mov dx, 0A120h; low word of 500000d")
    ],
    "part16/16.8-6b.asm": [
        ("mov dx, 500000d; low word", "mov dx, 0A120h; low word of 500000d")
    ],
    "part13/13.7-5a/main.cpp": [
        (
            "void main()\n{\n\tasm_main();\n}",
            "int main()\n{\n\tasm_main();\n\treturn 0;\n}",
        )
    ],
}


def apply_fixups(relative_path: str, text: str) -> str:
    for old, new in FIXUPS.get(relative_path, []):
        if old not in text:
            raise RuntimeError(f"fixup no longer applies to {relative_path}: {old!r}")
        text = text.replace(old, new, 1)
    return text


INCLUDE_LINE = re.compile(
    r"(?im)^([ \t]*INCLUDE[ \t]+)([A-Za-z0-9_.\\/]+)([ \t]*(?:;.*)?)$"
)
CANONICAL_INCLUDES = {
    "irvine32.inc": "Irvine32.inc",
    "macros.inc": "Macros.inc",
    "graphwin.inc": "GraphWin.inc",
}


def normalize_includes(text: str) -> str:
    """Use the canonical filename case so JWasm on Linux finds the headers."""

    def replace(match: re.Match[str]) -> str:
        name = match.group(2)
        return match.group(1) + CANONICAL_INCLUDES.get(name.lower(), name) + match.group(3)

    return INCLUDE_LINE.sub(replace, text)


def write_source(target: Path, text: str) -> None:
    relative = target.relative_to(OUTPUT).as_posix()
    text = normalize_includes(text)
    target.write_text(apply_fixups(relative, text), encoding="utf-8", newline="\n")


def read_snippet(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def convert_file(path: Path) -> list[Path]:
    text = read_snippet(path)
    lines = text.splitlines()
    part_dir = OUTPUT / f"part{part_number(path.name):02d}"
    outputs: list[Path] = []

    if not any(SEPARATOR.match(line) for line in lines):
        extension = classify(text)
        if extension is None:
            print(f"warning: no code detected in {path.name}", file=sys.stderr)
            return outputs
        target_dir = part_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{stem_slug(path.name)}.{extension}"
        write_source(target, clean(lines))
        return [target]

    # Files containing several snippets use lines of '=' to separate them.
    target_dir = part_dir / stem_slug(path.name)
    target_dir.mkdir(parents=True, exist_ok=True)
    used: set[str] = set()
    for label, section in split_sections(lines):
        body = clean(section)
        extension = classify(body)
        if extension is None:
            if body.strip():
                print(
                    f"note: skipped text-only section {label!r} in {path.name}",
                    file=sys.stderr,
                )
            continue
        target = target_dir / default_name(label, extension, used)
        write_source(target, body)
        outputs.append(target)

    if not outputs:
        raise RuntimeError(f"no code extracted from {path.name}")
    return outputs


def main() -> int:
    source_files = sorted(ROOT.glob("*.txt"), key=lambda p: (part_number(p.name), p.name.lower()))
    if not source_files:
        print("no .txt snippets found", file=sys.stderr)
        return 1

    if OUTPUT.exists():
        for old in sorted(OUTPUT.rglob("*"), reverse=True):
            if old.is_file():
                old.unlink()
            elif old.is_dir():
                old.rmdir()

    manifest: list[tuple[str, list[Path]]] = []
    for source in source_files:
        manifest.append((source.name, convert_file(source)))

    manifest_data = {
        "generated_by": "scripts/convert_snippets.py",
        "sources": {
            source_name: [p.relative_to(OUTPUT).as_posix() for p in outputs]
            for source_name, outputs in manifest
        },
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    lines = [
        "# Generated solutions",
        "",
        "This directory is generated from the original `.txt` snippets by",
        "`scripts/convert_snippets.py`.  Do not edit the files by hand; edit the",
        "converter or the original snippet and regenerate.",
        "",
        "| Original snippet | Source file(s) |",
        "| --- | --- |",
    ]
    for source_name, outputs in manifest:
        links = ", ".join(
            f"[`{p.relative_to(OUTPUT).as_posix()}`]({p.relative_to(OUTPUT).as_posix()})"
            for p in outputs
        ) or "(no code found)"
        lines.append(f"| `{source_name}` | {links} |")
    (OUTPUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    total = sum(len(outputs) for _, outputs in manifest)
    print(f"converted {len(manifest)} snippets into {total} source files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
