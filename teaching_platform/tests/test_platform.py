from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

import pytest

from teaching_platform.app import create_app
from teaching_platform.content import CHECKPOINT_ORDER, MANUAL_TEST_SCENARIOS
from teaching_platform.engine import PlatformError, TeachingEngine


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_ROOT = REPOSITORY_ROOT / "教学资源" / "平台检查点" / "S0到V0.1"


@pytest.fixture()
def engine(tmp_path: Path) -> TeachingEngine:
    instance = TeachingEngine(tmp_path / "runtime", CHECKPOINT_ROOT)
    yield instance
    instance.stop_all()


def save_reflections(engine: TeachingEngine, student_id: str, checkpoint_id: str) -> None:
    engine.save_reflections(
        student_id,
        checkpoint_id,
        f"{checkpoint_id}操作前预测：我先判断文件和页面变化。",
        f"{checkpoint_id}操作后观察：实际结果与检查点说明一致。",
        f"{checkpoint_id}原理解释：文件必须经过路由或工具调用才产生效果。",
    )


def save_passing_manual_tests(engine: TeachingEngine, student_id: str) -> None:
    cases = []
    for scenario in MANUAL_TEST_SCENARIOS:
        cases.append(
            {
                "id": scenario["id"],
                "precondition": "学生项目已经启动且浏览器可以访问。",
                "action": scenario["suggested_action"],
                "expected": f"{scenario['title']}符合S06规定结果。",
                "actual": "已亲自操作，页面结果与预期一致。",
                "conclusion": "通过",
            }
        )
    engine.save_manual_tests(student_id, cases)


def complete_one(engine: TeachingEngine, student_id: str, checkpoint_id: str) -> None:
    save_reflections(engine, student_id, checkpoint_id)
    if checkpoint_id == "C7":
        save_passing_manual_tests(engine, student_id)
    if checkpoint_id != "C0":
        engine.apply_checkpoint(student_id, checkpoint_id)
    if checkpoint_id == "C6":
        result = engine.run_tests(student_id)
        assert result["kind"] == "empty_collection"
    if checkpoint_id == "C7":
        result = engine.run_tests(student_id)
        assert result["passed_count"] == 6
    engine.complete_task(student_id, checkpoint_id)


def advance_through(
    engine: TeachingEngine, student_id: str, final_checkpoint: str
) -> dict:
    state, _ = engine.create_or_continue(student_id, "测试学生")
    final_position = CHECKPOINT_ORDER.index(final_checkpoint)
    for checkpoint_id in CHECKPOINT_ORDER[: final_position + 1]:
        if not state["tasks"][checkpoint_id]["completed"]:
            complete_one(engine, student_id, checkpoint_id)
            state = engine.get_state(student_id)
    return state


def prepare_c8(engine: TeachingEngine, student_id: str) -> dict:
    advance_through(engine, student_id, "C7")
    save_reflections(engine, student_id, "C8")
    engine.apply_checkpoint(student_id, "C8")
    return engine.get_state(student_id)


def restore_and_regress(engine: TeachingEngine, student_id: str) -> None:
    engine.inject_fault(student_id)
    engine.restore_fault(
        student_id,
        "错误明确为TemplateNotFound，检查后发现templates/index.html缺失。",
    )
    result = engine.run_tests(student_id)
    assert result["exit_code"] == 0
    assert result["passed_count"] == 6


def test_pt01_rejects_illegal_student_id_and_path_traversal(engine: TeachingEngine) -> None:
    for value in ("../escape", "..\\escape", "A/B", "A B", ""):
        with pytest.raises(PlatformError):
            engine.create_or_continue(value, "越界测试")
    assert not list(engine.state_root.glob("*.json"))
    assert not list(engine.workspace_root.iterdir())


def test_pt02_creates_only_s0_and_clean_git_baseline(engine: TeachingEngine) -> None:
    state, created = engine.create_or_continue("PT02", "起点学生")
    workspace = engine.workspace_path("PT02")
    files = sorted(
        path.relative_to(workspace).as_posix()
        for path in workspace.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(workspace).parts
    )
    assert created is True
    assert files == [".gitignore", "requirements.txt", "初始化开发环境.bat"]
    assert state["current_checkpoint"] == "C0"
    assert state["git_result"]["s0_commit"]
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=workspace, text=True, capture_output=True
    )
    assert status.stdout.strip() == ""


def test_pt03_refuses_to_skip_previous_checkpoint(engine: TeachingEngine) -> None:
    engine.create_or_continue("PT03", "顺序学生")
    with pytest.raises(PlatformError, match="不能跳过"):
        engine.apply_checkpoint("PT03", "C2")
    assert not (engine.workspace_path("PT03") / "app.py").exists()


def test_pt04_requires_prediction_before_applying(engine: TeachingEngine) -> None:
    advance_through(engine, "PT04", "C0")
    engine.save_reflections("PT04", "C1", "", "", "")
    with pytest.raises(PlatformError, match="操作前预测"):
        engine.apply_checkpoint("PT04", "C1")
    assert not (engine.workspace_path("PT04") / "static").exists()


def test_pt05_applies_c0_to_c8_snapshots_in_order(engine: TeachingEngine) -> None:
    prepare_c8(engine, "PT05")
    workspace = engine.workspace_path("PT05")
    expected_counts = [3, 3, 5, 8, 9, 10, 12, 13, 13]
    assert [len(engine.checkpoints[item]["files"]) for item in CHECKPOINT_ORDER] == expected_counts
    assert len([path for path in engine.final_files if (workspace / path).is_file()]) == 13
    assert engine.get_state("PT05")["current_checkpoint"] == "C8"


def test_pt06_c2_returns_the_minimal_text_page(engine: TeachingEngine) -> None:
    advance_through(engine, "PT06", "C1")
    save_reflections(engine, "PT06", "C2")
    engine.apply_checkpoint("PT06", "C2")
    result = engine.verify_checkpoint("PT06", "C2")
    assert result["passed"] is True
    assert result["behavior"]["mode"] == "minimal"
    assert result["behavior"]["result"]["home"].strip() == "校园实验室预约系统 dev-v0.1"


def test_pt07_c3_and_c4_remain_preparation_steps(engine: TeachingEngine) -> None:
    advance_through(engine, "PT07", "C4")
    state = engine.get_state("PT07")
    assert state["tasks"]["C3"]["verification"]["behavior"]["mode"] == "minimal"
    assert state["tasks"]["C4"]["verification"]["behavior"]["mode"] == "minimal"
    assert (engine.workspace_path("PT07") / "templates" / "labs.html").is_file()


def test_pt08_c5_has_three_pages_and_lab2_selection(engine: TeachingEngine) -> None:
    advance_through(engine, "PT08", "C5")
    result = engine.get_state("PT08")["tasks"]["C5"]["verification"]["behavior"]
    assert result["mode"] == "final"
    assert result["result"]["lab_count"] == 3
    assert result["result"]["lab2_selected"] is True
    assert result["result"]["button_disabled"] is True


def test_pt09_c7_runs_the_real_six_tests(engine: TeachingEngine) -> None:
    state = advance_through(engine, "PT09", "C7")
    assert state["last_test"]["exit_code"] == 0
    assert state["last_test"]["passed_count"] == 6
    assert "6 passed" in state["last_test"]["output"]


def test_pt10_fault_is_backed_up_and_template_not_found_is_observed(engine: TeachingEngine) -> None:
    prepare_c8(engine, "PT10")
    fault = engine.inject_fault("PT10")
    assert fault["status"] == "injected"
    assert "TemplateNotFound" in fault["evidence"]
    assert not (engine.workspace_path("PT10") / "templates" / "index.html").exists()
    assert (engine.backup_root / "PT10" / "index.html.before_fault").is_file()


def test_pt11_fault_recovery_requires_diagnosis_and_regression(engine: TeachingEngine) -> None:
    prepare_c8(engine, "PT11")
    engine.inject_fault("PT11")
    with pytest.raises(PlatformError, match="先填写"):
        engine.restore_fault("PT11", "")
    engine.restore_fault("PT11", "TemplateNotFound说明首页模板不在规定目录。")
    result = engine.run_tests("PT11")
    assert result["passed_count"] == 6
    assert (engine.workspace_path("PT11") / "templates" / "index.html").is_file()


def test_pt12_c8_matches_all_thirteen_endpoint_files(engine: TeachingEngine) -> None:
    prepare_c8(engine, "PT12")
    restore_and_regress(engine, "PT12")
    result = engine.compare_final("PT12")
    assert result["passed"] is True
    assert result["count"] == 13
    assert all(row["passed"] for row in result["rows"])


def test_pt13_freezes_clean_git_tag_at_current_commit(engine: TeachingEngine) -> None:
    prepare_c8(engine, "PT13")
    restore_and_regress(engine, "PT13")
    result = engine.freeze_release("PT13", "feat: complete static prototype for dev-v0.1")
    assert result["tag"] == "dev-v0.1"
    assert result["tagged_commit"] == result["v01_commit"]
    assert result["status_clean"] is True
    assert engine.active_checkpoint(engine.get_state("PT13")) is None


def test_pt14_exports_four_required_evidence_files(engine: TeachingEngine) -> None:
    prepare_c8(engine, "PT14")
    restore_and_regress(engine, "PT14")
    engine.freeze_release("PT14", "feat: complete static prototype for dev-v0.1")
    archive = engine.export_evidence("PT14")
    assert archive.is_file()
    with zipfile.ZipFile(archive) as package:
        assert sorted(package.namelist()) == [
            "state.json",
            "学习报告.md",
            "终点文件核对.csv",
            "自动测试输出.txt",
        ]
        assert "6 passed" in package.read("自动测试输出.txt").decode("utf-8")


def test_pt15_saved_state_continues_after_platform_restart(tmp_path: Path) -> None:
    runtime = tmp_path / "persistent-runtime"
    app1 = create_app(
        {"TESTING": True, "SECRET_KEY": "test", "RUNTIME_ROOT": runtime, "CHECKPOINT_ROOT": CHECKPOINT_ROOT}
    )
    client1 = app1.test_client()
    response = client1.post(
        "/enter", data={"student_id": "PT15", "name": "重启学生"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert "S0→dev-v0.1 任务总览" in response.get_data(as_text=True)
    app1.extensions["teaching_engine"].stop_all()

    app2 = create_app(
        {"TESTING": True, "SECRET_KEY": "test", "RUNTIME_ROOT": runtime, "CHECKPOINT_ROOT": CHECKPOINT_ROOT}
    )
    client2 = app2.test_client()
    response = client2.post(
        "/enter", data={"student_id": "PT15", "name": "重启学生"}, follow_redirects=True
    )
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "已继续原有学习进度" in page
    assert "PT15 · 重启学生" in page
    app2.extensions["teaching_engine"].stop_all()
