# S07 从dev-v0.1到dev-v0.2：数据库与查询

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 起点 | 已测试并提交的`dev-v0.1` |
| 终点 | `dev-v0.2`数据库与查询版本 |
| 对应需求 | REQ-02；继续保持REQ-01 |
| 课时 | 第10—11课时，共90分钟 |
| 正式参考标签 | `dev-v0.2` |
| 教师参考提交 | `0859544` |
| 自动测试 | 10项全部通过 |

V0.1的三间实验室写在`app.py`的`LABS`列表中，页面能看，但存在三个明显问题：

- 修改数据必须修改程序代码。
- 每次运行都不能保存业务数据变化。
- 只能显示列表，不能根据编号稳定查询一个对象。

V0.2把实验室迁移到SQLite，并增加关键词筛选、状态筛选和详情查询。预约表单仍然只是原型，不保存预约。

## 2. 开始前检查`dev-v0.1`

在个人项目根目录执行：

```powershell
git status --short
git describe --tags --exact-match HEAD
.\.venv\Scripts\python.exe -m pytest -q
```

正确结果：

- 第一条命令没有输出。
- 第二条命令输出`dev-v0.1`。
- 第三条命令显示`6 passed`。

如果不是这个结果，不进入V0.2。先按S06终点核对包恢复并完成V0.1。

在记录册复制一份“单版本记录模板”，填写：

```text
版本名称：V0.2 数据库与查询
起点版本或提交号：填写自己的dev-v0.1提交号
本版要解决的问题：实验室数据写死在app.py中，不能持久保存和按编号查询
本版验收标准：数据库自动创建，4间实验室可查询和筛选，详情可打开，10项测试通过
```

## 3. 本版真实变化

```text
删除：app.py中的LABS内存列表
新增：models.py中的Lab数据模型
新增：instance/campus_lab.db运行数据库（被Git忽略）
新增：lab_detail.html详情模板
更新：app.py使用SQLAlchemy创建、填充和查询数据库
更新：实验室列表增加关键词和状态筛选
更新：首页显示数据库统计
更新：预约表单的实验室选项来自数据库
更新：依赖、版本、样式和自动测试
重命名：启动dev-v0.1.bat → 启动系统.bat
```

`instance/campus_lab.db`是运行后自动生成的数据，不属于终点源码的15个受控文件，不提交到Git。

## 4. 步骤1：升级依赖、版本和启动脚本

### 4.1 整体替换`requirements.txt`

完整内容：

```text
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
pytest==9.1.1
```

新增的Flask-SQLAlchemy把Python类和数据库表连接起来。

### 4.2 安装新增依赖

保存文件后执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "from importlib.metadata import version; print(version('Flask-SQLAlchemy'))"
```

预期最后显示：

```text
3.1.1
```

如果这里失败，后面的`from flask_sqlalchemy import SQLAlchemy`一定会失败，所以不能跳过。

### 4.3 整体替换`VERSION`

```text
dev-v0.2
```

### 4.4 重命名并替换启动脚本

在文件资源管理器中把：

```text
启动dev-v0.1.bat
```

改名为：

```text
启动系统.bat
```

再把`启动系统.bat`整体替换为：

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

从本版开始，后续版本都使用统一名称`启动系统.bat`。

## 5. 步骤2：建立第一个数据模型

### 5.1 新建`models.py`

在项目根目录新建`models.py`，完整粘贴：

```python
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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

### 5.2 操作之后理解“类—表—行”

```text
Python类 Lab       ↔ SQLite表 labs
一个Lab对象        ↔ 表中的一行
对象属性 name      ↔ 表中的name列
```

- `primary_key=True`表示`id`唯一标识一条实验室记录。
- `unique=True`要求实验室名称不重复。
- `nullable=False`要求该列必须有值。
- `String(100)`等长度是数据设计约束，不是页面宽度。
- `is_available`不是数据库列，而是根据`status`计算出的便利属性。

此时只创建了模型定义，数据库文件还没有生成。真正把模型连接到应用后，SQLAlchemy才会建表。

## 6. 步骤3：把应用连接到SQLite

打开`app.py`，删除V0.1全部内容，完整替换为：

```python
from pathlib import Path

from flask import Flask, abort, render_template, request
from sqlalchemy import func, or_, select

from models import Lab, db


VERSION = "dev-v0.2"

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


def seed_labs():
    """数据库为空时写入课堂统一使用的样例数据。"""
    lab_count = db.session.scalar(select(func.count()).select_from(Lab))
    if lab_count == 0:
        db.session.add_all(Lab(**data) for data in LAB_SEED_DATA)
        db.session.commit()


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__, instance_relative_config=True)
    database_path = Path(app.instance_path) / "campus_lab.db"
    app.config.from_mapping(
        TESTING=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path.as_posix()}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_labs()

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

## 7. 步骤4：首次启动并观察数据库

### 7.1 启动

```powershell
.\.venv\Scripts\python.exe app.py
```

先打开：

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/labs
```

此时模板仍是V0.1样式，但列表应由数据库显示4间实验室，比V0.1多出“创新实践室”。

停止服务器后检查：

```powershell
Get-Item .\instance\campus_lab.db
git status --short
git status --short --ignored
```

预期：

- `instance/campus_lab.db`已经存在。
- 普通状态不会列出数据库。
- 带`--ignored`的状态把`instance/`显示为忽略项。

### 7.2 直接读取数据库对象

复制并执行下面一整行：

```powershell
.\.venv\Scripts\python.exe -c "from app import app; from models import Lab, db; c=app.app_context(); c.push(); rows=db.session.query(Lab).order_by(Lab.id).all(); print([(x.id,x.name,x.status) for x in rows]); c.pop()"
```

预期输出包含4条记录，并且最后一条为网络技术实验室、维护中。

### 7.3 操作之后理解数据库初始化

- `instance_relative_config=True`让应用使用专门的`instance`运行目录。
- `SQLALCHEMY_DATABASE_URI`指向`instance/campus_lab.db`。
- `db.init_app(app)`把模型组件连接到当前Flask应用。
- `db.create_all()`根据模型创建尚不存在的数据表。
- `seed_labs()`只在实验室数量为0时插入4条种子数据，重复启动不会重复添加。
- `app.app_context()`为初始化代码提供当前应用和数据库连接上下文。

## 8. 步骤5：更新数据库页面

### 8.1 整体替换`templates/base.html`

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
        开发教学版 {{ app_version }} · SQLite数据库与查询功能
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
                <a class="{{ 'active' if request.endpoint == 'reservation_form' else '' }}" href="{{ url_for('reservation_form') }}">预约申请</a>
            </nav>
        </div>
    </header>

    <main>
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

### 8.2 整体替换`templates/index.html`

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
                本版本已经把实验室信息迁移到SQLite数据库，并实现查询功能。
            </p>
            <div class="hero-actions">
                <a class="button primary" href="{{ url_for('lab_list') }}">浏览实验室</a>
                <a class="button secondary" href="{{ url_for('reservation_form') }}">查看预约表单</a>
            </div>
        </div>
        <div class="prototype-card">
            <span class="prototype-label">当前版本</span>
            <strong>{{ app_version }}</strong>
            <p>页面不再读取Python列表，而是通过数据模型查询SQLite数据库。</p>
            <ul class="check-list">
                <li>数据库首次启动自动创建</li>
                <li>内置 {{ lab_count }} 间实验室样例数据</li>
                <li>其中 {{ available_count }} 间当前可预约</li>
                <li>预约提交仍留到后续版本</li>
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
                <span class="state available">数据库查询已完成</span>
            </article>
            <article class="feature-card">
                <span class="step-number">02</span>
                <h3>提交预约</h3>
                <p>选择实验室、日期和时间，填写用途及参加人数。</p>
                <span class="state prototype">仍只展示表单</span>
            </article>
            <article class="feature-card">
                <span class="step-number">03</span>
                <h3>审批与管理</h3>
                <p>教师审批申请，管理员维护实验室的可用状态。</p>
                <span class="state later">后续版本实现</span>
            </article>
        </div>
    </div>
</section>
{% endblock %}
```

### 8.3 整体替换`templates/labs.html`

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

### 8.4 新建`templates/lab_detail.html`

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

### 8.5 整体替换`templates/reservation_form.html`

```html
{% extends "base.html" %}

{% block title %}预约申请｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">预约申请</p>
        <h1>填写实验室预约信息</h1>
        <p>实验室选项已从SQLite读取，但本版本仍不会保存预约申请。</p>
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
                <strong>dev-v0.2已经完成</strong>
                <p>数据库、实验室数据模型、样例数据、筛选和详情查询。</p>
            </div>
            <div class="stage-item next">
                <strong>dev-v0.3</strong>
                <p>增加用户登录，并区分学生、审批教师和管理员。</p>
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

### 8.6 复制V0.2样式资源

从：

```text
教学资源\版本终点核对包\dev-v0.2\static\style.css
```

覆盖个人项目的：

```text
static\style.css
```

终点样式为651行、约10 KB。本版新增筛选栏、详情布局和空结果样式，手工输入没有学习价值，因此使用精确资源。

### 8.7 操作之后理解查询

- GET表单把关键词和状态放入网址查询参数，刷新和复制网址后条件仍然存在。
- `select(Lab)`构造查询；`.where(...)`逐步增加条件。
- `or_`表示名称、位置、设备任一字段包含关键词即可。
- `order_by(Lab.id)`保证多次查询的显示顺序稳定。
- `<int:lab_id>`把网址中的编号转换为整数。
- 查不到对象时`abort(404)`明确返回“资源不存在”，而不是用空白页面掩盖问题。

## 9. 步骤6：替换V0.2自动测试

打开`tests/test_app.py`，整体替换为：

```python
import pytest
from sqlalchemy import select

from app import LAB_SEED_DATA, create_app
from models import Lab, db


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


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.2" in response.get_data(as_text=True)


def test_database_is_seeded(app):
    with app.app_context():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()

    assert len(labs) == len(LAB_SEED_DATA)
    assert labs[0].name == "软件工程实验室"


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


@pytest.mark.parametrize("path", ["/", "/labs", "/reservations/new"])
def test_navigation_is_visible_on_each_page(client, path):
    page = client.get(path).get_data(as_text=True)

    assert "首页" in page
    assert "实验室" in page
    assert "预约申请" in page
```

确保服务器已停止，然后执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

预期：

```text
..........                                                               [100%]
10 passed
```

测试使用`tmp_path/test.db`，每次在独立临时数据库中运行，不会依赖或污染个人`instance/campus_lab.db`。

## 10. 手工验收V0.2

双击`启动系统.bat`，执行：

| 用例编号 | 操作 | 预期结果 | 我的结果 |
| --- | --- | --- | --- |
| MT-V02-01 | 第一次启动并打开首页 | 自动生成数据库；首页显示4间实验室、3间可预约 |  |
| MT-V02-02 | 关键词输入`GPU`并选“可预约” | 只显示人工智能实验室 |  |
| MT-V02-03 | 输入不存在的关键词 | 显示“没有找到符合条件的实验室” |  |
| MT-V02-04 | 打开`/labs/2` | 显示人工智能实验室详情和计算机视觉说明 |  |
| MT-V02-05 | 打开`/labs/999` | 返回404页面 |  |
| MT-V02-06 | 打开预约表单下拉框 | 只有3间可预约实验室，不含维护中的网络技术实验室 |  |
| MT-V02-07 | 停止后重新启动 | 仍为4条数据，没有重复插入 |  |

把结果填写到记录册第16节，并在V0.2版本记录中说明数据库文件的位置和是否提交。

## 11. 常见问题与恢复

### 问题1：`No module named 'flask_sqlalchemy'`

依赖尚未安装到个人`.venv`。回到第4.2节，必须使用`.\.venv\Scripts\python.exe -m pip`安装。

### 问题2：`no such column`或页面与预期不一致

这通常来自旧数据库结构。V0.2第一次引入数据库，停止服务器后可以把当前数据库改名保留：

```powershell
Rename-Item .\instance\campus_lab.db campus_lab.v02-backup.db
```

重新启动会生成新数据库。确认新库正确后，备份文件仍可保留在`instance`中并被Git忽略。

### 问题3：每次启动都多出4条数据

检查`seed_labs()`中的`if lab_count == 0:`和其后缩进。只有空表才能执行`add_all`。

### 问题4：筛选结果始终显示全部

确认`statement = statement.where(...)`的结果重新赋给了`statement`；SQLAlchemy查询对象不会在原地自动改变。

### 问题5：详情页访问任何编号都报错

确认文件名为`templates/lab_detail.html`，路由参数和函数参数都叫`lab_id`，并且使用`db.session.get(Lab, lab_id)`。

### 问题6：首页报`lab_count is undefined`

确认`index()`调用`render_template`时同时传入`lab_count`和`available_count`。

### 完整恢复方法

记录错误后，从`教学资源\版本终点核对包\dev-v0.2`覆盖全部15个源码文件；个人`.git`和`.venv`保留不动。必要时把`instance/campus_lab.db`改名，让应用重建。随后重新执行10项测试。

## 12. 终点源码机械核对

`教学资源\版本终点核对包\dev-v0.2`由`dev-v0.2`标签机械导出，共15个文件。

在个人项目根目录执行，先修改第一行实际路径：

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v0.2"
$courseFiles = @(
    ".gitignore",
    "VERSION",
    "app.py",
    "models.py",
    "requirements.txt",
    "static\style.css",
    "templates\base.html",
    "templates\index.html",
    "templates\lab_detail.html",
    "templates\labs.html",
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

必须得到15行`PASS`。`instance/campus_lab.db`不在列表中，因为它是每台电脑自己的运行数据。

### 12.1 最终代码核对索引

| 终点文件 | 完整代码或准确来源 |
| --- | --- |
| `.gitignore`、初始化脚本、测试脚本 | 从`dev-v0.1`起点保持不变，并由15文件比较核对 |
| `VERSION`、`requirements.txt`、`启动系统.bat` | 本章第4节 |
| `models.py` | 本章第5.1节 |
| `app.py` | 本章第6节 |
| 5个HTML模板 | 本章第8.1—8.5节 |
| `static/style.css` | 本章第8.6节精确资源 |
| `tests/test_app.py` | 本章第9节 |

## 13. 提交并建立`dev-v0.2`标签

只有手工验收、10项测试和15文件核对全部通过后执行。

```powershell
git status --short
git diff --stat
git add VERSION app.py models.py requirements.txt static\style.css
git add templates\base.html templates\index.html templates\labs.html templates\lab_detail.html templates\reservation_form.html
git add tests\test_app.py "启动系统.bat"
git add -A -- "启动dev-v0.1.bat"
git status --short
git commit -m "feat: add SQLite lab catalog for dev-v0.2"
git tag -a dev-v0.2 -m "Complete development version 0.2"
```

验证：

```powershell
git status --short
git log --oneline --decorate -3
git tag --list
git show dev-v0.2:VERSION
```

正确结果：工作区干净；最新提交有`dev-v0.2`标签；旧的`dev-v0.1`仍保留；最后输出`dev-v0.2`。

把终点提交号、`10 passed`、7项手工验收和本版关键理解填入个人记录册。

## 14. 本章练习

练习在V0.2提交和标签之后进行；修改类练习结束后必须恢复并重新运行10项测试。

### 练习1：组合筛选

分别尝试：

```text
/labs?keyword=信息楼
/labs?status=维护中
/labs?keyword=投影&status=可预约
```

记录每次结果数量，并用`and`与`or`解释两个筛选条件怎样组合。

本练习不修改文件，无需恢复。

### 练习2：证明种子数据不会重复

连续停止和启动系统两次，再用第7.2节命令查询记录数量。说明`if lab_count == 0`的作用。

本练习不修改源码，无需恢复。

### 练习3：增加一个临时查询字段

在`lab_list`的`or_`中临时删除`Lab.equipment.like(like_value)`，再用`GPU`查询并观察测试失败。

恢复方法：

```powershell
git restore app.py
.\.venv\Scripts\python.exe -m pytest -q
```

### 练习4：观察404

比较`/labs/4`和`/labs/999`的状态与页面。说明为什么“无此数据”不能返回状态码200的空详情页。

本练习不修改文件，无需恢复。

### 练习5：验证数据库不应提交

执行：

```powershell
git status --short --ignored
git check-ignore -v instance\campus_lab.db
```

记录是哪一条`.gitignore`规则排除了数据库。

本练习不修改文件，无需恢复。

## 15. 两课时推进建议

### 第10课时：从内存列表到SQLite

```text
0—7分钟：核对V0.1并发现内存数据问题
7—15分钟：更新依赖、版本和启动脚本
15—25分钟：建立Lab模型并理解类—表—行
25—37分钟：替换app.py并首次创建数据库
37—45分钟：查询4条记录，解释配置、建表和种子数据
```

### 第11课时：完成查询、详情和验证

```text
0—18分钟：替换5个模板和CSS资源
18—27分钟：操作关键词、状态和详情查询
27—34分钟：替换并运行10项自动测试
34—39分钟：完成7项手工验收
39—42分钟：执行15文件机械核对
42—45分钟：提交并建立dev-v0.2标签
```

## 16. 本章完成检查

- [ ] 起点是测试通过且工作区干净的`dev-v0.1`。
- [ ] Flask-SQLAlchemy 3.1.1安装在个人`.venv`中。
- [ ] `models.py`中的`Lab`字段与类图一致。
- [ ] 首次启动生成`instance/campus_lab.db`。
- [ ] 重复启动不会重复插入种子数据。
- [ ] 首页显示4间实验室、3间可预约。
- [ ] 关键词和状态筛选均有效。
- [ ] 合法编号显示详情，不存在编号返回404。
- [ ] 预约下拉框只包含可预约实验室，且仍不能提交。
- [ ] 数据库和缓存没有进入Git提交。
- [ ] 7项手工验收均通过。
- [ ] 自动测试显示`10 passed`。
- [ ] 机械核对显示15行`PASS`。
- [ ] Git工作区干净，`dev-v0.1`和`dev-v0.2`标签都存在。
- [ ] 个人记录册已填写V0.2终点提交号、测试结果和数据库理解。
