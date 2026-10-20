"""Core scanning logic for nomagic."""

import os
import re

ALLOWED = {"0", "1", "-1", "2", "10", "100", "0.0", "1.0", "2.0"}

NUM_RE = re.compile(r"(?<![A-Za-z0-9_.])(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)(?![A-Za-z0-9_.])")

EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs",
        ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".cs", ".kt", ".swift"}

EXCLUDES = {".git", "node_modules", "__pycache__", ".venv", "venv",
            "dist", "build", ".tox", ".mypy_cache", ".pytest_cache"}

PY_EXTS = {".py", ".rb"}
C_STYLE = {".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".c",
           ".cpp", ".h", ".hpp", ".cs", ".kt", ".swift", ".php"}


def _strip_comment(line, ext):
    if ext in PY_EXTS and ext != ".rb":
        idx = line.find("#")
        if idx != -1:
            line = line[:idx]
    elif ext == ".rb":
        idx = line.find("#")
        if idx != -1:
            line = line[:idx]
    else:
        idx = line.find("//")
        if idx != -1:
            line = line[:idx]
    return line


def _remove_strings(line):
    line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
    line = re.sub(r"'(?:\\.|[^'\\])*'", "''", line)
    line = re.sub(r"`(?:\\.|[^`\\])*`", "``", line)
    return line


def _is_allowed(num, extra=None):
    if num in ALLOWED:
        return True
    if extra and num in extra:
        return True
    return False


def scan_file(path, extra_allowed=None):
    findings = []
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return findings
    extra = set(extra_allowed or [])
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("#", "//", "/*", "*", "--")):
            continue
        code = _strip_comment(line, ext)
        code = _remove_strings(code)
        for m in NUM_RE.finditer(code):
            num = m.group(1)
            if _is_allowed(num, extra):
                continue
            findings.append({
                "file": path,
                "line": i,
                "number": num,
                "context": stripped,
            })
    return findings


def scan_path(root, extra_allowed=None, exts=None):
    allowed_exts = set(exts) if exts else EXTS
    results = []
    if os.path.isfile(root):
        return scan_file(root, extra_allowed)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in EXCLUDES and not d.startswith("."))
        for fn in sorted(filenames):
            if os.path.splitext(fn)[1].lower() in allowed_exts:
                results.extend(scan_file(os.path.join(dirpath, fn), extra_allowed))
    return results
