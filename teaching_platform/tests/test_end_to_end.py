from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

from teaching_platform.app import create_app
from teaching_platform.content import MANUAL_TEST_SCENARIOS, TASKS


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_ROOT = REPOSITORY_ROOT / "教学资源" / "平台检查点" / "S0到V0.1"


def post_ok(client, path: str, data: dict[str, str] | None = None):
    response = client.post(path, data=data or {}, follow_redirects=True)
    assert response.status_code == 200
    return response


def save_prediction(client, checkpoint_id: str):
    answer = TASKS[checkpoint_id]["guide"]["prediction"]["answer"]
    return post_ok(
        client, f"/task/{checkpoint_id}/prediction", {"choice": answer}
    )


def finish_guided_records(client, checkpoint_id: str) -> None:
    post_ok(client, f"/task/{checkpoint_id}/action-confirmed")
    observation_data = {
        "observations": [
            item["id"]
            for item in TASKS[checkpoint_id]["guide"]["observation"]["items"]
        ]
    }
    response = client.post(
        f"/task/{checkpoint_id}/observation",
        data=observation_data,
        follow_redirects=True,
    )
    assert response.status_code == 200
    post_ok(
        client,
        f"/task/{checkpoint_id}/explanation",
        {
            "explanation": (
                f"{checkpoint_id} 中我通过亲手操作确认了文件、页面和运行结果之间的关系。"
            )
        },
    )


def manual_test_form() -> dict[str, str]:
    data: dict[str, str] = {}
    expected_results = (
        "显示系统名称、版本和三个业务说明。",
        "显示3间实验室，其中2间可预约、1间维护中。",
        "打开表单且人工智能实验室已选中。",
        "提交按钮禁用，页面说明当前版本不保存。",
        "三个页面均显示首页、实验室和预约申请导航。",
    )
    for index, (scenario, expected) in enumerate(
        zip(MANUAL_TEST_SCENARIOS, expected_results)
    ):
        prefix = f"case_{index}_"
        data[prefix + "precondition"] = "学生网站已启动，使用未登录浏览器访问。"
        data[prefix + "action"] = scenario["suggested_action"]
        data[prefix + "expected"] = expected
        data[prefix + "actual"] = "我已亲自操作，实际页面与预期一致。"
        data[prefix + "conclusion"] = "通过"
    return data


def test_clean_student_completes_the_entire_browser_workflow(tmp_path: Path) -> None:
    runtime = tmp_path / "fresh-student-runtime"
    config = {
        "TESTING": True,
        "SECRET_KEY": "end-to-end-test",
        "RUNTIME_ROOT": runtime,
        "CHECKPOINT_ROOT": CHECKPOINT_ROOT,
    }
    app = create_app(config)
    engine = app.extensions["teaching_engine"]
    client = app.test_client()

    response = post_ok(
        client,
        "/enter",
        {"student_id": "ACCEPT001", "name": "全流程验收学生"},
    )
    assert "个人工作区已创建" in response.get_data(as_text=True)

    for checkpoint_id in ("C0", "C1"):
        save_prediction(client, checkpoint_id)
        if checkpoint_id != "C0":
            post_ok(client, f"/task/{checkpoint_id}/apply")
        finish_guided_records(client, checkpoint_id)
        post_ok(client, f"/task/{checkpoint_id}/complete")

    save_prediction(client, "C2")
    post_ok(client, "/task/C2/apply")
    workspace_page = client.get("/workspace?file=app.py")
    assert workspace_page.status_code == 200
    assert "def create_app" in workspace_page.get_data(as_text=True)
    post_ok(client, "/student/start", {"return_to": "/task/C2"})
    server = engine.server_status("ACCEPT001")
    assert server and server["running"]
    with urllib.request.urlopen(server["url"], timeout=3) as page:
        assert page.status == 200
        assert "校园实验室预约系统 dev-v0.1" in page.read().decode("utf-8")
    post_ok(client, "/student/stop", {"return_to": "/task/C2"})
    finish_guided_records(client, "C2")
    post_ok(client, "/task/C2/complete")

    for checkpoint_id in ("C3", "C4", "C5"):
        save_prediction(client, checkpoint_id)
        post_ok(client, f"/task/{checkpoint_id}/apply")
        response = client.get(f"/task/{checkpoint_id}")
        assert response.status_code == 200
        finish_guided_records(client, checkpoint_id)
        post_ok(client, f"/task/{checkpoint_id}/complete")

    save_prediction(client, "C6")
    post_ok(client, "/task/C6/apply")
    response = post_ok(client, "/tests/run")
    assert "尚无测试用例" in response.get_data(as_text=True)
    assert engine.get_state("ACCEPT001")["last_test"]["kind"] == "empty_collection"
    finish_guided_records(client, "C6")
    post_ok(client, "/task/C6/complete")

    post_ok(client, "/tests/save", manual_test_form())
    state = engine.get_state("ACCEPT001")
    assert all(item["conclusion"] == "通过" for item in state["manual_tests"])
    save_prediction(client, "C7")
    post_ok(client, "/task/C7/apply")
    response = post_ok(client, "/tests/run")
    assert "6 passed" in response.get_data(as_text=True)
    finish_guided_records(client, "C7")
    post_ok(client, "/task/C7/complete")

    save_prediction(client, "C8")
    post_ok(client, "/task/C8/apply")
    response = post_ok(client, "/fault/inject")
    assert "TemplateNotFound" in response.get_data(as_text=True)
    response = post_ok(
        client,
        "/fault/restore",
        {"diagnosis": "错误显示TemplateNotFound，检查文件树发现templates/index.html缺失。"},
    )
    assert "故障已恢复" in response.get_data(as_text=True)
    post_ok(client, "/tests/run")
    assert engine.get_state("ACCEPT001")["last_test"]["passed_count"] == 6
    finish_guided_records(client, "C8")

    response = post_ok(
        client,
        "/release/freeze",
        {"commit_message": "feat: complete static prototype for dev-v0.1"},
    )
    page = response.get_data(as_text=True)
    assert "dev-v0.1" in page
    assert "13文件终点核对" in page

    archive_response = client.post("/report/export")
    assert archive_response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(archive_response.data)) as archive:
        assert set(archive.namelist()) == {
            "学习报告.md",
            "state.json",
            "自动测试输出.txt",
            "终点文件核对.csv",
        }
        report = archive.read("学习报告.md").decode("utf-8")
        assert "ACCEPT001" in report
        assert "dev-v0.1" in report
        assert "6 passed" in report

    engine.stop_all()
    restarted_app = create_app(config)
    restarted_client = restarted_app.test_client()
    response = post_ok(
        restarted_client,
        "/enter",
        {"student_id": "ACCEPT001", "name": "全流程验收学生"},
    )
    page = response.get_data(as_text=True)
    assert "已继续原有学习进度" in page
    assert "9/9" in page
    restarted_app.extensions["teaching_engine"].stop_all()
