"""半自动教学平台的受控工作区、测试、故障恢复和 Git 引擎。"""

from __future__ import annotations

import atexit
import csv
import difflib
import hashlib
import importlib.metadata
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .content import CHECKPOINT_ORDER, MANUAL_TEST_SCENARIOS, TASKS


STUDENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{2,32}$")
TEST_COUNT_PATTERN = re.compile(r"(\d+) passed")
STATE_SCHEMA_VERSION = 2

PHASE_LABELS = {
    "predict": "先作判断",
    "build": "生成本步变化",
    "experience": "亲手体验",
    "observe": "核对现象",
    "explain": "说清原理",
    "finish": "完成本关",
    "completed": "已完成",
}

PHASE_ACTIONS = {
    "predict": "回答1道选择题",
    "build": "让平台生成本步文件",
    "experience": "按清单亲手操作",
    "observe": "勾选亲眼看到的结果",
    "explain": "补全1句话",
    "finish": "验证并完成本关",
    "completed": "查看已保存的学习记录",
}


class PlatformError(RuntimeError):
    """面向学生显示、无需暴露内部堆栈的可恢复错误。"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalized_text(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class TeachingEngine:
    """每个公开方法都把文件操作限制在平台 runtime 工作区内。"""

    def __init__(self, runtime_root: Path, checkpoint_root: Path):
        self.runtime_root = Path(runtime_root).resolve()
        self.checkpoint_root = Path(checkpoint_root).resolve()
        self.workspace_root = self.runtime_root / "workspaces"
        self.state_root = self.runtime_root / "states"
        self.backup_root = self.runtime_root / "backups"
        self.log_root = self.runtime_root / "logs"
        self.export_root = self.runtime_root / "exports"
        for directory in (
            self.runtime_root,
            self.workspace_root,
            self.state_root,
            self.backup_root,
            self.log_root,
            self.export_root,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        self.pytest_config = self.runtime_root / "isolated-pytest.ini"
        if not self.pytest_config.exists():
            self.pytest_config.write_text(
                "[pytest]\ntestpaths = tests\naddopts = --disable-warnings\n",
                encoding="utf-8",
            )

        manifest_path = self.checkpoint_root / "manifest.json"
        if not manifest_path.is_file():
            raise PlatformError(f"找不到检查点清单：{manifest_path}")
        self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.checkpoints = {
            checkpoint["id"]: checkpoint for checkpoint in self.manifest["checkpoints"]
        }
        if tuple(self.checkpoints) != CHECKPOINT_ORDER:
            raise PlatformError("检查点清单必须严格按 C0—C8 排列。")

        self.final_files = tuple(self.manifest["managed_final_files"])
        self._lock = threading.RLock()
        self._processes: dict[str, tuple[subprocess.Popen[bytes], Any, int]] = {}
        atexit.register(self.stop_all)

    # ---------- 路径、状态与日志 ----------

    @staticmethod
    def validate_student_id(student_id: str) -> str:
        value = (student_id or "").strip()
        if not STUDENT_ID_PATTERN.fullmatch(value):
            raise PlatformError("学号只能包含2—32位英文字母、数字、下划线或短横线。")
        return value

    @staticmethod
    def _bounded_text(value: str | None, field: str, maximum: int = 5000) -> str:
        text = (value or "").strip()
        if len(text) > maximum:
            raise PlatformError(f"{field}不能超过{maximum}个字符。")
        return text

    @staticmethod
    def _ensure_inside(path: Path, root: Path) -> Path:
        resolved_root = root.resolve()
        resolved_path = path.resolve()
        try:
            resolved_path.relative_to(resolved_root)
        except ValueError as exc:
            raise PlatformError(f"拒绝访问工作区范围外的路径：{resolved_path}") from exc
        return resolved_path

    def workspace_path(self, student_id: str) -> Path:
        safe_id = self.validate_student_id(student_id)
        return self._ensure_inside(self.workspace_root / safe_id, self.workspace_root)

    def state_path(self, student_id: str) -> Path:
        safe_id = self.validate_student_id(student_id)
        return self._ensure_inside(self.state_root / f"{safe_id}.json", self.state_root)

    def _load_state(self, student_id: str) -> dict[str, Any]:
        path = self.state_path(student_id)
        if not path.is_file():
            raise PlatformError("尚未创建该学号的学习工作区。")
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PlatformError(f"学习状态文件无法读取：{path}") from exc
        if self._upgrade_state(state):
            self._save_state(state)
        return state

    @staticmethod
    def _upgrade_state(state: dict[str, Any]) -> bool:
        """把旧版三输入框草稿迁移到逐步向导，并保留原文供追溯。"""

        if state.get("schema_version", 1) >= STATE_SCHEMA_VERSION:
            return False
        c0 = state["tasks"]["C0"]
        c0_old_values = [
            c0.get(field, "").strip()
            for field in ("prediction", "observation", "explanation")
            if c0.get(field, "").strip()
        ]
        later_checkpoint_applied = any(
            state["tasks"][checkpoint_id].get("applied")
            for checkpoint_id in CHECKPOINT_ORDER[1:]
        )
        reset_invalid_c0 = (
            c0.get("completed")
            and len(c0_old_values) == 3
            and len(set(c0_old_values)) == 1
            and not later_checkpoint_applied
        )
        for checkpoint_id in CHECKPOINT_ORDER:
            task = state["tasks"][checkpoint_id]
            if checkpoint_id == "C0" and reset_invalid_c0:
                task["completed"] = False
                task["completed_at"] = None
                state["current_checkpoint"] = "C0"
            completed = bool(task.get("completed"))
            old_reflections = {
                field: task.get(field, "")
                for field in ("prediction", "observation", "explanation")
                if task.get(field, "")
            }
            if old_reflections and not completed:
                task["legacy_reflections"] = old_reflections
                task["prediction"] = ""
                task["observation"] = ""
                task["explanation"] = ""
            task.setdefault("prediction_choice", "")
            task.setdefault("observation_items", [])
            task["action_confirmed"] = completed
            task["action_confirmed_at"] = task.get("completed_at") if completed else None
            task["prediction_saved_at"] = task.get("completed_at") if completed else None
            task["observation_saved_at"] = task.get("completed_at") if completed else None
            task["explanation_saved_at"] = task.get("completed_at") if completed else None
        for case in state.get("manual_tests", []):
            if not case.get("precondition", "").strip():
                case["precondition"] = "学生项目已经启动，浏览器可以正常访问。"
        state["schema_version"] = STATE_SCHEMA_VERSION
        state.setdefault("actions", []).append(
            {
                "time": utc_now(),
                "action": "state_upgraded_to_guided_flow",
                "details": {"schema_version": STATE_SCHEMA_VERSION},
            }
        )
        return True

    def _save_state(self, state: dict[str, Any]) -> None:
        student_id = state["profile"]["student_id"]
        path = self.state_path(student_id)
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary, path)

    @staticmethod
    def _record(state: dict[str, Any], action: str, **details: Any) -> None:
        state["actions"].append(
            {"time": utc_now(), "action": action, "details": details}
        )

    def get_state(self, student_id: str) -> dict[str, Any]:
        with self._lock:
            return self._load_state(student_id)

    def list_students(self) -> list[dict[str, Any]]:
        summaries = []
        for path in sorted(self.state_root.glob("*.json")):
            try:
                state = json.loads(path.read_text(encoding="utf-8"))
                summaries.append(
                    {
                        "student_id": state["profile"]["student_id"],
                        "name": state["profile"]["name"],
                        "active": self.active_checkpoint(state),
                        "completed": sum(
                            1 for task in state["tasks"].values() if task["completed"]
                        ),
                        "last_action": state["actions"][-1]["time"]
                        if state["actions"]
                        else state["profile"]["created_at"],
                    }
                )
            except (OSError, KeyError, json.JSONDecodeError):
                continue
        return summaries

    # ---------- 检查点快照 ----------

    def _checkpoint_payload(self, checkpoint_id: str) -> Path:
        if checkpoint_id not in self.checkpoints:
            raise PlatformError("检查点编号无效。")
        return self.checkpoint_root / "checkpoints" / checkpoint_id / "payload"

    def _copy_snapshot(self, checkpoint_id: str, workspace: Path) -> None:
        checkpoint = self.checkpoints[checkpoint_id]
        payload = self._checkpoint_payload(checkpoint_id)
        for directory in checkpoint["directories"]:
            destination = self._ensure_inside(workspace / directory, workspace)
            destination.mkdir(parents=True, exist_ok=True)

        for record in checkpoint["files"]:
            relative_path = record["path"]
            source = payload / Path(relative_path)
            destination = self._ensure_inside(workspace / Path(relative_path), workspace)
            if not source.is_file():
                raise PlatformError(f"检查点来源文件缺失：{source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

    def _verify_files(self, checkpoint_id: str, workspace: Path) -> dict[str, Any]:
        checkpoint = self.checkpoints[checkpoint_id]
        expected = {record["path"]: record for record in checkpoint["files"]}
        checks = []
        passed = True
        for directory in checkpoint["directories"]:
            exists = (workspace / directory).is_dir()
            checks.append(
                {"item": f"目录 {directory}", "passed": exists, "detail": "存在" if exists else "缺失"}
            )
            passed = passed and exists

        for relative_path, record in expected.items():
            path = workspace / Path(relative_path)
            if not path.is_file():
                checks.append({"item": relative_path, "passed": False, "detail": "文件缺失"})
                passed = False
                continue
            actual = sha256(path.read_bytes())
            file_passed = actual == record["sha256"]
            checks.append(
                {
                    "item": relative_path,
                    "passed": file_passed,
                    "detail": "内容一致" if file_passed else "内容已变化",
                }
            )
            passed = passed and file_passed

        for relative_path in self.final_files:
            if relative_path not in expected and (workspace / Path(relative_path)).exists():
                checks.append(
                    {"item": relative_path, "passed": False, "detail": "本检查点不应提前出现"}
                )
                passed = False
        return {"passed": passed, "checks": checks}

    def _environment_info(self) -> dict[str, str]:
        def version(distribution: str) -> str:
            try:
                return importlib.metadata.version(distribution)
            except importlib.metadata.PackageNotFoundError:
                return "未安装"

        git = self._run_command(["git", "--version"], cwd=self.runtime_root, check=False)
        return {
            "python": sys.version.split()[0],
            "python_executable": sys.executable,
            "flask": version("Flask"),
            "pytest": version("pytest"),
            "git": (git.stdout or git.stderr).strip() or "不可用",
        }

    def create_or_continue(self, student_id: str, name: str) -> tuple[dict[str, Any], bool]:
        with self._lock:
            safe_id = self.validate_student_id(student_id)
            student_name = self._bounded_text(name, "姓名", 50)
            if not student_name:
                raise PlatformError("请输入姓名。")
            state_file = self.state_path(safe_id)
            if state_file.exists():
                return self._load_state(safe_id), False

            workspace = self.workspace_path(safe_id)
            if workspace.exists() and any(workspace.iterdir()):
                raise PlatformError("该学号目录已有内容但没有平台状态，平台不会自动覆盖。")
            workspace.mkdir(parents=True, exist_ok=True)
            self._copy_snapshot("C0", workspace)
            self._initialize_git(workspace, safe_id)

            now = utc_now()
            state: dict[str, Any] = {
                "schema_version": STATE_SCHEMA_VERSION,
                "profile": {"student_id": safe_id, "name": student_name, "created_at": now},
                "workspace": str(workspace),
                "current_checkpoint": "C0",
                "tasks": {
                    checkpoint_id: {
                        "prediction": "",
                        "prediction_choice": "",
                        "prediction_saved_at": None,
                        "action_confirmed": False,
                        "action_confirmed_at": None,
                        "observation": "",
                        "observation_items": [],
                        "observation_saved_at": None,
                        "explanation": "",
                        "explanation_saved_at": None,
                        "applied": checkpoint_id == "C0",
                        "applied_at": now if checkpoint_id == "C0" else None,
                        "verified": False,
                        "completed": False,
                        "completed_at": None,
                    }
                    for checkpoint_id in CHECKPOINT_ORDER
                },
                "environment": self._environment_info(),
                "actions": [],
                "manual_tests": [
                    {
                        **scenario,
                        "precondition": "学生项目已经启动，浏览器可以正常访问。",
                        "action": scenario["suggested_action"],
                        "expected": "",
                        "actual": "",
                        "conclusion": "",
                    }
                    for scenario in MANUAL_TEST_SCENARIOS
                ],
                "test_history": [],
                "last_test": None,
                "fault": None,
                "git_result": {"s0_commit": self._git_head(workspace)},
                "export_result": None,
            }
            initial_check = self._verify_files("C0", workspace)
            state["tasks"]["C0"]["verified"] = initial_check["passed"]
            state["tasks"]["C0"]["verification"] = initial_check
            self._record(state, "workspace_created", checkpoint="C0", files=3)
            self._save_state(state)
            return state, True

    @staticmethod
    def active_checkpoint(state: dict[str, Any]) -> str | None:
        for checkpoint_id in CHECKPOINT_ORDER:
            if not state["tasks"][checkpoint_id]["completed"]:
                return checkpoint_id
        return None

    @staticmethod
    def task_phase(state: dict[str, Any], checkpoint_id: str) -> str:
        task = state["tasks"][checkpoint_id]
        if task["completed"]:
            return "completed"
        if not task.get("prediction"):
            return "predict"
        if checkpoint_id != "C0" and not task["applied"]:
            return "build"
        if not task.get("action_confirmed"):
            return "experience"
        if not task.get("observation"):
            return "observe"
        if not task.get("explanation"):
            return "explain"
        return "finish"

    def action_readiness(
        self, state: dict[str, Any], checkpoint_id: str
    ) -> dict[str, Any]:
        """说明“亲手体验”步骤能否确认，并给页面可直接理解的原因。"""

        if checkpoint_id == "C6":
            ready = any(
                item.get("kind") == "empty_collection"
                for item in state.get("test_history", [])
            )
            return {
                "ready": ready,
                "reason": "先到测试页运行一次，看到“尚无测试用例”后再回来确认。",
            }
        if checkpoint_id == "C7":
            last_test = state.get("last_test") or {}
            applied_at = state["tasks"]["C7"].get("applied_at") or ""
            ready = (
                self._manual_tests_complete(state)
                and self._last_test_passed(state)
                and last_test.get("finished_at", "") >= applied_at
            )
            return {
                "ready": ready,
                "reason": "先完成5项手工验收，再运行新加入的自动测试并得到 6 passed。",
            }
        if checkpoint_id == "C8":
            fault = state.get("fault") or {}
            last_test = state.get("last_test") or {}
            ready = (
                fault.get("status") == "recovered"
                and self._last_test_passed(state)
                and last_test.get("finished_at", "") >= fault.get("recovered_at", "~")
            )
            return {
                "ready": ready,
                "reason": "先完成故障判断与恢复，再在恢复之后重新得到 6 passed。",
            }
        return {"ready": True, "reason": "完成上方操作后即可确认。"}

    def task_statuses(self, state: dict[str, Any]) -> list[dict[str, Any]]:
        active = self.active_checkpoint(state)
        statuses = []
        for checkpoint_id in CHECKPOINT_ORDER:
            task_state = state["tasks"][checkpoint_id]
            if task_state["completed"]:
                status = "completed"
            elif checkpoint_id == active:
                status = "active"
            else:
                status = "locked"
            phase = self.task_phase(state, checkpoint_id)
            statuses.append(
                {
                    "id": checkpoint_id,
                    "title": TASKS[checkpoint_id]["title"],
                    "status": status,
                    "applied": task_state["applied"],
                    "verified": task_state["verified"],
                    "phase": phase,
                    "phase_label": PHASE_LABELS[phase],
                    "next_action": (
                        PHASE_ACTIONS[phase]
                        if status != "locked"
                        else "等待前一关完成"
                    ),
                }
            )
        return statuses

    def _require_active(self, state: dict[str, Any], checkpoint_id: str) -> None:
        if checkpoint_id not in CHECKPOINT_ORDER:
            raise PlatformError("检查点编号无效。")
        active = self.active_checkpoint(state)
        if active != checkpoint_id:
            if state["tasks"][checkpoint_id]["completed"]:
                raise PlatformError("该任务已完成，只能查看，不能再次修改记录。")
            raise PlatformError(f"请先完成 {active or '全部任务'}，不能跳过检查点。")

    def save_prediction(
        self, student_id: str, checkpoint_id: str, choice: str
    ) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, checkpoint_id)
            task = state["tasks"][checkpoint_id]
            if task.get("action_confirmed") or (
                checkpoint_id != "C0" and task["applied"]
            ):
                raise PlatformError("已经进入实际操作，不能再把结果改写成事前判断。")
            options = {
                item["id"]: item["text"]
                for item in TASKS[checkpoint_id]["guide"]["prediction"]["options"]
            }
            selected = self._bounded_text(choice, "选择", 10)
            if selected not in options:
                raise PlatformError("请选择一个答案后再继续。")
            task["prediction_choice"] = selected
            task["prediction"] = f"{selected}. {options[selected]}"
            task["prediction_saved_at"] = utc_now()
            self._record(
                state,
                "prediction_saved",
                checkpoint=checkpoint_id,
                choice=selected,
            )
            self._save_state(state)
            return state

    def confirm_action(self, student_id: str, checkpoint_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, checkpoint_id)
            task = state["tasks"][checkpoint_id]
            if not task["applied"]:
                raise PlatformError("请先让平台生成本步文件。")
            if not task.get("prediction"):
                raise PlatformError("请先完成第1步判断。")
            readiness = self.action_readiness(state, checkpoint_id)
            if not readiness["ready"]:
                raise PlatformError(readiness["reason"])
            task["action_confirmed"] = True
            task["action_confirmed_at"] = utc_now()
            self._record(state, "student_action_confirmed", checkpoint=checkpoint_id)
            self._save_state(state)
            return state

    def save_observation(
        self, student_id: str, checkpoint_id: str, selected_items: list[str]
    ) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, checkpoint_id)
            task = state["tasks"][checkpoint_id]
            if not task.get("action_confirmed"):
                raise PlatformError("请先完成亲手操作，再核对实际结果。")
            items = TASKS[checkpoint_id]["guide"]["observation"]["items"]
            expected_ids = [item["id"] for item in items]
            selected = list(dict.fromkeys(selected_items))
            if set(selected) != set(expected_ids):
                raise PlatformError("请完成实际操作，并逐项勾选所有亲眼确认的结果。")
            text_by_id = {item["id"]: item["text"] for item in items}
            task["observation_items"] = expected_ids
            task["observation"] = "已确认：" + "；".join(
                text_by_id[item_id] for item_id in expected_ids
            )
            task["observation_saved_at"] = utc_now()
            self._record(
                state,
                "observation_saved",
                checkpoint=checkpoint_id,
                items=expected_ids,
            )
            self._save_state(state)
            return state

    def save_explanation(
        self, student_id: str, checkpoint_id: str, explanation: str
    ) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, checkpoint_id)
            task = state["tasks"][checkpoint_id]
            if not task.get("observation"):
                raise PlatformError("请先核对并保存实际观察结果。")
            answer = self._bounded_text(explanation, "一句话结论", 500)
            if len(answer) < 8:
                raise PlatformError("请至少写8个字，把原因说完整。")
            task["explanation"] = answer
            task["explanation_saved_at"] = utc_now()
            self._record(state, "explanation_saved", checkpoint=checkpoint_id)
            self._save_state(state)
            return state

    def apply_checkpoint(self, student_id: str, checkpoint_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, checkpoint_id)
            task = state["tasks"][checkpoint_id]
            if checkpoint_id == "C0":
                raise PlatformError("C0 已在创建个人工作区时准确应用。")
            if not task.get("prediction_choice"):
                raise PlatformError("请先完成第1步选择题，再生成本步文件。")
            if checkpoint_id == "C7" and not self._manual_tests_complete(state):
                raise PlatformError("请先完成测试页中的5项手工验收记录，再加入自动测试。")

            self.stop_student(student_id, record=False)
            workspace = self.workspace_path(student_id)
            self._copy_snapshot(checkpoint_id, workspace)
            verification = self._verify_files(checkpoint_id, workspace)
            if not verification["passed"]:
                raise PlatformError("检查点文件应用后核对失败，未改变任务完成状态。")
            task["applied"] = True
            task["applied_at"] = utc_now()
            task["action_confirmed"] = False
            task["action_confirmed_at"] = None
            task["verified"] = False
            task["verification"] = verification
            state["current_checkpoint"] = checkpoint_id
            delta = self.checkpoints[checkpoint_id]["delta_from_previous"]
            self._record(state, "checkpoint_applied", checkpoint=checkpoint_id, delta=delta)
            self._save_state(state)
            return state

    # ---------- 代码观察、行为验证与任务门禁 ----------

    def allowed_files(self) -> set[str]:
        return set(self.final_files)

    def workspace_view(self, student_id: str, selected: str | None = None) -> dict[str, Any]:
        state = self._load_state(student_id)
        workspace = self.workspace_path(student_id)
        files = []
        for relative in self.final_files:
            path = workspace / Path(relative)
            if path.is_file():
                files.append({"path": relative, "bytes": path.stat().st_size})
        directories = [
            directory
            for directory in ("static", "templates", "tests")
            if (workspace / directory).is_dir()
        ]
        content = None
        if selected:
            if selected not in self.allowed_files():
                raise PlatformError("只能查看课程清单中的受控文件。")
            path = self._ensure_inside(workspace / Path(selected), workspace)
            if not path.is_file():
                raise PlatformError("当前检查点尚未创建该文件。")
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        return {
            "state": state,
            "files": files,
            "directories": directories,
            "selected": selected,
            "content": content,
        }

    def compare_file(self, checkpoint_id: str, relative_path: str) -> dict[str, Any]:
        if checkpoint_id not in CHECKPOINT_ORDER:
            raise PlatformError("检查点编号无效。")
        current = self.checkpoints[checkpoint_id]
        current_paths = {record["path"] for record in current["files"]}
        if relative_path not in current_paths or relative_path not in self.allowed_files():
            raise PlatformError("该文件不属于此检查点。")
        current_path = self._checkpoint_payload(checkpoint_id) / Path(relative_path)
        position = CHECKPOINT_ORDER.index(checkpoint_id)
        previous_text = ""
        previous_label = "空白"
        if position:
            previous_id = CHECKPOINT_ORDER[position - 1]
            previous_paths = {
                record["path"] for record in self.checkpoints[previous_id]["files"]
            }
            if relative_path in previous_paths:
                previous_path = self._checkpoint_payload(previous_id) / Path(relative_path)
                previous_text = previous_path.read_text(encoding="utf-8-sig")
                previous_label = previous_id
        current_text = current_path.read_text(encoding="utf-8-sig")
        diff = "".join(
            difflib.unified_diff(
                previous_text.splitlines(keepends=True),
                current_text.splitlines(keepends=True),
                fromfile=f"{previous_label}/{relative_path}",
                tofile=f"{checkpoint_id}/{relative_path}",
            )
        )
        return {
            "checkpoint": checkpoint_id,
            "path": relative_path,
            "previous": previous_label,
            "diff": diff or "（与前一检查点内容相同）",
        }

    def _behavior_probe(self, workspace: Path, checkpoint_id: str) -> dict[str, Any]:
        if checkpoint_id in ("C0", "C1"):
            return {"passed": not (workspace / "app.py").exists(), "mode": "not_runnable"}
        mode = "minimal" if checkpoint_id in ("C2", "C3", "C4") else "final"
        probe = r'''import json
from app import create_app
app = create_app({"TESTING": True})
client = app.test_client()
home = client.get("/")
result = {"home_status": home.status_code, "home": home.get_data(as_text=True)}
if "__MODE__" == "final":
    import app as student_app
    labs = client.get("/labs")
    form = client.get("/reservations/new?lab=2")
    result.update({
        "labs_status": labs.status_code,
        "form_status": form.status_code,
        "lab_count": len(student_app.LABS),
        "available_count": sum(1 for item in student_app.LABS if item["status"] == "\u53ef\u9884\u7ea6"),
        "maintenance_count": sum(1 for item in student_app.LABS if item["status"] == "\u7ef4\u62a4\u4e2d"),
        "lab2_selected": 'value="2" selected' in form.get_data(as_text=True),
        "button_disabled": "disabled" in form.get_data(as_text=True),
    })
print(json.dumps(result, ensure_ascii=True))
'''.replace("__MODE__", mode)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        run = self._run_command(
            [sys.executable, "-c", probe], cwd=workspace, check=False, env=env
        )
        if run.returncode != 0:
            return {
                "passed": False,
                "mode": mode,
                "error": (run.stdout + run.stderr).strip(),
            }
        try:
            result = json.loads(run.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return {"passed": False, "mode": mode, "error": run.stdout + run.stderr}
        if mode == "minimal":
            expected = "校园实验室预约系统 dev-v0.1"
            passed = result["home_status"] == 200 and result["home"].strip() == expected
        else:
            passed = (
                result["home_status"] == 200
                and result["labs_status"] == 200
                and result["form_status"] == 200
                and result["lab_count"] == 3
                and result["available_count"] == 2
                and result["maintenance_count"] == 1
                and result["lab2_selected"]
                and result["button_disabled"]
            )
        return {"passed": passed, "mode": mode, "result": result}

    def verify_checkpoint(self, student_id: str, checkpoint_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            task = state["tasks"].get(checkpoint_id)
            if not task or not task["applied"]:
                raise PlatformError("请先应用该检查点。")
            workspace = self.workspace_path(student_id)
            files = self._verify_files(checkpoint_id, workspace)
            behavior = self._behavior_probe(workspace, checkpoint_id)
            result = {
                "passed": files["passed"] and behavior["passed"],
                "files": files,
                "behavior": behavior,
                "time": utc_now(),
            }
            task["verified"] = result["passed"]
            task["verification"] = result
            self._record(
                state, "checkpoint_verified", checkpoint=checkpoint_id, passed=result["passed"]
            )
            self._save_state(state)
            return result

    def complete_task(self, student_id: str, checkpoint_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, checkpoint_id)
            task = state["tasks"][checkpoint_id]
            if not task["applied"]:
                raise PlatformError("请先让平台生成本步文件。")
            if not task.get("action_confirmed"):
                raise PlatformError("请先按清单完成亲手体验。")
            missing = [
                label
                for field, label in (
                    ("prediction", "第1步判断"),
                    ("observation", "实际观察"),
                    ("explanation", "一句话结论"),
                )
                if not task[field]
            ]
            if missing:
                raise PlatformError("请先填写并保存：" + "、".join(missing))
            verification = self.verify_checkpoint(student_id, checkpoint_id)
            state = self._load_state(student_id)
            if not verification["passed"]:
                raise PlatformError("当前文件或可见行为未通过检查，不能完成任务。")
            if checkpoint_id == "C6" and not any(
                item.get("kind") == "empty_collection" for item in state["test_history"]
            ):
                raise PlatformError("请先运行一次测试并观察“尚无测试用例”的结果。")
            if checkpoint_id == "C7":
                if not self._manual_tests_complete(state):
                    raise PlatformError("5项手工验收尚未全部通过。")
                if not self._last_test_passed(state):
                    raise PlatformError("最近一次自动测试必须显示6 passed。")
            if checkpoint_id == "C8":
                raise PlatformError("C8 请使用“冻结 dev-v0.1”完成最终门禁。")
            task = state["tasks"][checkpoint_id]
            task["completed"] = True
            task["completed_at"] = utc_now()
            self._record(state, "task_completed", checkpoint=checkpoint_id)
            self._save_state(state)
            return state

    # ---------- 学生网站进程 ----------

    @staticmethod
    def _free_port(preferred: int = 5001) -> int:
        for port in range(preferred, preferred + 20):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.bind(("127.0.0.1", port))
                except OSError:
                    continue
                return port
        raise PlatformError("5001—5020端口均被占用，请先关闭旧服务。")

    def start_student(self, student_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            current = state["current_checkpoint"]
            if CHECKPOINT_ORDER.index(current) < 2 or not (self.workspace_path(student_id) / "app.py").is_file():
                raise PlatformError("至少应用 C2 后才能启动学生项目。")
            self.stop_student(student_id, record=False)
            port = self._free_port()
            workspace = self.workspace_path(student_id)
            log_path = self.log_root / f"{student_id}_student.log"
            log_handle = log_path.open("ab")
            command = (
                "import os; from app import create_app; app=create_app(); "
                "app.run(host='127.0.0.1', port=int(os.environ['STUDENT_PORT']), "
                "debug=False, use_reloader=False)"
            )
            env = os.environ.copy()
            env["STUDENT_PORT"] = str(port)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            process = subprocess.Popen(
                [sys.executable, "-u", "-c", command],
                cwd=workspace,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                env=env,
                creationflags=creationflags,
            )
            self._processes[student_id] = (process, log_handle, port)
            url = f"http://127.0.0.1:{port}"
            deadline = time.monotonic() + 6
            last_error = ""
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    break
                try:
                    with urllib.request.urlopen(url, timeout=0.5) as response:
                        if response.status == 200:
                            self._record(state, "student_app_started", url=url, pid=process.pid)
                            state["student_server"] = {"url": url, "port": port, "started_at": utc_now()}
                            self._save_state(state)
                            return state["student_server"]
                except Exception as exc:  # 短暂连接失败属于启动轮询的正常状态
                    last_error = str(exc)
                    time.sleep(0.15)
            self.stop_student(student_id, record=False)
            tail = self.read_student_log(student_id, lines=30)
            raise PlatformError(f"学生项目未能启动：{last_error}\n{tail}")

    def stop_student(self, student_id: str, *, record: bool = True) -> bool:
        with self._lock:
            item = self._processes.pop(student_id, None)
            if not item:
                return False
            process, log_handle, port = item
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
            log_handle.close()
            if record and self.state_path(student_id).exists():
                state = self._load_state(student_id)
                self._record(state, "student_app_stopped", port=port)
                state["student_server"] = None
                self._save_state(state)
            return True

    def stop_all(self) -> None:
        for student_id in list(self._processes):
            try:
                self.stop_student(student_id, record=False)
            except Exception:
                pass

    def server_status(self, student_id: str) -> dict[str, Any] | None:
        item = self._processes.get(student_id)
        if not item:
            return None
        process, _, port = item
        if process.poll() is not None:
            self.stop_student(student_id, record=False)
            return None
        return {"running": True, "port": port, "url": f"http://127.0.0.1:{port}"}

    def read_student_log(self, student_id: str, lines: int = 60) -> str:
        self.validate_student_id(student_id)
        path = self._ensure_inside(self.log_root / f"{student_id}_student.log", self.log_root)
        if not path.is_file():
            return "（尚无运行日志）"
        return "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:])

    # ---------- 手工测试与自动测试 ----------

    def save_manual_tests(self, student_id: str, cases: list[dict[str, str]]) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            expected_ids = [item["id"] for item in MANUAL_TEST_SCENARIOS]
            received_ids = [item.get("id", "") for item in cases]
            if received_ids != expected_ids:
                raise PlatformError("手工测试用例编号或顺序不正确。")
            cleaned = []
            for source, scenario in zip(cases, MANUAL_TEST_SCENARIOS):
                conclusion = self._bounded_text(source.get("conclusion"), "测试结论", 20)
                if conclusion not in ("", "通过", "不通过"):
                    raise PlatformError("测试结论只能选择“通过”或“不通过”。")
                cleaned.append(
                    {
                        **scenario,
                        "precondition": self._bounded_text(source.get("precondition"), "前置条件", 1000),
                        "action": self._bounded_text(source.get("action"), "操作", 2000),
                        "expected": self._bounded_text(source.get("expected"), "预期结果", 2000),
                        "actual": self._bounded_text(source.get("actual"), "实际结果", 2000),
                        "conclusion": conclusion,
                    }
                )
            state["manual_tests"] = cleaned
            self._record(
                state,
                "manual_tests_saved",
                complete=self._manual_tests_complete(state),
            )
            self._save_state(state)
            return state

    @staticmethod
    def _manual_tests_complete(state: dict[str, Any]) -> bool:
        cases = state.get("manual_tests", [])
        if len(cases) != len(MANUAL_TEST_SCENARIOS):
            return False
        required = ("precondition", "action", "expected", "actual")
        return all(all(case.get(field, "").strip() for field in required) and case.get("conclusion") == "通过" for case in cases)

    @staticmethod
    def _manual_expectations_ready(state: dict[str, Any]) -> bool:
        cases = state.get("manual_tests", [])
        required = ("precondition", "action", "expected")
        return len(cases) >= 4 and all(
            all(case.get(field, "").strip() for field in required) for case in cases[:4]
        )

    @staticmethod
    def _last_test_passed(state: dict[str, Any]) -> bool:
        result = state.get("last_test") or {}
        return result.get("exit_code") == 0 and result.get("passed_count") == 6

    def run_tests(self, student_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            current = state["current_checkpoint"]
            position = CHECKPOINT_ORDER.index(current)
            if position < 6:
                raise PlatformError("C6 加入测试入口后才能运行本阶段测试。")
            if position >= 7 and not self._manual_expectations_ready(state):
                raise PlatformError("请先填写至少4项手工用例的前置条件、操作和预期。")
            workspace = self.workspace_path(student_id)
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"
            started = utc_now()
            run = self._run_command(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                    "-c",
                    str(self.pytest_config),
                    "--rootdir",
                    str(workspace),
                    "tests",
                ],
                cwd=workspace,
                check=False,
                env=env,
            )
            output = (run.stdout + run.stderr).strip()
            match = TEST_COUNT_PATTERN.search(output)
            passed_count = int(match.group(1)) if match else 0
            if position == 6 and run.returncode == 5 and passed_count == 0:
                kind = "empty_collection"
            elif run.returncode == 0 and passed_count == 6:
                kind = "six_passed"
            else:
                kind = "failure"
            result = {
                "started_at": started,
                "finished_at": utc_now(),
                "exit_code": run.returncode,
                "passed_count": passed_count,
                "kind": kind,
                "output": output,
            }
            state["last_test"] = result
            state["test_history"].append(result)
            self._record(state, "pytest_finished", checkpoint=current, kind=kind, exit_code=run.returncode)
            self._save_state(state)
            return result

    # ---------- 受控故障、终点核对与 Git 冻结 ----------

    def inject_fault(self, student_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, "C8")
            if not state["tasks"]["C8"]["applied"]:
                raise PlatformError("请先应用 C8。")
            if state.get("fault") and state["fault"].get("status") == "injected":
                raise PlatformError("受控故障已经存在，请先观察并恢复。")
            self.stop_student(student_id, record=False)
            workspace = self.workspace_path(student_id)
            source = workspace / "templates" / "index.html"
            if not source.is_file():
                raise PlatformError("首页模板当前已经缺失，不能重复注入故障。")
            backup_dir = self._ensure_inside(self.backup_root / student_id, self.backup_root)
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup = backup_dir / "index.html.before_fault"
            shutil.copyfile(source, backup)
            source.unlink()
            probe = self._behavior_probe(workspace, "C8")
            evidence = probe.get("error", "")
            if "TemplateNotFound" not in evidence:
                shutil.copyfile(backup, source)
                raise PlatformError("没有观察到预期的 TemplateNotFound，故障已自动撤销。")
            state["fault"] = {
                "type": "TemplateNotFound",
                "file": "templates/index.html",
                "status": "injected",
                "injected_at": utc_now(),
                "evidence": evidence[-5000:],
                "diagnosis": "",
            }
            self._record(state, "fault_injected", fault_type="TemplateNotFound")
            self._save_state(state)
            return state["fault"]

    def restore_fault(self, student_id: str, diagnosis: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            fault = state.get("fault")
            if not fault or fault.get("status") != "injected":
                raise PlatformError("当前没有等待恢复的受控故障。")
            explanation = self._bounded_text(diagnosis, "故障判断依据", 3000)
            if not explanation:
                raise PlatformError("请先填写故障现象和判断依据，再恢复。")
            workspace = self.workspace_path(student_id)
            accurate = self._checkpoint_payload("C7") / "templates" / "index.html"
            destination = workspace / "templates" / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(accurate, destination)
            probe = self._behavior_probe(workspace, "C8")
            if not probe["passed"]:
                raise PlatformError("模板已恢复，但页面行为仍未通过，请查看验证结果。")
            fault["status"] = "recovered"
            fault["diagnosis"] = explanation
            fault["recovered_at"] = utc_now()
            fault["recovery_probe"] = probe
            self._record(state, "fault_recovered", diagnosis=explanation)
            self._save_state(state)
            return fault

    def compare_final(self, student_id: str) -> dict[str, Any]:
        self._load_state(student_id)
        workspace = self.workspace_path(student_id)
        rows = []
        passed = True
        for relative_path in self.final_files:
            mine = workspace / Path(relative_path)
            answer = self.checkpoint_root.parents[1] / "版本终点核对包" / "dev-v0.1" / Path(relative_path)
            if not mine.is_file() or not answer.is_file():
                same = False
                detail = "个人文件或终点文件缺失"
            else:
                same = normalized_text(mine.read_bytes()) == normalized_text(answer.read_bytes())
                detail = "PASS" if same else "内容不同"
            rows.append({"path": relative_path, "passed": same, "detail": detail})
            passed = passed and same
        return {"passed": passed, "count": len(rows), "rows": rows, "time": utc_now()}

    def freeze_release(self, student_id: str, commit_message: str) -> dict[str, Any]:
        with self._lock:
            state = self._load_state(student_id)
            self._require_active(state, "C8")
            task = state["tasks"]["C8"]
            if not task["applied"]:
                raise PlatformError("请先进入 C8 故障恢复与发布阶段。")
            if not task.get("action_confirmed"):
                raise PlatformError("请先完成故障恢复、回归测试并确认亲手操作。")
            for field, label in (
                ("prediction", "第1步判断"),
                ("observation", "实际观察"),
                ("explanation", "一句话结论"),
            ):
                if not task[field]:
                    raise PlatformError(f"请先填写并保存{label}。")
            fault = state.get("fault") or {}
            if fault.get("status") != "recovered":
                raise PlatformError("必须先完成受控故障的观察、判断和恢复。")
            if not self._manual_tests_complete(state):
                raise PlatformError("5项手工验收必须全部通过。")
            if not self._last_test_passed(state):
                raise PlatformError("故障恢复后必须重新得到6 passed。")
            if state["last_test"]["finished_at"] < fault["recovered_at"]:
                raise PlatformError("当前6 passed早于故障恢复，请重新运行回归测试。")
            message = self._bounded_text(commit_message, "提交说明", 200)
            if not message:
                raise PlatformError("请输入本次里程碑的提交说明。")

            self.stop_student(student_id, record=False)
            verification = self.verify_checkpoint(student_id, "C8")
            state = self._load_state(student_id)
            final_compare = self.compare_final(student_id)
            if not verification["passed"] or not final_compare["passed"]:
                raise PlatformError("13文件或页面行为核对未通过，不能冻结版本。")
            workspace = self.workspace_path(student_id)
            existing = self._run_command(
                ["git", "tag", "--list", "dev-v0.1"], cwd=workspace
            ).stdout.strip()
            if existing:
                raise PlatformError("dev-v0.1标签已经存在，平台不会移动已有标签。")
            self._run_command(["git", "add", "--", *self.final_files], cwd=workspace)
            status_before = self._git_status(workspace)
            unexpected = [line for line in status_before.splitlines() if line.startswith("??")]
            if unexpected:
                raise PlatformError("存在课程清单外的未跟踪文件，请先处理：" + "；".join(unexpected))
            self._run_command(["git", "commit", "-m", message], cwd=workspace)
            self._run_command(
                ["git", "tag", "-a", "dev-v0.1", "-m", "Complete development version 0.1"],
                cwd=workspace,
            )
            commit = self._git_head(workspace)
            tagged_commit = self._run_command(
                ["git", "rev-parse", "dev-v0.1^{}"], cwd=workspace
            ).stdout.strip()
            status_after = self._git_status(workspace)
            if status_after or tagged_commit != commit:
                raise PlatformError("提交或标签验证失败，请教师检查工作区。")

            state["git_result"].update(
                {
                    "v01_commit": commit,
                    "tag": "dev-v0.1",
                    "tagged_commit": tagged_commit,
                    "status_clean": True,
                    "message": message,
                    "frozen_at": utc_now(),
                }
            )
            task = state["tasks"]["C8"]
            task["verified"] = True
            task["verification"] = verification
            task["completed"] = True
            task["completed_at"] = utc_now()
            state["final_compare"] = final_compare
            self._record(state, "release_frozen", tag="dev-v0.1", commit=commit)
            self._save_state(state)
            return state["git_result"]

    # ---------- 证据包 ----------

    def export_evidence(self, student_id: str) -> Path:
        with self._lock:
            state = self._load_state(student_id)
            if not state["tasks"]["C8"]["completed"]:
                raise PlatformError("完成并冻结 dev-v0.1 后才能导出证据包。")
            final = self.compare_final(student_id)
            student_export_root = self._ensure_inside(self.export_root / student_id, self.export_root)
            student_export_root.mkdir(parents=True, exist_ok=True)
            destination = student_export_root / f"{student_id}_dev-v0.1_学习证据.zip"
            state["export_result"] = {
                "path": str(destination),
                "exported_at": utc_now(),
                "archive_name": destination.name,
            }
            self._record(state, "evidence_exported", archive=destination.name)
            self._save_state(state)

            markdown = self._build_report_markdown(state, final)
            csv_buffer = io.StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=("path", "passed", "detail"))
            writer.writeheader()
            writer.writerows(final["rows"])
            test_output = (state.get("last_test") or {}).get("output", "（尚无测试输出）")
            with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("学习报告.md", markdown.encode("utf-8"))
                archive.writestr(
                    "state.json",
                    (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
                )
                archive.writestr("自动测试输出.txt", test_output.encode("utf-8"))
                archive.writestr("终点文件核对.csv", ("\ufeff" + csv_buffer.getvalue()).encode("utf-8"))
            return destination

    def _build_report_markdown(self, state: dict[str, Any], final: dict[str, Any]) -> str:
        lines = [
            "# S0到dev-v0.1个人学习报告",
            "",
            f"- 学号：{state['profile']['student_id']}",
            f"- 姓名：{state['profile']['name']}",
            f"- 起点提交：{state['git_result'].get('s0_commit', '')}",
            f"- 终点提交：{state['git_result'].get('v01_commit', '')}",
            f"- 正式标签：{state['git_result'].get('tag', '')}",
            f"- 自动测试：{(state.get('last_test') or {}).get('passed_count', 0)} passed",
            f"- 终点核对：{final['count']}个文件，{'通过' if final['passed'] else '未通过'}",
            "",
            "## C0—C8学习记录",
            "",
        ]
        for checkpoint_id in CHECKPOINT_ORDER:
            task = state["tasks"][checkpoint_id]
            lines.extend(
                [
                    f"### {checkpoint_id} {TASKS[checkpoint_id]['title']}",
                    "",
                    f"- 事前判断：{task['prediction']}",
                    f"- 实际核对：{task['observation']}",
                    f"- 一句话结论：{task['explanation']}",
                    f"- 完成时间：{task.get('completed_at') or ''}",
                    "",
                ]
            )
        lines.extend(["## 手工测试", ""])
        for case in state["manual_tests"]:
            lines.extend(
                [
                    f"### {case['id']} {case['title']}",
                    "",
                    f"- 前置条件：{case['precondition']}",
                    f"- 操作：{case['action']}",
                    f"- 预期：{case['expected']}",
                    f"- 实际：{case['actual']}",
                    f"- 结论：{case['conclusion']}",
                    "",
                ]
            )
        fault = state.get("fault") or {}
        lines.extend(
            [
                "## 故障与恢复",
                "",
                f"- 故障类型：{fault.get('type', '')}",
                f"- 学生判断：{fault.get('diagnosis', '')}",
                f"- 恢复时间：{fault.get('recovered_at', '')}",
                "",
                "## 操作时间线",
                "",
            ]
        )
        for item in state["actions"]:
            lines.append(f"- {item['time']}：{item['action']}")
        lines.append("")
        return "\n".join(lines)

    # ---------- 命令与 Git ----------

    @staticmethod
    def _run_command(
        command: list[str],
        *,
        cwd: Path,
        check: bool = True,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise PlatformError(f"命令无法执行：{' '.join(command)}；{exc}") from exc
        if check and result.returncode != 0:
            detail = (result.stdout + result.stderr).strip()
            raise PlatformError(f"命令执行失败：{' '.join(command)}\n{detail}")
        return result

    def _initialize_git(self, workspace: Path, student_id: str) -> None:
        result = self._run_command(["git", "init", "-b", "main"], cwd=workspace, check=False)
        if result.returncode != 0:
            self._run_command(["git", "init"], cwd=workspace)
        self._run_command(["git", "config", "user.name", f"课程学生 {student_id}"], cwd=workspace)
        self._run_command(
            ["git", "config", "user.email", f"{student_id}@course.local"], cwd=workspace
        )
        s0_files = [item["path"] for item in self.checkpoints["C0"]["files"]]
        self._run_command(["git", "add", "--", *s0_files], cwd=workspace)
        self._run_command(["git", "commit", "-m", "chore: establish S0 baseline"], cwd=workspace)
        if self._git_status(workspace):
            raise PlatformError("S0提交后工作区不干净，已停止创建。")

    def _git_head(self, workspace: Path) -> str:
        return self._run_command(["git", "rev-parse", "HEAD"], cwd=workspace).stdout.strip()

    def _git_status(self, workspace: Path) -> str:
        return self._run_command(
            ["git", "status", "--porcelain", "--untracked-files=all"], cwd=workspace
        ).stdout.strip()
