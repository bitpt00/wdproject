# S08 从dev-v0.2到dev-v0.3：登录与角色

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 起点 | 已测试并提交的`dev-v0.2` |
| 终点 | `dev-v0.3`登录与角色版本 |
| 对应需求 | REQ-03、REQ-08中的基础权限；保持REQ-01、REQ-02 |
| 课时 | 第12—13课时，共90分钟 |
| 正式参考标签 | `dev-v0.3` |
| 教师参考提交 | `543e509` |
| 自动测试 | 14项全部通过 |

V0.2知道“有哪些实验室”，但不知道“当前操作者是谁”。任何人都能打开静态预约表单，也没有学生、审批教师和管理员的区别。

V0.3完成三个基础能力：

```text
认证 authentication：确认你是谁
会话 session：在后续请求中记住你已经登录
授权 authorization：根据角色判断你能做什么
```

本版只建立角色入口。学生仍不能真正提交预约，教师和管理员工作台也只显示后续功能说明。

## 2. 开始前检查`dev-v0.2`

```powershell
git status --short
git describe --tags --exact-match HEAD
.\.venv\Scripts\python.exe -m pytest -q
```

正确结果：工作区干净；当前提交标签为`dev-v0.2`；测试显示`10 passed`。

在个人记录册复制一份单版本模板，填写：

```text
版本名称：V0.3 登录与角色
起点版本或提交号：填写自己的dev-v0.2提交号
本版要解决的问题：系统不能识别当前用户，所有人看到相同入口
本版验收标准：三类账号可登录退出、工作台不同、学生表单受角色保护、14项测试通过
```

## 3. 本版真实变化

V0.2终点有15个受控文件，V0.3终点有17个：

```text
新增：User模型和users数据表
新增：三条用户种子数据和密码哈希
新增：登录、退出、工作台路由
新增：login_required与role_required权限装饰器
新增：login.html和dashboard.html
更新：公共模板根据登录状态和角色显示菜单
更新：首页和预约原型显示身份状态
更新：CSS和自动测试
保持：实验室数据、查询和详情功能
```

## 4. 步骤1：升级版本并增加`User`模型

### 4.1 整体替换`VERSION`

```text
dev-v0.3
```

### 4.2 整体替换`models.py`

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

### 4.3 操作之后理解用户模型

- `username`是登录账号，必须唯一。
- `role`只保存`student`、`approver`或`admin`，页面通过`role_name`显示中文。
- 数据库不保存明文密码`123456`，而保存`password_hash`。
- `set_password`生成带随机盐的哈希；`check_password`验证输入是否匹配。
- 相同密码的不同用户，其哈希字符串也不要求相同。

认证信息属于敏感数据。即使是课堂演示账号，也要学习“不保存明文密码”的基本原则。

## 5. 步骤2：增加登录、会话和角色权限

打开`app.py`并整体替换：

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

## 6. 步骤3：先检查用户表和密码，不急着开页面

保存`app.py`后执行：

```powershell
.\.venv\Scripts\python.exe -c "from app import app; from models import User,db; c=app.app_context(); c.push(); users=db.session.query(User).order_by(User.id).all(); print([(u.username,u.role,u.password_hash!='123456',u.check_password('123456')) for u in users]); c.pop()"
```

预期出现三组信息：

```text
('20260001', 'student', True, True)
('T1001', 'approver', True, True)
('A001', 'admin', True, True)
```

第三个值`True`证明数据库中的哈希不等于明文；第四个值`True`证明输入`123456`能够通过验证。

### 6.1 操作之后理解一次登录

```text
浏览器POST账号和密码
→ 查询User
→ check_password验证哈希
→ session保存user_id
→ 后续请求before_request读取User到g.user
→ 路由装饰器检查是否登录及角色
```

- `session`保存在经过签名的浏览器会话中，`SECRET_KEY`用于保护签名。
- 会话只保存`user_id`，不保存明文密码。
- `g.user`只在当前请求中使用，每次请求都会重新根据会话加载用户。
- `login_required`解决“必须登录”，`role_required`进一步解决“必须属于规定角色”。
- `@wraps`保留原路由函数信息，避免多个装饰器破坏Flask端点名称。

V0.3的`SECRET_KEY`是课程开发值，且POST表单尚未加入防伪令牌；这些质量和安全加固安排在V0.6。

## 7. 步骤4：建立登录和角色页面

### 7.1 整体替换`templates/base.html`

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

### 7.2 新建`templates/login.html`

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

### 7.3 新建`templates/dashboard.html`

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

### 7.4 整体替换`templates/index.html`

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

### 7.5 整体替换`templates/reservation_form.html`

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

注意：冻结的V0.3模板中，最后两个阶段卡片都写成`dev-v0.4`。本手册按真实标签保留这一现象，不在代码步骤中偷偷修正；第14节会把它作为一个可记录的界面缺陷。

### 7.6 复制V0.3样式资源

用：

```text
教学资源\版本终点核对包\dev-v0.3\static\style.css
```

覆盖个人`static\style.css`。终点样式为758行、约12 KB，新增用户区、登录页、消息提示和工作台样式。

### 7.7 操作之后理解页面权限

- 模板中的`{% if g.user %}`只决定菜单显示，改善使用体验。
- 真正的权限边界在路由装饰器中。隐藏菜单不能代替服务端授权。
- `flash`把一次请求中的结果提示带到下一个页面。
- 退出使用POST，因为它会改变会话状态；直接GET访问`/logout`不是正确入口。

## 8. 步骤5：运行并观察三类角色

双击`启动系统.bat`，使用统一密码`123456`依次登录：

| 账号 | 角色 | 工作台应显示的主要内容 |
| --- | --- | --- |
| `20260001` | 学生 | 查询实验室、填写预约 |
| `T1001` | 审批教师 | 审批队列尚未开放 |
| `A001` | 实验室管理员 | 实验室维护尚未开放 |

每次切换角色前先单击“退出”。已经登录时直接访问`/login`会返回当前角色工作台，不会覆盖为另一个账号。

## 9. 步骤6：替换V0.3自动测试

把`tests/test_app.py`整体替换为：

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

停止服务器后执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

预期：

```text
..............                                                           [100%]
14 passed
```

## 10. 手工验收V0.3

| 用例编号 | 操作 | 预期结果 | 我的结果 |
| --- | --- | --- | --- |
| MT-V03-01 | 退出状态打开`/dashboard` | 转到登录页，并提示先登录 |  |
| MT-V03-02 | 用学生账号和错误密码登录 | 显示账号或密码错误，仍在登录页 |  |
| MT-V03-03 | 用`20260001`登录 | 显示张晨、学生工作台和预约表单入口 |  |
| MT-V03-04 | 学生打开预约表单 | 返回正常页面，但提交按钮仍禁用 |  |
| MT-V03-05 | 退出后用`T1001`登录 | 显示审批教师工作台，不显示学生预约入口 |  |
| MT-V03-06 | 教师直接打开`/reservations/new` | 返回403 |  |
| MT-V03-07 | 用`A001`登录 | 显示管理员工作台和尚未开放说明 |  |
| MT-V03-08 | 单击退出，再打开`/dashboard` | 会话已清除，再次转到登录页 |  |
| MT-V03-09 | 未登录打开实验室列表 | 公共查询仍可使用 |  |

把结果填入记录册，特别记录“看不见入口”和“直接输入网址被拒绝”是两种不同检查。

## 11. 常见问题与恢复

### 问题1：`no such table: users`

确认新的`models.py`已经保存，并重新启动应用。`db.create_all()`会在V0.2数据库中增加缺少的`users`表。

### 问题2：三类账号都提示密码错误

旧数据库可能有不完整的用户数据。停止服务器，把`instance/campus_lab.db`改名备份后重新启动，让种子数据完整生成。

### 问题3：登录成功后立刻又回到登录页

检查`SECRET_KEY`是否存在，登录成功分支是否执行`session["user_id"] = user.id`，以及`before_request`是否把用户加载到`g.user`。

### 问题4：教师看不到菜单，但直接输入学生网址却能打开

只做了模板隐藏，没有做服务端授权。确认预约路由上方同时有：

```python
@app.get("/reservations/new")
@role_required("student")
def reservation_form():
    ...
```

### 问题5：页面提示信息不出现

`flash`只是写入消息，`base.html`还必须调用`get_flashed_messages(with_categories=true)`显示。

### 问题6：出现`BuildError`或所有路由名称异常

检查两个装饰器是否使用`@wraps(view)`。修改装饰器后完全停止并重启服务器。

### 完整恢复方法

保留个人`.git`和`.venv`，从`教学资源\版本终点核对包\dev-v0.3`覆盖17个终点文件。若数据库结构仍异常，把本地数据库改名后重建。重新执行14项测试，再进入提交。

## 12. 终点源码机械核对

V0.3核对包由冻结标签机械导出，共17个受控文件。在个人项目根目录执行，先修改第一行：

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v0.3"
$courseFiles = @(
    ".gitignore",
    "VERSION",
    "app.py",
    "models.py",
    "requirements.txt",
    "static\style.css",
    "templates\base.html",
    "templates\dashboard.html",
    "templates\index.html",
    "templates\lab_detail.html",
    "templates\labs.html",
    "templates\login.html",
    "templates\reservation_form.html",
    "tests\test_app.py",
    "初始化开发环境.bat",
    "启动系统.bat",
    "运行测试.bat"
)
foreach ($courseFile in $courseFiles) {
    $mine = (Get-Content -LiteralPath $courseFile -Raw -Encoding UTF8).Replace("`r`n", "`n")
    $answer = (Get-Content -LiteralPath (Join-Path $courseAnswerRoot $courseFile) -Raw -Encoding UTF8).Replace("`r`n", "`n")
    if ($mine -ceq $answer) { "PASS  $courseFile" } else { "CHECK $courseFile" }
}
```

必须得到17行`PASS`。

### 12.1 最终代码核对索引

| 终点内容 | 完整代码或准确来源 |
| --- | --- |
| `VERSION`、`models.py` | 第4节 |
| `app.py` | 第5节 |
| 5个新增或修改模板 | 第7.1—7.5节 |
| `static/style.css` | 第7.6节精确资源 |
| `tests/test_app.py` | 第9节 |
| 其余7个文件 | 从`dev-v0.2`起点保持不变，并由17文件比较核对 |

## 13. 提交并建立`dev-v0.3`标签

只有9项手工验收、14项自动测试和17文件核对都通过后执行：

```powershell
git status --short
git diff --stat
git add VERSION app.py models.py static\style.css
git add templates\base.html templates\dashboard.html templates\index.html templates\login.html templates\reservation_form.html
git add tests\test_app.py
git commit -m "feat: add login and role access for dev-v0.3"
git tag -a dev-v0.3 -m "Complete development version 0.3"
```

验证：

```powershell
git status --short
git log --oneline --decorate -4
git tag --list
git show dev-v0.3:VERSION
```

正确结果：工作区干净；最新提交有`dev-v0.3`；V0.1、V0.2标签仍在；版本文件输出`dev-v0.3`。

## 14. 本章练习

### 练习1：区分认证和授权

判断下列失败发生在认证还是授权：错误密码登录、教师访问学生预约页、未登录访问工作台。

本练习不修改代码，无需恢复。

### 练习2：观察会话

学生登录后依次刷新首页、列表和工作台，观察右上角身份是否保持；退出后再次刷新，说明`session`和`g.user`分别承担什么作用。

本练习不修改文件，无需恢复。

### 练习3：让权限测试先失败

临时把预约路由的`@role_required("student")`注释掉，运行测试并找到教师访问测试的变化。

恢复方法：

```powershell
git restore app.py
.\.venv\Scripts\python.exe -m pytest -q
```

### 练习4：验证密码没有明文保存

执行第6节用户查询命令，比较三名用户哈希与`123456`；说明为什么系统仍能判断输入密码正确。

本练习不修改文件，无需恢复。

### 练习5：记录真实界面缺陷

在学生预约原型右侧观察两个都标为`dev-v0.4`的阶段卡片。在记录册第17节新增`BUG-V03-01`，写明复现步骤、预期和实际结果。本版不修复它，因为冻结终点必须与标签一致；V0.4替换页面时再检查。

本练习只增加缺陷记录，不修改源码，无需恢复。

## 15. 两课时推进建议

### 第12课时：从用户表到有效会话

```text
0—7分钟：核对V0.2，区分认证、会话和授权
7—18分钟：增加User模型并理解密码哈希
18—34分钟：替换app.py，分析登录和两个装饰器
34—40分钟：运行数据库查询验证三条用户数据
40—45分钟：画出一次登录请求链路
```

### 第13课时：三角色页面、测试和冻结

```text
0—18分钟：替换5个模板与CSS资源
18—28分钟：分别体验学生、教师、管理员工作台
28—34分钟：替换并执行14项自动测试
34—39分钟：完成9项手工验收
39—42分钟：执行17文件机械核对
42—45分钟：提交并建立dev-v0.3标签
```

## 16. 本章完成检查

- [ ] 起点是测试通过且工作区干净的`dev-v0.2`。
- [ ] `users`表包含学生、审批教师和管理员三条种子数据。
- [ ] 数据库存储密码哈希而不是明文`123456`。
- [ ] 错误密码不会建立登录会话。
- [ ] 未登录访问工作台会转到登录页。
- [ ] 三类账号登录后看到不同工作台内容。
- [ ] 学生可以打开预约原型，教师直接访问得到403。
- [ ] 退出后会话被清除。
- [ ] 我能解释认证、会话、授权、`g.user`和两个装饰器。
- [ ] 我知道模板隐藏菜单不能代替服务端权限检查。
- [ ] 9项手工验收均通过。
- [ ] 自动测试显示`14 passed`。
- [ ] 机械核对显示17行`PASS`。
- [ ] Git工作区干净，`dev-v0.1`—`dev-v0.3`标签均存在。
- [ ] 个人记录册已填写V0.3提交号、测试结果和`BUG-V03-01`观察记录。
