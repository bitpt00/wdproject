from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def fence_language(path: Path) -> str:
    """Return a readable Markdown fence language without changing source text."""
    if path.name == ".gitignore":
        return "gitignore"
    return {
        ".py": "python",
        ".html": "html",
        ".css": "css",
        ".bat": "bat",
        ".md": "markdown",
        ".txt": "text",
    }.get(path.suffix.lower(), "text")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    files = sorted(
        (path for path in source.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(source).as_posix(),
    )
    if not files:
        raise SystemExit("No source files found.")

    rows: list[tuple[str, int, int, str]] = []
    contents: list[tuple[str, str, str]] = []
    for path in files:
        relative = path.relative_to(source).as_posix()
        raw = path.read_bytes()
        source_text = raw.decode("utf-8")
        normalized_text = source_text.replace("\r\n", "\n").replace("\r", "\n")
        rows.append(
            (
                relative,
                len(raw),
                len(normalized_text.splitlines()),
                hashlib.sha256(raw).hexdigest(),
            )
        )
        contents.append((relative, fence_language(path), normalized_text))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(f"# {args.version} 完整代码核对附录\n\n")
        handle.write(
            "> 本附录由冻结版本终点包机械生成，不是手工重新整理的代码。"
            "文件内容只统一为LF换行；原始字节数与SHA-256用于核对终点资源。\n\n"
        )
        handle.write("## 1. 文件清单\n\n")
        handle.write("| 路径 | 原始字节数 | 代码行数 | 原始文件SHA-256 |\n")
        handle.write("| --- | ---: | ---: | --- |\n")
        for relative, byte_count, line_count, digest in rows:
            handle.write(
                f"| `{relative}` | {byte_count} | {line_count} | `{digest}` |\n"
            )

        handle.write("\n## 2. 完整文件内容\n\n")
        for index, (relative, language, source_text) in enumerate(contents):
            handle.write(f"### `{relative}`\n\n")
            handle.write(f"```{language}\n")
            handle.write(source_text)
            if not source_text.endswith("\n"):
                handle.write("\n")
            handle.write("```\n")
            if index < len(contents) - 1:
                handle.write("\n")


if __name__ == "__main__":
    main()
