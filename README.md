# nomagic

Detect **magic numbers** in source code — numeric literals that appear inline instead of being
given a meaningful name. Replacing them with named constants makes code easier to read, review,
and change.

## Features

- Scans common source extensions (Python, JS/TS, Java, Go, Rust, C/C++, Ruby, PHP, C#, Kotlin, Swift).
- Skips comments and string literals.
- Allows common, harmless values (`0`, `1`, `-1`, `2`, `10`, `100`).
- Custom allow-list via `--allow`.
- Filter extensions via `--ext`.
- Human-readable or `--json` output.
- Non-zero exit code when findings exist (CI-friendly).

## Install

```bash
pip install -e .
```

Or run directly:

```bash
python -m nomagic.cli .
```

## Usage

```bash
nomagic .                    # scan current directory
nomagic src/                 # scan a directory
nomagic file.py              # scan a single file
nomagic . --json             # machine-readable output
nomagic . --allow 42,3.14    # allow extra numbers
nomagic . --ext .py,.js      # limit extensions
```

Example output:

```
src/calc.py:12: magic number 86400 -> SECONDS = 86400
src/calc.py:18: magic number 3.14159 -> return 3.14159 * r * r

Total: 2
```

## License

MIT
