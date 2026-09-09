"""S0→dev-v0.1 半自动教学平台的本地 Web 入口。"""

from __future__ import annotations

import os
import threading
import webbrowser
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from .content import CHECKPOINT_ORDER, MANUAL_TEST_SCENARIOS, TASKS
from .engine import PlatformError, TeachingEngine


PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_ROOT.parent
DEFAULT_CHECKPOINT_ROOT = REPOSITORY_ROOT / "教学资源" / "平台检查点" / "S0到V0.1"


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="local-s0-to-v01-teaching-platform",
        RUNTIME_ROOT=PACKAGE_ROOT / "runtime",
        CHECKPOINT_ROOT=DEFAULT_CHECKPOINT_ROOT,
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    engine = TeachingEngine(
        Path(app.config["RUNTIME_ROOT"]), Path(app.config["CHECKPOINT_ROOT"])
    )
    app.extensions["teaching_engine"] = engine

    def current_student_id() -> str | None:
        return session.get("student_id")

    def require_student(view: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(view)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            if not current_student_id():
                flash("请先输入学号和姓名，创建或继续个人工作区。", "warning")
                return redirect(url_for("index"))
            return view(*args, **kwargs)

        return wrapped

    @app.context_processor
    def inject_common() -> dict[str, Any]:
        return {
            "checkpoint_order": CHECKPOINT_ORDER,
            "task_definitions": TASKS,
            "current_student_id": current_student_id(),
        }

    @app.errorhandler(PlatformError)
    def handle_platform_error(error: PlatformError) -> Any:
        flash(str(error), "error")
        return redirect(request.referrer or url_for("index"))

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "scope": "S0-to-dev-v0.1"}

    @app.get("/")
    def index() -> str:
        existing = None
        student_id = current_student_id()
        if student_id:
            try:
                existing = engine.get_state(student_id)
            except PlatformError:
                session.clear()
        return render_template("index.html", existing=existing)

    @app.post("/enter")
    def enter() -> Any:
        state, created = engine.create_or_continue(
            request.form.get("student_id", ""), request.form.get("name", "")
        )
        session["student_id"] = state["profile"]["student_id"]
        flash("个人工作区已创建，S0基线已建立。" if created else "已继续原有学习进度。", "success")
        return redirect(url_for("dashboard"))

    @app.post("/leave")
    @require_student
    def leave() -> Any:
        student_id = current_student_id()
        if student_id:
            engine.stop_student(student_id)
        session.clear()
        flash("已退出当前学生工作区，学习记录仍保存在本机。", "success")
        return redirect(url_for("index"))

    @app.get("/dashboard")
    @require_student
    def dashboard() -> str:
        student_id = current_student_id()
        state = engine.get_state(student_id)
        return render_template(
            "dashboard.html",
            state=state,
            statuses=engine.task_statuses(state),
            server=engine.server_status(student_id),
        )

    @app.get("/task/<checkpoint_id>")
    @require_student
    def task(checkpoint_id: str) -> Any:
        if checkpoint_id not in CHECKPOINT_ORDER:
            raise PlatformError("检查点编号无效。")
        student_id = current_student_id()
        state = engine.get_state(student_id)
        status = next(item for item in engine.task_statuses(state) if item["id"] == checkpoint_id)
        if status["status"] == "locked":
            raise PlatformError("该任务尚未解锁，请按 C0—C8 顺序完成。")
        checkpoint = engine.checkpoints[checkpoint_id]
        return render_template(
            "task.html",
            checkpoint_id=checkpoint_id,
            definition=TASKS[checkpoint_id],
            checkpoint=checkpoint,
            task_state=state["tasks"][checkpoint_id],
            status=status,
            state=state,
            server=engine.server_status(student_id),
            log=engine.read_student_log(student_id),
        )

    @app.post("/task/<checkpoint_id>/reflections")
    @require_student
    def save_reflections(checkpoint_id: str) -> Any:
        engine.save_reflections(
            current_student_id(),
            checkpoint_id,
            request.form.get("prediction", ""),
            request.form.get("observation", ""),
            request.form.get("explanation", ""),
        )
        flash("思考记录已保存。", "success")
        return redirect(url_for("task", checkpoint_id=checkpoint_id))

    @app.post("/task/<checkpoint_id>/apply")
    @require_student
    def apply_checkpoint(checkpoint_id: str) -> Any:
        engine.apply_checkpoint(current_student_id(), checkpoint_id)
        flash(f"{checkpoint_id} 已准确应用。请亲自操作并记录观察。", "success")
        return redirect(url_for("task", checkpoint_id=checkpoint_id))

    @app.post("/task/<checkpoint_id>/verify")
    @require_student
    def verify_checkpoint(checkpoint_id: str) -> Any:
        result = engine.verify_checkpoint(current_student_id(), checkpoint_id)
        flash("文件与可见行为均通过检查。" if result["passed"] else "检查未通过，请查看结果并诊断。", "success" if result["passed"] else "error")
        return redirect(url_for("task", checkpoint_id=checkpoint_id))

    @app.post("/task/<checkpoint_id>/complete")
    @require_student
    def complete_task(checkpoint_id: str) -> Any:
        engine.complete_task(current_student_id(), checkpoint_id)
        flash(f"{checkpoint_id} 已完成，下一检查点已解锁。", "success")
        return redirect(url_for("dashboard"))

    @app.post("/student/start")
    @require_student
    def start_student() -> Any:
        server = engine.start_student(current_student_id())
        flash(f"学生项目已启动：{server['url']}。请在新标签页亲自操作。", "success")
        return redirect(request.form.get("return_to") or url_for("dashboard"))

    @app.post("/student/stop")
    @require_student
    def stop_student() -> Any:
        stopped = engine.stop_student(current_student_id())
        flash("学生项目已停止。" if stopped else "学生项目当前没有运行。", "success")
        return redirect(request.form.get("return_to") or url_for("dashboard"))

    @app.get("/workspace")
    @require_student
    def workspace() -> str:
        view = engine.workspace_view(current_student_id(), request.args.get("file"))
        return render_template("workspace.html", **view)

    @app.get("/compare/<checkpoint_id>/<path:relative_path>")
    @require_student
    def compare(checkpoint_id: str, relative_path: str) -> str:
        state = engine.get_state(current_student_id())
        if checkpoint_id not in state["tasks"] or not state["tasks"][checkpoint_id]["applied"]:
            raise PlatformError("只能查看已经应用检查点的代码差异。")
        result = engine.compare_file(checkpoint_id, relative_path)
        return render_template("compare.html", result=result)

    @app.get("/tests")
    @require_student
    def tests_page() -> str:
        student_id = current_student_id()
        state = engine.get_state(student_id)
        return render_template(
            "tests.html",
            state=state,
            server=engine.server_status(student_id),
            manual_complete=engine._manual_tests_complete(state),
        )

    @app.post("/tests/save")
    @require_student
    def save_tests() -> Any:
        cases = []
        for index, scenario in enumerate(MANUAL_TEST_SCENARIOS):
            prefix = f"case_{index}_"
            cases.append(
                {
                    "id": scenario["id"],
                    "precondition": request.form.get(prefix + "precondition", ""),
                    "action": request.form.get(prefix + "action", ""),
                    "expected": request.form.get(prefix + "expected", ""),
                    "actual": request.form.get(prefix + "actual", ""),
                    "conclusion": request.form.get(prefix + "conclusion", ""),
                }
            )
        engine.save_manual_tests(current_student_id(), cases)
        flash("手工测试记录已保存。", "success")
        return redirect(url_for("tests_page"))

    @app.post("/tests/run")
    @require_student
    def run_tests() -> Any:
        result = engine.run_tests(current_student_id())
        if result["kind"] == "six_passed":
            message, category = "自动测试完成：6 passed。", "success"
        elif result["kind"] == "empty_collection":
            message, category = "pytest 已运行，但尚无测试用例；这是 C6 的预期观察。", "warning"
        else:
            message, category = "自动测试未通过，请先阅读输出再恢复。", "error"
        flash(message, category)
        return redirect(url_for("tests_page"))

    @app.post("/fault/inject")
    @require_student
    def inject_fault() -> Any:
        engine.inject_fault(current_student_id())
        flash("已暂时移出首页模板。请先阅读 TemplateNotFound 证据并填写判断。", "warning")
        return redirect(url_for("task", checkpoint_id="C8"))

    @app.post("/fault/restore")
    @require_student
    def restore_fault() -> Any:
        engine.restore_fault(current_student_id(), request.form.get("diagnosis", ""))
        flash("首页模板已准确恢复。现在必须重新运行6项回归测试。", "success")
        return redirect(url_for("task", checkpoint_id="C8"))

    @app.post("/release/freeze")
    @require_student
    def freeze_release() -> Any:
        result = engine.freeze_release(
            current_student_id(), request.form.get("commit_message", "")
        )
        flash(f"dev-v0.1 已冻结，终点提交为 {result['v01_commit'][:8]}。", "success")
        return redirect(url_for("report"))

    @app.get("/report")
    @require_student
    def report() -> str:
        state = engine.get_state(current_student_id())
        final = engine.compare_final(current_student_id())
        return render_template("report.html", state=state, final=final)

    @app.post("/report/export")
    @require_student
    def export_report() -> Any:
        path = engine.export_evidence(current_student_id())
        return send_file(path, as_attachment=True, download_name=path.name)

    @app.get("/teacher")
    def teacher() -> str:
        return render_template("teacher.html", students=engine.list_students())

    return app


if __name__ == "__main__":
    application = create_app()
    address = "http://127.0.0.1:8000"
    print(f"教学平台正在运行：{address}")
    print("关闭本窗口即可停止教学平台。")
    if os.environ.get("TEACHING_PLATFORM_NO_BROWSER") != "1":
        threading.Timer(1.0, lambda: webbrowser.open(address)).start()
    application.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)
