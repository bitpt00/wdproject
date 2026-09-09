"""生成半自动教学平台使用的 S0→dev-v0.1 完整检查点快照。

本脚本只读取已经冻结的 S0 起点包、dev-v0.1 终点核对包，以及本文件中
与 S06 第 4.3 节一致的临时 Flask 入口。它不会改动任何来源目录。
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
S0_ROOT = REPOSITORY_ROOT / "教学资源" / "S0_起点包"
V01_ROOT = REPOSITORY_ROOT / "教学资源" / "版本终点核对包" / "dev-v0.1"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "教学资源" / "平台检查点" / "S0到V0.1"

S0_FILES = (
    ".gitignore",
    "requirements.txt",
    "初始化开发环境.bat",
)

V01_FILES = (
    ".gitignore",
    "VERSION",
    "app.py",
    "requirements.txt",
    "static/style.css",
    "templates/base.html",
    "templates/index.html",
    "templates/labs.html",
    "templates/reservation_form.html",
    "tests/test_app.py",
    "初始化开发环境.bat",
    "启动dev-v0.1.bat",
    "运行测试.bat",
)

INTERMEDIATE_APP = '''from flask import Flask


VERSION = "dev-v0.1"


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__)
    app.config.from_mapping(TESTING=False)

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return f"校园实验室预约系统 {VERSION}"

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
'''


@dataclass(frozen=True)
class CheckpointDefinition:
    checkpoint_id: str
    title: str
    website_state: str
    directories: tuple[str, ...]
    files: tuple[str, ...]
    final_app: bool = False


CHECKPOINTS = (
    CheckpointDefinition(
        "C0",
        "确认S0起点",
        "尚不能启动",
        (),
        S0_FILES,
    ),
    CheckpointDefinition(
        "C1",
        "建立项目结构",
        "尚不能启动",
        ("static", "templates", "tests"),
        S0_FILES,
    ),
    CheckpointDefinition(
        "C2",
        "建立最小Flask应用",
        "纯文字首页可访问",
        ("static", "templates", "tests"),
        S0_FILES + ("VERSION", "app.py"),
    ),
    CheckpointDefinition(
        "C3",
        "准备共享布局、首页和样式",
        "仍显示C2纯文字",
        ("static", "templates", "tests"),
        S0_FILES
        + (
            "VERSION",
            "app.py",
            "static/style.css",
            "templates/base.html",
            "templates/index.html",
        ),
    ),
    CheckpointDefinition(
        "C4",
        "准备实验室列表模板",
        "仍显示C2纯文字",
        ("static", "templates", "tests"),
        S0_FILES
        + (
            "VERSION",
            "app.py",
            "static/style.css",
            "templates/base.html",
            "templates/index.html",
            "templates/labs.html",
        ),
    ),
    CheckpointDefinition(
        "C5",
        "形成完整V0.1页面",
        "三个正式页面可操作",
        ("static", "templates", "tests"),
        S0_FILES
        + (
            "VERSION",
            "app.py",
            "static/style.css",
            "templates/base.html",
            "templates/index.html",
            "templates/labs.html",
            "templates/reservation_form.html",
        ),
        final_app=True,
    ),
    CheckpointDefinition(
        "C6",
        "增加运行与测试入口",
        "网站可运行，尚无自动测试用例",
        ("static", "templates", "tests"),
        S0_FILES
        + (
            "VERSION",
            "app.py",
            "static/style.css",
            "templates/base.html",
            "templates/index.html",
            "templates/labs.html",
            "templates/reservation_form.html",
            "启动dev-v0.1.bat",
            "运行测试.bat",
        ),
        final_app=True,
    ),
    CheckpointDefinition(
        "C7",
        "设计并运行V0.1测试",
        "三个页面可用，6项自动测试可运行",
        ("static", "templates", "tests"),
        V01_FILES,
        final_app=True,
    ),
    CheckpointDefinition(
        "C8",
        "故障恢复、终点核对和版本冻结",
        "dev-v0.1正式终点",
        ("static", "templates", "tests"),
        V01_FILES,
        final_app=True,
    ),
)


def normalized_text_bytes(data: bytes) -> bytes:
    """按课程机械核对规则统一文本换行，不忽略其他内容差异。"""
    text = data.decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_bytes(relative_path: str, *, final_app: bool) -> tuple[bytes, str]:
    if relative_path in S0_FILES:
        path = S0_ROOT / relative_path
        return path.read_bytes(), f"教学资源/S0_起点包/{relative_path}"

    if relative_path == "app.py" and not final_app:
        return INTERMEDIATE_APP.encode("utf-8"), "S06第4.3节临时app.py"

    path = V01_ROOT / Path(relative_path)
    return path.read_bytes(), f"教学资源/版本终点核对包/dev-v0.1/{relative_path}"


def ensure_sources() -> None:
    missing = [str(S0_ROOT / path) for path in S0_FILES if not (S0_ROOT / path).is_file()]
    missing.extend(
        str(V01_ROOT / path) for path in V01_FILES if not (V01_ROOT / path).is_file()
    )
    if missing:
        raise FileNotFoundError("缺少冻结来源文件：\n" + "\n".join(missing))

    s0_names = sorted(path.as_posix() for path in S0_ROOT.rglob("*") if path.is_file())
    expected_s0 = sorted((S0_ROOT / path).as_posix() for path in S0_FILES)
    if s0_names != expected_s0:
        raise RuntimeError("S0起点包不再恰好包含3个文件，已停止生成。")


def calculate_delta(
    previous_files: dict[str, str], current_files: dict[str, str]
) -> dict[str, list[str]]:
    previous_paths = set(previous_files)
    current_paths = set(current_files)
    return {
        "added": sorted(current_paths - previous_paths),
        "modified": sorted(
            path
            for path in current_paths & previous_paths
            if current_files[path] != previous_files[path]
        ),
        "removed": sorted(previous_paths - current_paths),
    }


def build(output_root: Path) -> None:
    ensure_sources()
    if output_root.exists():
        raise FileExistsError(
            f"输出目录已经存在，为避免覆盖请改用新的 --output：{output_root}"
        )

    output_root.mkdir(parents=True)
    manifest: dict[str, object] = {
        "schema_version": 1,
        "title": "S0到dev-v0.1半自动教学平台检查点",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_baseline": "S0_起点包",
        "target_version": "dev-v0.1",
        "target_git_commit": "215a1d6",
        "text_comparison": "UTF-8文本去除BOM并统一CRLF/CR为LF后计算SHA-256",
        "managed_final_files": list(V01_FILES),
        "checkpoints": [],
    }

    previous_hashes: dict[str, str] = {}
    for definition in CHECKPOINTS:
        checkpoint_root = output_root / "checkpoints" / definition.checkpoint_id
        payload_root = checkpoint_root / "payload"
        payload_root.mkdir(parents=True)
        for directory in definition.directories:
            (payload_root / directory).mkdir(parents=True, exist_ok=True)

        file_records = []
        current_hashes: dict[str, str] = {}
        for relative_path in definition.files:
            data, source = source_bytes(relative_path, final_app=definition.final_app)
            destination = payload_root / Path(relative_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            normalized_sha = sha256(normalized_text_bytes(data))
            current_hashes[relative_path] = normalized_sha
            file_records.append(
                {
                    "path": relative_path,
                    "source": source,
                    "bytes": len(data),
                    "sha256": sha256(data),
                    "normalized_text_sha256": normalized_sha,
                }
            )

        checkpoint_record = {
            "id": definition.checkpoint_id,
            "title": definition.title,
            "website_state": definition.website_state,
            "directories": list(definition.directories),
            "files": file_records,
            "delta_from_previous": calculate_delta(previous_hashes, current_hashes),
        }
        manifest["checkpoints"].append(checkpoint_record)
        (checkpoint_root / "checkpoint.json").write_text(
            json.dumps(checkpoint_record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        previous_hashes = current_hashes

    (output_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    final_payload = output_root / "checkpoints" / "C8" / "payload"
    final_paths = sorted(path.relative_to(final_payload).as_posix() for path in final_payload.rglob("*") if path.is_file())
    if final_paths != sorted(V01_FILES):
        raise RuntimeError("C8文件清单不是准确的13个dev-v0.1终点文件。")

    for relative_path in V01_FILES:
        generated = normalized_text_bytes((final_payload / relative_path).read_bytes())
        expected = normalized_text_bytes((V01_ROOT / relative_path).read_bytes())
        if generated != expected:
            raise RuntimeError(f"C8与dev-v0.1终点不一致：{relative_path}")

    print(f"已生成 {len(CHECKPOINTS)} 个检查点：{output_root}")
    print(f"C8已通过 {len(V01_FILES)} 个终点文件的规范化文本核对。")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="输出目录；必须尚不存在，默认写入教学资源/平台检查点/S0到V0.1",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    build(arguments.output.resolve())
