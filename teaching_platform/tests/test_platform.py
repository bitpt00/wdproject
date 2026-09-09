from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

import pytest

from teaching_platform.app import create_app
from teaching_platform.content import CHECKPOINT_ORDER, MANUAL_TEST_SCENARIOS, TASKS
from teaching_platform.engine import PlatformError, TeachingEngine


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_ROOT = REPOSITORY_ROOT / "教学资源" / "平台检查点" / "S0到V0.1"


@pytest.fixture()
def engine(tmp_path: Path) -> TeachingEngine:
    instance = TeachingEngine(tmp_path / "runtime", CHECKPOINT_ROOT)
    yield instance
    instance.stop_all()


def save_guided_records(engine: TeachingEngine, student_id: str, checkpoint_id: str) -> None:
    guide = TASKS[checkpoint_id]["guide"]
    engine.save_prediction(
        student_id, checkpoint_id, guide["prediction"]["answer"]
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
    save_guided_records(engine, student_id, checkpoint_id)
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
    engine.confirm_action(student_id, checkpoint_id)
    observation_ids = [
        item["id"] for item in TASKS[checkpoint_id]["guide"]["observation"]["items"]
    ]
    engine.save_observation(student_id, checkpoint_id, observation_ids)
    engine.save_explanation(
        student_id,
        checkpoint_id,
        f"{checkpoint_id} 中我通过实际操作确认了文件、页面与程序连接关系。",
    )
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
    save_guided_records(engine, student_id, "C8")
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
    engine.confirm_action(student_id, "C8")
    engine.save_observation(
        student_id,
        "C8",
        [item["id"] for item in TASKS["C8"]["guide"]["observation"]["items"]],
    )
    engine.save_explanation(
        student_id,
        "C8",
        "恢复模板只能消除当前错误，重新回归测试才能确认其他页面没有受到影响。",
    )


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
    with pytest.raises(PlatformError, match="第1步选择题"):
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
    save_guided_records(engine, "PT06", "C2")
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
    assert "你现在要做什么" in response.get_data(as_text=True)
    response = client1.post(
        "/task/C0/prediction", data={"choice": "B"}, follow_redirects=True
    )
    assert "B. 不能启动网站" in response.get_data(as_text=True)
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
    assert "B. 不能启动网站" in page
    assert 'data-phase="experience"' in page
    app2.extensions["teaching_engine"].stop_all()


def test_pt16_task_page_reveals_only_the_current_student_action(tmp_path: Path) -> None:
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "guided-ui-test",
            "RUNTIME_ROOT": tmp_path / "guided-ui-runtime",
            "CHECKPOINT_ROOT": CHECKPOINT_ROOT,
        }
    )
    client = app.test_client()
    client.post("/enter", data={"student_id": "PT16", "name": "向导学生"})

    page = client.get("/task/C0").get_data(as_text=True)
    assert 'data-phase="predict"' in page
    assert "如果现在就尝试启动网站" in page
    assert 'name="choice"' in page
    assert 'name="observations"' not in page
    assert 'name="explanation"' not in page
    assert "教师讲解的关键知识" not in page

    tests_page = client.get("/tests").get_data(as_text=True)
    assert "当前关卡不需要填写测试记录" in tests_page
    assert 'name="case_0_expected"' not in tests_page
    app.extensions["teaching_engine"].stop_all()


def test_pt17_c0_saves_each_record_and_unlocks_the_next_step(tmp_path: Path) -> None:
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "guided-save-test",
            "RUNTIME_ROOT": tmp_path / "guided-save-runtime",
            "CHECKPOINT_ROOT": CHECKPOINT_ROOT,
        }
    )
    client = app.test_client()
    client.post("/enter", data={"student_id": "PT17", "name": "保存学生"})

    response = client.post(
        "/task/C0/prediction", data={"choice": "B"}, follow_redirects=True
    )
    page = response.get_data(as_text=True)
    assert "已保存你的选择" in page
    assert "B. 不能启动网站" in page
    assert 'data-phase="experience"' in page
    assert 'name="observations"' not in page

    response = client.post("/task/C0/action-confirmed", follow_redirects=True)
    page = response.get_data(as_text=True)
    assert "你完成了亲手操作" in page
    assert 'data-phase="observe"' in page
    assert 'name="observations"' in page
    assert 'name="explanation"' not in page

    observations = [
        item["id"] for item in TASKS["C0"]["guide"]["observation"]["items"]
    ]
    response = client.post(
        "/task/C0/observation",
        data={"observations": observations},
        follow_redirects=True,
    )
    page = response.get_data(as_text=True)
    assert "已保存 3 项实际观察" in page
    assert 'data-phase="explain"' in page
    assert 'name="observations"' not in page
    assert 'name="explanation"' in page

    answer = "S0 已准备依赖和环境入口，但没有 app.py，所以不能向浏览器提供页面。"
    response = client.post(
        "/task/C0/explanation",
        data={"explanation": answer},
        follow_redirects=True,
    )
    page = response.get_data(as_text=True)
    assert "一句话结论已保存" in page
    assert answer in page
    assert 'data-phase="finish"' in page
    app.extensions["teaching_engine"].stop_all()


def test_pt18_old_invalid_three_box_completion_is_preserved_but_reset(
    engine: TeachingEngine,
) -> None:
    state, _ = engine.create_or_continue("PT18", "迁移学生")
    state["schema_version"] = 1
    state["tasks"]["C0"].update(
        {
            "prediction": "旧版预测",
            "observation": "旧版预测",
            "explanation": "旧版预测",
            "completed": True,
            "completed_at": "2026-09-09T00:00:00+00:00",
        }
    )
    engine._save_state(state)

    upgraded = engine.get_state("PT18")
    task = upgraded["tasks"]["C0"]
    assert upgraded["schema_version"] == 2
    assert task["legacy_reflections"] == {
        "prediction": "旧版预测",
        "observation": "旧版预测",
        "explanation": "旧版预测",
    }
    assert task["prediction"] == ""
    assert task["observation"] == ""
    assert task["explanation"] == ""
    assert task["completed"] is False
    assert engine.task_phase(upgraded, "C0") == "predict"
