# dev-v0.3 完整代码核对附录

> 本附录由冻结版本终点包机械生成，不是手工重新整理的代码。文件内容只统一为LF换行；原始字节数与SHA-256用于核对终点资源。

## 1. 文件清单

| 路径 | 原始字节数 | 代码行数 | 原始文件SHA-256 |
| --- | ---: | ---: | --- |
| `.gitignore` | 62 | 6 | `bb1173460471204c4b38c69ac9b1fe238efe3a175a029a3977a659bff182d955` |
| `VERSION` | 10 | 1 | `49f74f673a66749bd323546ccb327be8637ecccc42922f7b837a9be3445d756b` |
| `app.py` | 7241 | 237 | `0ca55ef09b838780dd24f6c5c8aadb10679031f6d2926c2655e5d3629620fd49` |
| `models.py` | 1741 | 50 | `1053bdf0aa28c3bcb845fb6a1ce958ef18f2ed5b50f85cada36a4c59e82d1ff0` |
| `requirements.txt` | 54 | 3 | `1f2fb163b1f8c0cae49cf5a4a8279685080d4c3126ae0e77527fa2ce231766f3` |
| `static/style.css` | 12206 | 758 | `f9afff342e57ef6945090bd7b4f6ca26e6e2187c97dd50814a2231910e995625` |
| `templates/base.html` | 2841 | 66 | `73452936904464c19aba29293378e5f16e5942bf010b3b26afd2bd3fcbd99b34` |
| `templates/dashboard.html` | 2225 | 52 | `9f9b7a5025d555ed54e789b507148673a02b370cbc03adff7b2079aadafe22d4` |
| `templates/index.html` | 2979 | 66 | `6b03bf0e780cab31045813993386194fa819a0b26a45aa6aa85fee5fd12ad304` |
| `templates/lab_detail.html` | 1712 | 40 | `415c76bf12bdfd3327df6bd4ab613a798aeb1d776fd72e2664be5462acd434a7` |
| `templates/labs.html` | 3154 | 75 | `61b5bdbe64d6646df209eb5faf238ac7b4d2e28cb10413a8c844a1c92ce50a03` |
| `templates/login.html` | 1595 | 33 | `8bf1d1b294b3e59ce75527187ad4d7f1e2d57c7a5faa665423969d92dca6dddf` |
| `templates/reservation_form.html` | 3208 | 75 | `10597042540a27e389c28642b3aa147f2cc0b4743a6225dc4438ac28beccc3af` |
| `tests/test_app.py` | 4173 | 141 | `30efc379322559fa2fbd9383f8b984ce0cf93b7431d38a9cd068210debc1fb7e` |
| `初始化开发环境.bat` | 529 | 26 | `233dfdaa0b6fc06efe8394712a96a31e28a3ed2c46d48e7317b9797d22f4d04e` |
| `启动系统.bat` | 367 | 14 | `7a5647c36b82a5409692ef3a1ff95dff84622b29d0c27a776eaeada37e060e96` |
| `运行测试.bat` | 242 | 14 | `e68e2cf8e58cd20aee07fdfc6414878de748fd822b76ff2b01f41337bef6a405` |

## 2. 完整文件内容

### `.gitignore`

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.py[cod]
instance/

```

### `VERSION`

```text
dev-v0.3
```

### `app.py`

```python
from pathlib import Path
from functools import wraps

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func, or_, select

from models import Lab, User, db


VERSION = "dev-v0.3"

LAB_SEED_DATA = [
    {
        "name": "软件工程实验室",
        "location": "信息楼 A301",
        "capacity": 40,
        "equipment": "台式计算机、投影设备",
        "status": "可预约",
        "description": "适合软件工程、数据库和综合实践课程。",
    },
    {
        "name": "人工智能实验室",
        "location": "信息楼 A305",
        "capacity": 32,
        "equipment": "GPU工作站、投影设备",
        "status": "可预约",
        "description": "适合人工智能、数据分析和计算机视觉实验。",
    },
    {
        "name": "创新实践室",
        "location": "知新楼 B205",
        "capacity": 24,
        "equipment": "移动桌椅、电子白板、讨论区",
        "status": "可预约",
        "description": "适合项目评审、小型研讨和创新实践活动。",
    },
    {
        "name": "网络技术实验室",
        "location": "信息楼 B201",
        "capacity": 36,
        "equipment": "网络实验箱、台式计算机",
        "status": "维护中",
        "description": "交换机正在升级维护，暂不接受新预约。",
    },
]

USER_SEED_DATA = [
    {
        "username": "20260001",
        "display_name": "张晨",
        "department": "数字媒体专业",
        "role": "student",
    },
    {
        "username": "T1001",
        "display_name": "李老师",
        "department": "软件工程教研室",
        "role": "approver",
    },
    {
        "username": "A001",
        "display_name": "王老师",
        "department": "实验教学中心",
        "role": "admin",
    },
]


def seed_database():
    """数据库为空时写入课堂统一使用的样例数据。"""
    lab_count = db.session.scalar(select(func.count()).select_from(Lab))
    if lab_count == 0:
        db.session.add_all(Lab(**data) for data in LAB_SEED_DATA)

    user_count = db.session.scalar(select(func.count()).select_from(User))
    if user_count == 0:
        for data in USER_SEED_DATA:
            user = User(**data)
            user.set_password("123456")
            db.session.add(user)

    if lab_count == 0 or user_count == 0:
        db.session.commit()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("请先登录后再访问该页面。", "warning")
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped_view(**kwargs):
            if g.user.role not in roles:
                abort(403)
            return view(**kwargs)

        return wrapped_view

    return decorator


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__, instance_relative_config=True)
    database_path = Path(app.instance_path) / "campus_lab.db"
    app.config.from_mapping(
        TESTING=False,
        SECRET_KEY="development-course-secret-key",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path.as_posix()}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_database()

    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.user = db.session.get(User, user_id) if user_id else None

    @app.context_processor
    def inject_version():
        return {"app_version": VERSION}

    @app.get("/")
    def index():
        lab_count = db.session.scalar(select(func.count()).select_from(Lab))
        available_count = db.session.scalar(
            select(func.count()).select_from(Lab).where(Lab.status == "可预约")
        )
        return render_template(
            "index.html",
            lab_count=lab_count,
            available_count=available_count,
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if g.user is not None:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = db.session.scalar(select(User).where(User.username == username))

            if user is None or not user.check_password(password):
                flash("账号或密码错误，请重新输入。", "error")
            else:
                session.clear()
                session["user_id"] = user.id
                flash(f"欢迎回来，{user.display_name}。", "success")
                return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.post("/logout")
    @login_required
    def logout():
        session.clear()
        flash("您已安全退出。", "success")
        return redirect(url_for("index"))

    @app.get("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.get("/labs")
    def lab_list():
        keyword = request.args.get("keyword", "").strip()
        status = request.args.get("status", "").strip()

        statement = select(Lab)
        if keyword:
            like_value = f"%{keyword}%"
            statement = statement.where(
                or_(
                    Lab.name.like(like_value),
                    Lab.location.like(like_value),
                    Lab.equipment.like(like_value),
                )
            )
        if status in {"可预约", "维护中"}:
            statement = statement.where(Lab.status == status)

        labs = db.session.scalars(statement.order_by(Lab.id)).all()
        return render_template(
            "labs.html",
            labs=labs,
            keyword=keyword,
            selected_status=status,
        )

    @app.get("/labs/<int:lab_id>")
    def lab_detail(lab_id):
        lab = db.session.get(Lab, lab_id)
        if lab is None:
            abort(404)
        return render_template("lab_detail.html", lab=lab)

    @app.get("/reservations/new")
    @role_required("student")
    def reservation_form():
        selected_lab_id = request.args.get("lab", type=int)
        labs = db.session.scalars(
            select(Lab).where(Lab.status == "可预约").order_by(Lab.id)
        ).all()
        return render_template(
            "reservation_form.html",
            labs=labs,
            selected_lab_id=selected_lab_id,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
```

### `models.py`

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model):
    """系统用户：一个字段保存一个用户当前承担的角色。"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        return {
            "student": "学生",
            "approver": "审批教师",
            "admin": "实验室管理员",
        }.get(self.role, "未知角色")


class Lab(db.Model):
    """实验室：dev-v0.2阶段的第一个数据库实体。"""

    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="可预约")
    description = db.Column(db.Text, nullable=False, default="")

    @property
    def is_available(self):
        return self.status == "可预约"
```

### `requirements.txt`

```text
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
pytest==9.1.1
```

### `static/style.css`

```css
:root {
    --navy: #16324f;
    --blue: #2563eb;
    --blue-dark: #1d4ed8;
    --teal: #0f766e;
    --ink: #1f2937;
    --muted: #667085;
    --line: #dbe3ec;
    --surface: #ffffff;
    --soft: #f4f7fb;
    --warning: #a15c00;
    --danger: #b42318;
    --shadow: 0 16px 40px rgba(22, 50, 79, 0.09);
}

* {
    box-sizing: border-box;
}

body {
    display: flex;
    min-height: 100vh;
    flex-direction: column;
    margin: 0;
    min-width: 320px;
    color: var(--ink);
    background: var(--soft);
    font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
    line-height: 1.6;
}

main {
    flex: 1 0 auto;
}

.version-strip,
.site-header,
.site-footer {
    flex-shrink: 0;
}

a {
    color: inherit;
    text-decoration: none;
}

.container {
    width: min(1120px, calc(100% - 40px));
    margin: 0 auto;
}

.version-strip {
    padding: 7px 20px;
    color: #eaf3ff;
    background: var(--navy);
    font-size: 13px;
    text-align: center;
}

.site-header {
    position: sticky;
    top: 0;
    z-index: 10;
    border-bottom: 1px solid rgba(219, 227, 236, 0.9);
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(10px);
}

.header-inner,
.footer-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-inner {
    min-height: 72px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    display: grid;
    width: 42px;
    height: 42px;
    place-items: center;
    border-radius: 12px;
    color: white;
    background: var(--blue);
    font-size: 22px;
    font-weight: 800;
}

.brand strong,
.brand small {
    display: block;
}

.brand strong {
    color: var(--navy);
    font-size: 16px;
}

.brand small {
    margin-top: -3px;
    color: var(--muted);
    font-size: 12px;
}

.main-nav {
    display: flex;
    gap: 8px;
}

.main-nav a {
    padding: 9px 14px;
    border-radius: 9px;
    color: #475467;
    font-size: 14px;
    font-weight: 600;
}

.main-nav a:hover,
.main-nav a.active {
    color: var(--blue-dark);
    background: #eef4ff;
}

.hero {
    padding: 76px 0 70px;
    background:
        radial-gradient(circle at 85% 20%, rgba(37, 99, 235, 0.13), transparent 28%),
        linear-gradient(145deg, #ffffff 0%, #edf4ff 100%);
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 64px;
    align-items: center;
}

.eyebrow {
    margin: 0 0 8px;
    color: var(--teal);
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.12em;
}

h1,
h2,
h3,
p {
    margin-top: 0;
}

h1 {
    margin-bottom: 20px;
    color: var(--navy);
    font-size: clamp(34px, 5vw, 54px);
    line-height: 1.2;
}

h2 {
    color: var(--navy);
}

.hero-copy {
    max-width: 690px;
    color: #475467;
    font-size: 18px;
}

.hero-actions {
    display: flex;
    gap: 12px;
    margin-top: 30px;
}

.button {
    display: inline-flex;
    min-height: 44px;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border: 0;
    border-radius: 10px;
    font: inherit;
    font-weight: 700;
    cursor: pointer;
}

.button.primary {
    color: white;
    background: var(--blue);
}

.button.primary:hover {
    background: var(--blue-dark);
}

.button.secondary {
    color: var(--navy);
    border: 1px solid var(--line);
    background: white;
}

.button:disabled {
    color: #98a2b3;
    background: #e4e7ec;
    cursor: not-allowed;
}

.button.full {
    width: 100%;
}

.button.small {
    padding: 9px 16px;
    color: #ffffff;
    background: var(--blue);
}

.prototype-card,
.feature-card,
.lab-card,
.reservation-form,
.stage-panel,
.detail-card,
.filter-bar,
.empty-state {
    border: 1px solid rgba(219, 227, 236, 0.9);
    border-radius: 18px;
    background: var(--surface);
    box-shadow: var(--shadow);
}

.prototype-card {
    padding: 30px;
}

.prototype-label {
    display: inline-block;
    margin-bottom: 10px;
    color: var(--blue-dark);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
}

.prototype-card > strong {
    display: block;
    color: var(--navy);
    font-size: 30px;
}

.prototype-card > p {
    color: var(--muted);
}

.check-list {
    margin: 22px 0 0;
    padding: 0;
    list-style: none;
}

.check-list li {
    position: relative;
    margin-top: 10px;
    padding-left: 25px;
}

.check-list li::before {
    position: absolute;
    left: 0;
    color: var(--teal);
    content: "✓";
    font-weight: 900;
}

.section {
    padding: 70px 0;
}

.section.compact-top {
    padding-top: 34px;
}

.section-heading {
    margin-bottom: 28px;
}

.section-heading h2 {
    margin-bottom: 0;
    font-size: 30px;
}

.feature-grid,
.lab-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
}

.feature-card,
.lab-card {
    padding: 26px;
}

.step-number,
.lab-id {
    color: var(--blue-dark);
    font-size: 13px;
    font-weight: 800;
}

.feature-card h3,
.lab-card h2 {
    margin: 10px 0 8px;
    color: var(--navy);
}

.feature-card p {
    min-height: 52px;
    color: var(--muted);
}

.state,
.status {
    display: inline-flex;
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

.state.available,
.status.open {
    color: #087443;
    background: #ecfdf3;
}

.state.prototype {
    color: var(--warning);
    background: #fff7e8;
}

.state.later,
.status.closed {
    color: #667085;
    background: #f2f4f7;
}

.page-heading {
    padding: 54px 0 46px;
    color: white;
    background: linear-gradient(135deg, var(--navy), #234f7b);
}

.page-heading h1 {
    margin-bottom: 12px;
    color: white;
    font-size: 38px;
}

.page-heading p:last-child {
    max-width: 760px;
    margin-bottom: 0;
    color: #dbeafe;
}

.page-heading .eyebrow {
    color: #8ee5d7;
}

.lab-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.lab-details {
    margin: 22px 0;
}

.lab-details div {
    display: grid;
    grid-template-columns: 52px 1fr;
    gap: 8px;
    padding: 8px 0;
    border-bottom: 1px solid #eef1f5;
}

.lab-details dt {
    color: var(--muted);
    font-size: 13px;
}

.lab-details dd {
    margin: 0;
    font-size: 14px;
}

.text-link {
    color: var(--blue-dark);
    font-size: 14px;
    font-weight: 700;
}

.text-link:hover {
    text-decoration: underline;
}

.text-muted {
    color: #98a2b3;
    font-size: 14px;
}

.filter-bar {
    display: flex;
    align-items: flex-end;
    gap: 14px;
    margin-bottom: 18px;
    padding: 20px;
}

.user-area {
    display: flex;
    align-items: center;
    gap: 12px;
}

.user-chip {
    display: flex;
    flex-direction: column;
    color: var(--navy);
    font-size: 13px;
    line-height: 1.25;
}

.user-chip small {
    color: var(--muted);
}

.inline-form {
    margin: 0;
}

.text-button {
    padding: 0;
    border: 0;
    color: var(--blue-dark);
    background: transparent;
    cursor: pointer;
}

.flash-stack {
    padding-top: 18px;
}

.flash {
    margin-bottom: 10px;
    padding: 13px 16px;
    border: 1px solid #bbd5ff;
    border-radius: 10px;
    color: #1849a9;
    background: #eff6ff;
}

.flash.success {
    border-color: #a6f4c5;
    color: #067647;
    background: #ecfdf3;
}

.flash.warning,
.flash.error {
    border-color: #fedf89;
    color: #93370d;
    background: #fffaeb;
}

.auth-section {
    display: flex;
    align-items: center;
}

.auth-layout,
.dashboard-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(300px, 0.85fr);
    gap: 24px;
    align-items: start;
}

.auth-layout h1 {
    margin: 6px 0 10px;
    color: var(--navy);
}

.form-intro {
    margin: 0 0 24px;
    color: var(--muted);
}

.demo-account {
    display: flex;
    justify-content: space-between;
    padding: 13px 0;
    border-bottom: 1px solid var(--line);
}

.demo-account span {
    color: var(--muted);
}

.demo-password {
    margin: 22px 0 0;
}

.filter-bar .form-row {
    margin: 0;
}

.filter-bar .grow {
    flex: 1;
}

.filter-status {
    width: 180px;
}

.result-summary {
    margin: 0 0 18px;
    color: var(--muted);
}

.card-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    margin-top: auto;
}

.empty-state {
    grid-column: 1 / -1;
    padding: 44px;
    text-align: center;
}

.empty-state h2 {
    margin-top: 0;
}

.back-link {
    display: inline-block;
    margin-bottom: 22px;
    color: #dbeafe;
    text-decoration: none;
}

.detail-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(280px, 0.75fr);
    gap: 24px;
    align-items: start;
}

.detail-card {
    padding: 28px;
}

.detail-card h2 {
    margin: 0;
}

.detail-list {
    margin: 26px 0;
}

.detail-list div {
    display: grid;
    grid-template-columns: 130px 1fr;
    gap: 18px;
    padding: 16px 0;
    border-bottom: 1px solid var(--line);
}

.detail-list dt {
    color: var(--muted);
}

.detail-list dd {
    margin: 0;
    font-weight: 700;
}

.form-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 340px;
    gap: 28px;
    align-items: start;
}

.reservation-form,
.stage-panel {
    padding: 30px;
}

.form-row {
    margin-bottom: 20px;
}

.form-row label {
    display: block;
    margin-bottom: 7px;
    color: #344054;
    font-size: 14px;
    font-weight: 700;
}

.form-row input,
.form-row select,
.form-row textarea {
    width: 100%;
    padding: 11px 12px;
    color: var(--ink);
    border: 1px solid #cfd8e3;
    border-radius: 9px;
    background: white;
    font: inherit;
}

.form-row input:focus,
.form-row select:focus,
.form-row textarea:focus {
    border-color: var(--blue);
    outline: 3px solid rgba(37, 99, 235, 0.12);
}

.form-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}

.stage-panel h2 {
    margin-bottom: 20px;
}

.stage-item {
    padding: 16px 0;
    border-top: 1px solid #eef1f5;
}

.stage-item strong {
    color: var(--navy);
}

.stage-item p {
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 14px;
}

.stage-item.done strong {
    color: var(--teal);
}

.stage-item.next strong {
    color: var(--blue-dark);
}

.site-footer {
    padding: 28px 0;
    color: #98a2b3;
    background: #10283f;
    font-size: 13px;
}

@media (max-width: 840px) {
    .hero-grid,
    .form-layout,
    .auth-layout,
    .dashboard-grid {
        grid-template-columns: 1fr;
    }

    .feature-grid,
    .lab-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero {
        padding-top: 54px;
    }
    .detail-layout {
        grid-template-columns: 1fr;
    }

    .filter-bar {
        align-items: stretch;
        flex-direction: column;
    }

    .filter-status {
        width: auto;
    }
}

@media (max-width: 600px) {
    .container {
        width: min(100% - 28px, 1120px);
    }

    .header-inner {
        align-items: flex-start;
        flex-direction: column;
        gap: 12px;
        padding: 14px 0;
    }

    .user-area {
        width: 100%;
        justify-content: flex-end;
    }

    .main-nav {
        width: 100%;
    }

    .main-nav a {
        flex: 1;
        padding: 8px;
        text-align: center;
    }

    .hero-actions,
    .footer-inner {
        align-items: stretch;
        flex-direction: column;
    }

    .feature-grid,
    .lab-grid,
    .form-columns {
        grid-template-columns: 1fr;
    }

    .feature-card p {
        min-height: 0;
    }
}
```

### `templates/base.html`

```html
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}校园实验室预约系统{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="version-strip">
        开发教学版 {{ app_version }} · 用户登录与角色权限
    </div>

    <header class="site-header">
        <div class="container header-inner">
            <a class="brand" href="{{ url_for('index') }}">
                <span class="brand-mark">L</span>
                <span>
                    <strong>校园实验室</strong>
                    <small>预约与审批系统</small>
                </span>
            </a>
            <nav class="main-nav" aria-label="主要导航">
                <a class="{{ 'active' if request.endpoint == 'index' else '' }}" href="{{ url_for('index') }}">首页</a>
                <a class="{{ 'active' if request.endpoint in ['lab_list', 'lab_detail'] else '' }}" href="{{ url_for('lab_list') }}">实验室</a>
                {% if g.user %}
                <a class="{{ 'active' if request.endpoint == 'dashboard' else '' }}" href="{{ url_for('dashboard') }}">工作台</a>
                {% if g.user.role == 'student' %}
                <a class="{{ 'active' if request.endpoint == 'reservation_form' else '' }}" href="{{ url_for('reservation_form') }}">预约申请</a>
                {% endif %}
                {% endif %}
            </nav>
            <div class="user-area">
                {% if g.user %}
                <span class="user-chip"><strong>{{ g.user.display_name }}</strong><small>{{ g.user.role_name }}</small></span>
                <form class="inline-form" method="post" action="{{ url_for('logout') }}">
                    <button class="text-button" type="submit">退出</button>
                </form>
                {% else %}
                <a class="button small" href="{{ url_for('login') }}">登录</a>
                {% endif %}
            </div>
        </div>
    </header>

    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        <div class="container flash-stack">
            {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
        <div class="container footer-inner">
            <span>校园实验室预约与审批系统</span>
            <span>{{ app_version }}</span>
        </div>
    </footer>
</body>
</html>
```

### `templates/dashboard.html`

```html
{% extends "base.html" %}

{% block title %}工作台｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">{{ g.user.role_name }}工作台</p>
        <h1>{{ g.user.display_name }}，您好</h1>
        <p>{{ g.user.department }} · 当前登录账号 {{ g.user.username }}</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container dashboard-grid">
        {% if g.user.role == 'student' %}
        <article class="feature-card">
            <span class="step-number">01</span>
            <h2>查询实验室</h2>
            <p>查询地点、设备和状态，为预约选择合适资源。</p>
            <a class="text-link" href="{{ url_for('lab_list') }}">开始查询</a>
        </article>
        <article class="feature-card">
            <span class="step-number">02</span>
            <h2>填写预约</h2>
            <p>当前可以查看表单，dev-v0.4开放提交和取消功能。</p>
            <a class="text-link" href="{{ url_for('reservation_form') }}">查看表单</a>
        </article>
        {% elif g.user.role == 'approver' %}
        <article class="feature-card">
            <span class="step-number">01</span>
            <h2>审批队列</h2>
            <p>角色权限已经就绪，dev-v0.5加入真正的待审批申请。</p>
            <span class="state prototype">功能尚未开放</span>
        </article>
        {% else %}
        <article class="feature-card">
            <span class="step-number">01</span>
            <h2>实验室维护</h2>
            <p>管理员身份已经识别，最终集成版加入状态维护入口。</p>
            <span class="state prototype">功能尚未开放</span>
        </article>
        {% endif %}

        <aside class="stage-panel">
            <span class="prototype-label">权限观察点</span>
            <h2>为什么菜单不同</h2>
            <p>登录后，系统从会话读取用户，再根据用户表中的role字段决定能够访问的路由和看到的操作。</p>
        </aside>
    </div>
</section>
{% endblock %}
```

### `templates/index.html`

```html
{% extends "base.html" %}

{% block title %}首页｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="hero">
    <div class="container hero-grid">
        <div>
            <p class="eyebrow">校园实验资源统一预约</p>
            <h1>校园实验室预约与审批系统</h1>
            <p class="hero-copy">
                学生查询实验室并提交预约，教师处理审批，管理员维护实验室状态。
                本版本在数据库查询的基础上增加登录，并区分学生、审批教师和管理员。
            </p>
            <div class="hero-actions">
                <a class="button primary" href="{{ url_for('lab_list') }}">浏览实验室</a>
                {% if g.user %}
                <a class="button secondary" href="{{ url_for('dashboard') }}">进入我的工作台</a>
                {% else %}
                <a class="button secondary" href="{{ url_for('login') }}">使用演示账号登录</a>
                {% endif %}
            </div>
        </div>
        <div class="prototype-card">
            <span class="prototype-label">当前版本</span>
            <strong>{{ app_version }}</strong>
            <p>系统能够识别“谁在使用”，并据此显示不同菜单和页面。</p>
            <ul class="check-list">
                <li>账号密码经过哈希保存</li>
                <li>登录状态保存在浏览器会话中</li>
                <li>学生、教师、管理员权限分离</li>
                <li>预约提交仍留到dev-v0.4</li>
            </ul>
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <div class="section-heading">
            <p class="eyebrow">主要业务</p>
            <h2>系统准备支持的三类操作</h2>
        </div>
        <div class="feature-grid">
            <article class="feature-card">
                <span class="step-number">01</span>
                <h3>查询实验室</h3>
                <p>按关键词和状态筛选，查看实验室的完整信息。</p>
                <span class="state available">已有 {{ lab_count }} 间实验室</span>
            </article>
            <article class="feature-card">
                <span class="step-number">02</span>
                <h3>提交预约</h3>
                <p>选择实验室、日期和时间，填写用途及参加人数。</p>
                <span class="state prototype">学生可看，暂不可提交</span>
            </article>
            <article class="feature-card">
                <span class="step-number">03</span>
                <h3>审批与管理</h3>
                <p>教师审批申请，管理员维护实验室的可用状态。</p>
                <span class="state later">角色入口已经建立</span>
            </article>
        </div>
    </div>
</section>
{% endblock %}
```

### `templates/lab_detail.html`

```html
{% extends "base.html" %}

{% block title %}{{ lab.name }}｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <a class="back-link" href="{{ url_for('lab_list') }}">← 返回实验室列表</a>
        <p class="eyebrow">LAB-{{ "%03d"|format(lab.id) }}</p>
        <h1>{{ lab.name }}</h1>
        <p>{{ lab.description }}</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container detail-layout">
        <article class="detail-card">
            <div class="lab-card-top">
                <h2>实验室信息</h2>
                <span class="status {{ 'open' if lab.is_available else 'closed' }}">{{ lab.status }}</span>
            </div>
            <dl class="detail-list">
                <div><dt>位置</dt><dd>{{ lab.location }}</dd></div>
                <div><dt>可容纳人数</dt><dd>{{ lab.capacity }}人</dd></div>
                <div><dt>主要设备</dt><dd>{{ lab.equipment }}</dd></div>
            </dl>
            {% if lab.is_available %}
            <a class="button primary" href="{{ url_for('reservation_form', lab=lab.id) }}">填写预约信息</a>
            {% else %}
            <button class="button primary" disabled>维护期间不可预约</button>
            {% endif %}
        </article>
        <aside class="stage-panel">
            <span class="prototype-label">数据来源</span>
            <h2>这不是写死的页面</h2>
            <p>当前内容由路由根据网址中的实验室编号，从SQLite数据库查询后交给Jinja2模板显示。</p>
        </aside>
    </div>
</section>
{% endblock %}
```

### `templates/labs.html`

```html
{% extends "base.html" %}

{% block title %}实验室｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">实验资源</p>
        <h1>实验室列表</h1>
        <p>数据来自SQLite。可以按名称、位置、设备或当前状态进行筛选。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container">
        <form class="filter-bar" method="get" action="{{ url_for('lab_list') }}">
            <div class="form-row grow">
                <label for="keyword">关键词</label>
                <input id="keyword" name="keyword" value="{{ keyword }}" placeholder="名称、位置或设备">
            </div>
            <div class="form-row filter-status">
                <label for="status">状态</label>
                <select id="status" name="status">
                    <option value="">全部状态</option>
                    <option value="可预约" {{ 'selected' if selected_status == '可预约' else '' }}>可预约</option>
                    <option value="维护中" {{ 'selected' if selected_status == '维护中' else '' }}>维护中</option>
                </select>
            </div>
            <button class="button primary" type="submit">查询</button>
            <a class="button secondary" href="{{ url_for('lab_list') }}">重置</a>
        </form>

        <div class="result-summary">查询到 <strong>{{ labs|length }}</strong> 间实验室</div>

        <div class="lab-grid">
        {% for lab in labs %}
        <article class="lab-card">
            <div class="lab-card-top">
                <span class="lab-id">LAB-{{ "%03d"|format(lab.id) }}</span>
                <span class="status {{ 'open' if lab.status == '可预约' else 'closed' }}">{{ lab.status }}</span>
            </div>
            <h2>{{ lab.name }}</h2>
            <dl class="lab-details">
                <div>
                    <dt>位置</dt>
                    <dd>{{ lab.location }}</dd>
                </div>
                <div>
                    <dt>容量</dt>
                    <dd>{{ lab.capacity }}人</dd>
                </div>
                <div>
                    <dt>设备</dt>
                    <dd>{{ lab.equipment }}</dd>
                </div>
            </dl>
            <div class="card-actions">
                <a class="text-link" href="{{ url_for('lab_detail', lab_id=lab.id) }}">查看详情</a>
                {% if lab.is_available %}
                <a class="text-link" href="{{ url_for('reservation_form', lab=lab.id) }}">填写预约信息</a>
                {% else %}
                <span class="text-muted">当前不能选择</span>
                {% endif %}
            </div>
        </article>
        {% else %}
        <div class="empty-state">
            <h2>没有找到符合条件的实验室</h2>
            <p>请更换关键词或清除筛选条件。</p>
        </div>
        {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```

### `templates/login.html`

```html
{% extends "base.html" %}

{% block title %}登录｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="section auth-section">
    <div class="container auth-layout">
        <form class="reservation-form" method="post" action="{{ url_for('login') }}">
            <p class="eyebrow">身份验证</p>
            <h1>登录系统</h1>
            <p class="form-intro">使用下方任一课堂演示账号，观察不同角色看到的工作台。</p>
            <div class="form-row">
                <label for="username">账号</label>
                <input id="username" name="username" autocomplete="username" required autofocus>
            </div>
            <div class="form-row">
                <label for="password">密码</label>
                <input id="password" name="password" type="password" autocomplete="current-password" required>
            </div>
            <button class="button primary full" type="submit">登录</button>
        </form>

        <aside class="stage-panel">
            <span class="prototype-label">课堂演示账号</span>
            <h2>三种角色，同一密码</h2>
            <div class="demo-account"><strong>20260001</strong><span>学生</span></div>
            <div class="demo-account"><strong>T1001</strong><span>审批教师</span></div>
            <div class="demo-account"><strong>A001</strong><span>实验室管理员</span></div>
            <p class="demo-password">统一密码：<strong>123456</strong></p>
        </aside>
    </div>
</section>
{% endblock %}
```

### `templates/reservation_form.html`

```html
{% extends "base.html" %}

{% block title %}预约申请｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">预约申请</p>
        <h1>填写实验室预约信息</h1>
        <p>{{ g.user.display_name }}已以学生身份登录。当前版本用于验证权限，尚不保存预约申请。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container form-layout">
        <form class="reservation-form" aria-label="实验室预约表单">
            <div class="form-row">
                <label for="lab">实验室</label>
                <select id="lab" name="lab">
                    <option value="">请选择实验室</option>
                    {% for lab in labs %}
                    <option value="{{ lab.id }}" {{ 'selected' if selected_lab_id == lab.id else '' }}>{{ lab.name }}（{{ lab.location }}）</option>
                    {% endfor %}
                </select>
            </div>

            <div class="form-columns">
                <div class="form-row">
                    <label for="date">预约日期</label>
                    <input id="date" name="date" type="date">
                </div>
                <div class="form-row">
                    <label for="attendees">参加人数</label>
                    <input id="attendees" name="attendees" type="number" min="1" placeholder="例如：20">
                </div>
            </div>

            <div class="form-columns">
                <div class="form-row">
                    <label for="start-time">开始时间</label>
                    <input id="start-time" name="start_time" type="time">
                </div>
                <div class="form-row">
                    <label for="end-time">结束时间</label>
                    <input id="end-time" name="end_time" type="time">
                </div>
            </div>

            <div class="form-row">
                <label for="purpose">使用目的</label>
                <textarea id="purpose" name="purpose" rows="4" placeholder="说明课程、实验或活动内容"></textarea>
            </div>

            <button class="button primary full" type="button" disabled>提交预约（后续版本开放）</button>
        </form>

        <aside class="stage-panel">
            <span class="prototype-label">开发边界</span>
            <h2>这个版本做到哪里</h2>
            <div class="stage-item done">
                <strong>dev-v0.3已经完成</strong>
                <p>用户模型、密码校验、登录会话和三种角色的访问权限。</p>
            </div>
            <div class="stage-item next">
                <strong>dev-v0.4</strong>
                <p>增加可预约时段，让学生真正提交、查看和取消预约。</p>
            </div>
            <div class="stage-item later">
                <strong>dev-v0.4</strong>
                <p>让学生真正提交、查看和取消预约。</p>
            </div>
        </aside>
    </div>
</section>
{% endblock %}
```

### `tests/test_app.py`

```python
import pytest
from sqlalchemy import select

from app import LAB_SEED_DATA, create_app
from models import Lab, User, db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username="20260001", password="123456"):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.3" in response.get_data(as_text=True)


def test_database_is_seeded(app):
    with app.app_context():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()
        users = db.session.scalars(select(User).order_by(User.id)).all()

    assert len(labs) == len(LAB_SEED_DATA)
    assert labs[0].name == "软件工程实验室"
    assert [user.role for user in users] == ["student", "approver", "admin"]
    assert users[0].password_hash != "123456"


def test_lab_page_shows_database_labs(client):
    response = client.get("/labs")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    for lab in LAB_SEED_DATA:
        assert lab["name"] in page


def test_lab_list_can_filter_by_keyword_and_status(client):
    page = client.get("/labs?keyword=GPU&status=可预约").get_data(as_text=True)

    assert "人工智能实验室" in page
    assert "软件工程实验室" not in page
    assert "网络技术实验室" not in page


def test_lab_detail_comes_from_database(client):
    response = client.get("/labs/2")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "人工智能实验室" in page
    assert "计算机视觉实验" in page


def test_unknown_lab_returns_404(client):
    assert client.get("/labs/999").status_code == 404


def test_reservation_page_contains_required_fields(client):
    login(client)
    response = client.get("/reservations/new?lab=2")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'name="lab"' in page
    assert 'name="date"' in page
    assert 'name="start_time"' in page
    assert 'name="end_time"' in page
    assert 'name="attendees"' in page
    assert 'name="purpose"' in page
    assert 'value="2" selected' in page
    assert "提交预约（后续版本开放）" in page


def test_student_can_login_and_see_student_dashboard(client):
    response = login(client)
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "张晨，您好" in page
    assert "学生工作台" in page
    assert "填写预约" in page


def test_invalid_password_does_not_create_session(client):
    response = login(client, password="wrong-password")
    page = response.get_data(as_text=True)

    assert "账号或密码错误" in page
    assert "登录系统" in page


def test_anonymous_user_is_redirected_to_login(client):
    response = client.get("/dashboard", follow_redirects=True)

    assert "请先登录" in response.get_data(as_text=True)
    assert "登录系统" in response.get_data(as_text=True)


def test_approver_cannot_open_student_reservation_page(client):
    login(client, username="T1001")

    assert client.get("/reservations/new").status_code == 403


def test_logout_clears_login_session(client):
    login(client)
    client.post("/logout")

    assert client.get("/dashboard").status_code == 302


@pytest.mark.parametrize("path", ["/", "/labs"])
def test_navigation_is_visible_on_each_page(client, path):
    page = client.get(path).get_data(as_text=True)

    assert "首页" in page
    assert "实验室" in page
    assert "登录" in page
```

### `初始化开发环境.bat`

```bat
@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3.11 -m venv .venv 2>nul
    if errorlevel 1 python -m venv .venv
)

if not exist ".venv\Scripts\python.exe" (
    echo Failed to create the virtual environment.
    pause
    exit /b 1
)

set PIP_DISABLE_PIP_VERSION_CHECK=1
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo Development environment is ready.
pause

```

### `启动系统.bat`

```bat
@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment is missing.
    echo Run the setup script first.
    pause
    exit /b 1
)

start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Milliseconds 1200; Start-Process 'http://127.0.0.1:5000'"
".venv\Scripts\python.exe" app.py
pause
```

### `运行测试.bat`

```bat
@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment is missing.
    echo Run the setup script first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pytest -q
pause

```
