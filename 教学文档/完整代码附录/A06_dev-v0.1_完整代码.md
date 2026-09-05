# dev-v0.1 完整代码核对附录

> 本附录由冻结版本终点包机械生成，不是手工重新整理的代码。文件内容只统一为LF换行；原始字节数与SHA-256用于核对终点资源。

## 1. 文件清单

| 路径 | 原始字节数 | 代码行数 | 原始文件SHA-256 |
| --- | ---: | ---: | --- |
| `.gitignore` | 62 | 6 | `bb1173460471204c4b38c69ac9b1fe238efe3a175a029a3977a659bff182d955` |
| `VERSION` | 12 | 2 | `ebf4db0c6feec25726e50e12bc468c0bb3f5dd65b86d5e36e896d7b537acfe6b` |
| `app.py` | 1781 | 73 | `29b06b6c27caffd618c054d7e60e95dfc4519bfe0414a3bd7878ed517e9feaa6` |
| `requirements.txt` | 31 | 3 | `d10dcff248aaaedae49b35a4af6061ae8fd26953105cfdc4d5745a8a53d1ee70` |
| `static/style.css` | 8988 | 551 | `169b1749efe05afc05f59203a6ef6f36d7bb371a20311f52bf8007adae7a2b48` |
| `templates/base.html` | 1665 | 43 | `cf9364c2d1d1d45cf90cf2e896bf512760c3e5637391b28cd2024e92b2ebb945` |
| `templates/index.html` | 2702 | 63 | `52b3a9224744cea83905a01cf3615dca1ce9bc6538754679df09740560ae32fe` |
| `templates/labs.html` | 1641 | 47 | `59c403459d185eef69e9f10d4e2b6d846a6937f43598d278ef72abac0731237e` |
| `templates/reservation_form.html` | 3174 | 76 | `27c9be642809496cca6cf554b70a7f6256aeff33e0ee34c7a34741b197cd2133` |
| `tests/test_app.py` | 1471 | 51 | `4f623887d98be9e3ea773ad9c1b5ae4b48492949bb4920242f8b1a3cc0a75224` |
| `初始化开发环境.bat` | 529 | 26 | `233dfdaa0b6fc06efe8394712a96a31e28a3ed2c46d48e7317b9797d22f4d04e` |
| `启动dev-v0.1.bat` | 369 | 15 | `d38205f132da84b035d8b8228c8e0f459f68b356a08a59954697f44efc648e06` |
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
dev-v0.1

```

### `app.py`

```python
from flask import Flask, render_template, request


VERSION = "dev-v0.1"

# V0.1暂时使用内存中的示例数据。
# V0.2会把这些数据迁移到SQLite数据库。
LABS = [
    {
        "id": 1,
        "name": "软件工程实验室",
        "location": "信息楼 A301",
        "capacity": 40,
        "equipment": "台式计算机、投影设备",
        "status": "可预约",
    },
    {
        "id": 2,
        "name": "人工智能实验室",
        "location": "信息楼 A305",
        "capacity": 32,
        "equipment": "GPU工作站、投影设备",
        "status": "可预约",
    },
    {
        "id": 3,
        "name": "网络技术实验室",
        "location": "信息楼 B201",
        "capacity": 36,
        "equipment": "网络实验箱、台式计算机",
        "status": "维护中",
    },
]


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__)
    app.config.from_mapping(TESTING=False)

    if test_config:
        app.config.update(test_config)

    @app.context_processor
    def inject_version():
        return {"app_version": VERSION}

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/labs")
    def lab_list():
        return render_template("labs.html", labs=LABS)

    @app.get("/reservations/new")
    def reservation_form():
        selected_lab_id = request.args.get("lab", type=int)
        return render_template(
            "reservation_form.html",
            labs=LABS,
            selected_lab_id=selected_lab_id,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

```

### `requirements.txt`

```text
Flask==3.1.3
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

.prototype-card,
.feature-card,
.lab-card,
.reservation-form,
.stage-panel {
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
    .form-layout {
        grid-template-columns: 1fr;
    }

    .feature-grid,
    .lab-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero {
        padding-top: 54px;
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
        开发教学版 {{ app_version }} · 当前为页面原型，尚未接入数据库
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
                <a class="{{ 'active' if request.endpoint == 'lab_list' else '' }}" href="{{ url_for('lab_list') }}">实验室</a>
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
                本版本先完成可运行的网站骨架和主要页面。
            </p>
            <div class="hero-actions">
                <a class="button primary" href="{{ url_for('lab_list') }}">浏览实验室</a>
                <a class="button secondary" href="{{ url_for('reservation_form') }}">查看预约表单</a>
            </div>
        </div>
        <div class="prototype-card">
            <span class="prototype-label">当前版本</span>
            <strong>{{ app_version }}</strong>
            <p>页面和导航已经可以运行，数据仍是程序中的示例内容。</p>
            <ul class="check-list">
                <li>Flask应用可以启动</li>
                <li>路由能够打开不同页面</li>
                <li>Jinja2模板可以复用页面布局</li>
                <li>预约数据暂时不会保存</li>
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
                <p>查看实验室位置、容量、主要设备和当前状态。</p>
                <span class="state available">本版本可查看</span>
            </article>
            <article class="feature-card">
                <span class="step-number">02</span>
                <h3>提交预约</h3>
                <p>选择实验室、日期和时间，填写用途及参加人数。</p>
                <span class="state prototype">本版本仅展示表单</span>
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

### `templates/labs.html`

```html
{% extends "base.html" %}

{% block title %}实验室｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">实验资源</p>
        <h1>实验室列表</h1>
        <p>V0.1使用程序中的三条示例数据。V0.2将改为从SQLite数据库读取。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container lab-grid">
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
            {% if lab.status == '可预约' %}
            <a class="text-link" href="{{ url_for('reservation_form', lab=lab.id) }}">填写预约信息</a>
            {% else %}
            <span class="text-muted">当前不能选择</span>
            {% endif %}
        </article>
        {% endfor %}
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
        <p>本页面用于确认需要采集哪些信息。V0.1不会把表单内容保存到数据库。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container form-layout">
        <form class="reservation-form" aria-label="实验室预约表单">
            <div class="form-row">
                <label for="lab">实验室</label>
                <select id="lab" name="lab">
                    <option value="">请选择实验室</option>
                    {% for lab in labs if lab.status == '可预约' %}
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
                <strong>已经完成</strong>
                <p>页面结构、输入项、导航和基本样式。</p>
            </div>
            <div class="stage-item next">
                <strong>dev-v0.2</strong>
                <p>接入SQLite，让实验室数据能够保存和查询。</p>
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

from app import LABS, create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.1" in response.get_data(as_text=True)


def test_lab_page_shows_all_sample_labs(client):
    response = client.get("/labs")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    for lab in LABS:
        assert lab["name"] in page


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

### `启动dev-v0.1.bat`

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
