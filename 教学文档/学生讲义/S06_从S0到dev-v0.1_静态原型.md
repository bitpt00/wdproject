# S06 从S0到dev-v0.1：静态原型

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 起点 | 个人仓库中的S0基线提交 |
| 终点 | `dev-v0.1`静态原型 |
| 对应需求 | REQ-01；为REQ-02、REQ-04提供页面原型 |
| 课时 | 第8—9课时，共90分钟 |
| 正式参考标签 | `dev-v0.1` |
| 教师参考提交 | `215a1d6` |
| 自动测试 | 6项全部通过 |

终点必须能够观察到：

- Flask应用在`http://127.0.0.1:5000`启动。
- 首页、实验室列表和预约表单三个入口均可打开。
- 页面共享导航、页脚、版本条和样式。
- 列表显示三条程序内示例数据。
- 从人工智能实验室进入表单时，该实验室被预先选中。
- 预约按钮不可提交，页面明确说明数据暂不保存。

本版不做数据库、登录、真正预约和审批。看到表单不等于已经完成业务功能。

## 2. 开始前检查S0

打开个人项目`my-campus-lab`，在PowerShell执行：

```powershell
git branch --show-current
git status --short
git log --oneline --decorate -1
git tag --list
```

正确起点应满足：

- 当前分支是`main`。
- `git status --short`没有输出。
- 最新提交信息包含`create S0 baseline`。
- 尚无`dev-v0.1`标签。
- 根目录只有三个已跟踪起点文件；`.venv`可以存在但已被忽略。

如果起点不干净，先用`git diff`查看改动。不要带着不明修改开始本版。

在《学生项目开发记录册》第15节复制一份“单版本记录模板”，填写：

```text
版本名称：V0.1 静态原型
起点版本或提交号：填写自己的S0提交号
本版要解决的问题：目前个人项目还没有可运行的网站，需求和页面结构无法观察
本版验收标准：首页、列表、静态表单可打开，6项自动测试通过
```

## 3. 认识本版文件结构

V0.1终点包含13个文件：

```text
my-campus-lab/
├─ .gitignore                       S0已有
├─ requirements.txt                 S0已有
├─ 初始化开发环境.bat                S0已有
├─ VERSION                          本版新增
├─ app.py                           本版新增
├─ 启动dev-v0.1.bat                 本版新增
├─ 运行测试.bat                      本版新增
├─ static/
│  └─ style.css                     本版新增，复制课程样式资源
├─ templates/
│  ├─ base.html                     本版新增
│  ├─ index.html                    本版新增
│  ├─ labs.html                     本版新增
│  └─ reservation_form.html         本版新增
└─ tests/
   └─ test_app.py                   本版新增
```

先在项目根目录执行：

```powershell
New-Item -ItemType Directory -Force -Path static, templates, tests
```

预期看到三个目录，命令重复执行也不会删除已有内容。

## 4. 步骤1：先让最小Flask应用运行

### 4.1 本步目标

先只建立一个网址和一行文字，验证“Python解释器—Flask—浏览器”最短链路。这个`app.py`是中间状态，第7步会整体替换成V0.1最终内容。

### 4.2 新建`VERSION`

在项目根目录新建文件`VERSION`，完整内容只有一行：

```text
dev-v0.1
```

### 4.3 新建临时`app.py`

在项目根目录新建`app.py`，完整粘贴：

```python
from flask import Flask


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
```

### 4.4 运行并观察

```powershell
.\.venv\Scripts\python.exe app.py
```

若个人项目尚未创建`.venv`，先停止操作并双击`初始化开发环境.bat`。

命令窗口出现：

```text
* Running on http://127.0.0.1:5000
```

浏览器访问：

```text
http://127.0.0.1:5000/
```

预期只看到：

```text
校园实验室预约系统 dev-v0.1
```

观察完成后回到终端按`Ctrl+C`。

### 4.5 操作之后理解代码

- `Flask(__name__)`创建Web应用对象。
- `@app.get("/")`把根网址和`index`函数连接起来，这种连接称为路由。
- 浏览器发出GET请求后，Flask执行`index`并把字符串作为响应返回。
- `create_app`采用应用工厂形式，后面的测试可以使用不同配置创建应用。
- `if __name__ == "__main__"`保证直接运行`app.py`时才启动开发服务器。
- `debug=True`便于课堂开发时自动重载，不是生产部署配置。

## 5. 步骤2：建立共享页面布局和样式

### 5.1 本步目标

先准备页面模板和样式文件。此时不急着运行，等第7步的三个路由全部就绪后统一观察。

### 5.2 复制`static/style.css`

V0.1样式文件有551行，主要用于页面布局和视觉效果，不是本课的编程重点。不要手工逐行输入。

从课程材料复制：

```text
教学资源\版本终点核对包\dev-v0.1\static\style.css
```

粘贴到个人项目：

```text
static\style.css
```

复制后确认文件名不是`style.css.txt`，文件大小约为9 KB。

### 5.3 新建`templates/base.html`

完整粘贴：

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

### 5.4 新建`templates/index.html`

完整粘贴：

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

### 5.5 操作之后理解模板

- `base.html`保存所有页面共用的HTML骨架、导航和页脚。
- `{% block content %}`为子页面保留可替换区域。
- `{% extends "base.html" %}`表示首页复用公共骨架。
- `{{ app_version }}`输出Flask传入的版本值。
- `url_for('lab_list')`根据路由函数名生成网址，避免在多个模板中重复硬编码。
- CSS只负责显示效果。即使样式文件丢失，业务路由仍可能返回HTML，但页面会失去布局。

## 6. 步骤3：建立实验室列表页面

### 6.1 新建`templates/labs.html`

完整粘贴：

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

### 6.2 操作之后理解循环和判断

- `{% for lab in labs %}`为每条实验室数据生成一张卡片。
- `lab.name`在Jinja2中可以读取字典中的`name`值。
- `"%03d"|format(lab.id)`把编号1显示为`001`。
- `{% if lab.status == '可预约' %}`决定显示可点击链接还是“当前不能选择”。
- 这里的判断只影响页面展示。V0.1没有服务端预约提交，所以还不构成完整安全规则。

## 7. 步骤4：建立静态预约表单并完成最终`app.py`

### 7.1 新建`templates/reservation_form.html`

完整粘贴：

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

表单中的按钮使用`type="button"`并带有`disabled`，因此输入内容不会发送到服务器。这是V0.1明确保留的功能缺口。

### 7.2 用终点代码整体替换`app.py`

打开根目录`app.py`，全选原临时代码，完整替换为：

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

### 7.3 运行三个页面

```powershell
.\.venv\Scripts\python.exe app.py
```

依次访问：

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/labs
http://127.0.0.1:5000/reservations/new?lab=2
```

可见结果：

- 首页显示完整布局和`dev-v0.1`。
- 列表显示三间实验室，其中两间可预约、一间维护中。
- 第三个网址的下拉框预选“人工智能实验室”。
- 页面之间的首页、实验室和预约申请导航均可使用。

观察完成后按`Ctrl+C`停止服务器。

### 7.4 操作之后理解最终路由

- `render_template("labs.html", labs=LABS)`把Python列表传给模板。
- `request.args.get("lab", type=int)`读取网址查询参数中的`lab=2`，并转换为整数。
- `@app.context_processor`让所有模板都能使用`app_version`，不必每个路由重复传入。
- 三条实验室数据随着Python进程存在，并没有写入磁盘；重启后仍来自代码常量`LABS`。

## 8. 步骤5：增加启动脚本和测试入口

### 8.1 新建`启动dev-v0.1.bat`

完整粘贴：

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

双击它，预期出现服务器窗口并自动打开浏览器。若浏览器没有自动出现，服务器窗口仍在运行时可以手工访问首页。

### 8.2 新建`运行测试.bat`

完整粘贴：

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

这个脚本暂时还没有测试文件。下一步建立测试后再执行。

## 9. 步骤6：用自动测试固定V0.1行为

### 9.1 新建`tests/test_app.py`

完整粘贴：

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

### 9.2 运行测试

确保服务器已经停止，再执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

也可以双击`运行测试.bat`。正确结果为：

```text
......                                                                   [100%]
6 passed
```

### 9.3 操作之后理解测试

- `fixture client`为每个测试提供一个不需要真正打开浏览器的Flask测试客户端。
- 状态码`200`表示请求正常完成。
- 测试不仅检查“网址能开”，还检查版本、实验室名称、表单字段和导航文字。
- 参数化测试用一段代码分别检查三个网址，所以终端显示的用例数多于测试函数数。
- 自动测试可以重复执行，是V0.1终点是否稳定的证据。

## 10. 手工验收V0.1

先双击`启动dev-v0.1.bat`，按顺序执行：

| 用例编号 | 操作 | 预期结果 | 我的结果 |
| --- | --- | --- | --- |
| MT-V01-01 | 未登录打开首页 | 显示系统名称、版本和三个业务说明 |  |
| MT-V01-02 | 打开实验室列表 | 显示3间实验室；2间可预约、1间维护中 |  |
| MT-V01-03 | 单击人工智能实验室“填写预约信息” | 打开表单，人工智能实验室已选中 |  |
| MT-V01-04 | 填写表单并观察提交按钮 | 按钮禁用，不能提交，页面说明暂不保存 |  |
| MT-V01-05 | 在三个页面分别使用导航 | 首页、实验室、预约申请入口均可见可用 |  |

把结果填写到记录册第16节；发现失败时不要先填写“通过”，记录实际页面和复现步骤。

手工验收结束后按`Ctrl+C`停止服务器。

## 11. 常见问题与恢复

### 问题1：`TemplateNotFound`

检查文件是否位于`templates`，而不是`template`；再检查文件名是否完全为`index.html`、`labs.html`或`reservation_form.html`。

### 问题2：`BuildError`并提到`lab_list`或`reservation_form`

模板中的`url_for`找不到同名路由函数。确认`app.py`已经整体替换为第7.2节最终代码，不要只增加一部分。

### 问题3：页面只有文字，没有样式

在浏览器中直接访问：

```text
http://127.0.0.1:5000/static/style.css
```

若返回404，检查`static/style.css`的位置和扩展名。

### 问题4：修改后页面没有变化

先按`Ctrl+C`停止旧服务器，再重新运行；浏览器按`Ctrl+F5`强制刷新，避免使用缓存样式。

### 问题5：测试导入了课程演示项目，而不是个人项目

执行：

```powershell
Get-Location
.\.venv\Scripts\python.exe -c "import app; print(app.__file__)"
```

输出路径必须位于个人`my-campus-lab`目录。

### 问题6：测试数量不是6

执行：

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

检查`tests/test_app.py`是否保存、文件名是否误成`test_app.py.txt`，以及参数化路径是否完整。

### 完整恢复方法

如果多处代码已经混乱：

1. 先把自己的错误现象记录在记录册。
2. 保留S0提交，不删除`.git`。
3. 从`教学资源\版本终点核对包\dev-v0.1`逐文件复制到个人项目。
4. 不复制任何`.git`或`.venv`目录；核对包本身不含这些目录。
5. 重新运行6项测试。
6. 通过后再完成Git提交和标签。

恢复包用于掉队救援和最终核对，不代替前面的逐步操作。

## 12. 终点源码机械核对

### 12.1 核对包来源

目录`教学资源\版本终点核对包\dev-v0.1`由教师仓库的`dev-v0.1`标签机械导出，共13个文件；不是根据讲义重新手工整理的副本。

### 12.2 运行文本比较

保持PowerShell当前目录为个人项目根目录。把第一行路径改成自己电脑上课程材料的实际位置，然后完整执行：

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v0.1"
$courseFiles = @(
    ".gitignore",
    "VERSION",
    "app.py",
    "requirements.txt",
    "static\style.css",
    "templates\base.html",
    "templates\index.html",
    "templates\labs.html",
    "templates\reservation_form.html",
    "tests\test_app.py",
    "初始化开发环境.bat",
    "启动dev-v0.1.bat",
    "运行测试.bat"
)
foreach ($courseFile in $courseFiles) {
    $mine = (Get-Content -LiteralPath $courseFile -Raw -Encoding UTF8).Replace("`r`n", "`n")
    $answer = (Get-Content -LiteralPath (Join-Path $courseAnswerRoot $courseFile) -Raw -Encoding UTF8).Replace("`r`n", "`n")
    if ($mine -ceq $answer) {
        "PASS  $courseFile"
    } else {
        "CHECK $courseFile"
    }
}
```

正确结果应有13行`PASS`，不能出现`CHECK`。这个比较会忽略Windows与Linux换行方式的差异，但不会忽略变量名、路由、文字、缩进或多余内容。

如果出现`CHECK`，用编辑器的文件比较功能查看个人文件与核对包文件，只修正显示差异的文件，再重新运行全部测试。

### 12.3 最终代码核对索引

本章以下位置给出的终点代码与`dev-v0.1`标签一致：

| 最终文件 | 完整代码或准确来源 |
| --- | --- |
| `.gitignore` | S02第8.1节；S0起点未修改 |
| `requirements.txt` | S02第14.1节；S0起点未修改 |
| `初始化开发环境.bat` | S01第6.2节；S0起点未修改 |
| `VERSION` | 本章第4.2节 |
| `app.py` | 本章第7.2节 |
| `static/style.css` | 从机械导出的终点核对包复制 |
| `templates/base.html` | 本章第5.3节 |
| `templates/index.html` | 本章第5.4节 |
| `templates/labs.html` | 本章第6.1节 |
| `templates/reservation_form.html` | 本章第7.1节 |
| `tests/test_app.py` | 本章第9.1节 |
| `启动dev-v0.1.bat` | 本章第8.1节 |
| `运行测试.bat` | 本章第8.2节 |

### 12.4 三个起点文件的终点准确内容

V0.1没有修改下面三个S0文件。为使本手册可以独立核对，它们的终点内容再次列出。

`.gitignore`：

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.py[cod]
instance/
```

`requirements.txt`：

```text
Flask==3.1.3
pytest==9.1.1
```

`初始化开发环境.bat`：

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

## 13. 提交并建立`dev-v0.1`标签

只有手工验收、6项测试和13个文件核对全部通过后，才执行版本操作。

### 13.1 查看本版变化

```powershell
git status --short
git diff --stat
```

不要提交`.venv`、`__pycache__`或`.pytest_cache`。

### 13.2 明确暂存终点文件

```powershell
git add VERSION app.py "启动dev-v0.1.bat" "运行测试.bat"
git add static\style.css
git add templates\base.html templates\index.html templates\labs.html templates\reservation_form.html
git add tests\test_app.py
git status --short
```

### 13.3 提交

```powershell
git commit -m "feat: complete static prototype for dev-v0.1"
```

### 13.4 建立正式标签

```powershell
git tag -a dev-v0.1 -m "Complete development version 0.1"
```

### 13.5 验证提交和标签

```powershell
git status --short
git log --oneline --decorate -2
git tag --list
git show dev-v0.1:VERSION
```

正确结果：

- 第一条命令无输出。
- 最新提交旁出现`tag: dev-v0.1`。
- 标签列表包含且只新增`dev-v0.1`。
- 最后一条命令输出`dev-v0.1`。

把终点提交号、标签、手工测试和`6 passed`记录到个人记录册V0.1版本记录中。

## 14. 本章练习

每个练习先完成观察，再恢复到正式终点；恢复后必须重新运行6项测试。

### 练习1：增加一条内存实验室数据

复制`LABS`中的一条字典，把编号改为4、名称改为“数字媒体实验室”，观察列表自动多出一张卡片。

恢复方法：完成观察后执行：

```powershell
git restore app.py
```

### 练习2：理解查询参数

分别访问：

```text
/reservations/new?lab=1
/reservations/new?lab=2
/reservations/new?lab=999
```

记录下拉框的差异，并说明为什么第三个地址没有任何实验室被选中。

本练习不修改文件，无需恢复。

### 练习3：观察模板继承

在`base.html`页脚中临时增加自己的学号，刷新三个页面，观察它们是否同时变化。

恢复方法：

```powershell
git restore templates\base.html
```

### 练习4：让一项测试先失败再恢复

在`index.html`中把页面主标题临时改为“实验室系统”，运行测试并找到失败断言。

恢复方法：

```powershell
git restore templates\index.html
.\.venv\Scripts\python.exe -m pytest -q
```

最终必须重新看到`6 passed`。

### 练习5：判断原型边界

填写表单后尝试提交，说明为什么按钮禁用是正确的V0.1设计，而不是本版缺陷；再指出真正提交预约计划在哪个版本实现。

本练习不修改文件，无需恢复。

## 15. 两课时推进建议

### 第8课时：从空项目到可观察页面

```text
0—8分钟：核对S0与V0.1终点
8—18分钟：完成最小Flask应用并打开纯文字首页
18—30分钟：建立公共模板、首页和样式
30—39分钟：建立实验室列表模板
39—45分钟：解释路由、模板继承、循环与判断
```

课时结束标志：最小Flask链路已经验证，四个模板与样式文件就位。

### 第9课时：完成原型并冻结版本

```text
0—12分钟：建立静态预约表单并替换最终app.py
12—20分钟：运行三个页面并解释查询参数
20—29分钟：建立测试文件和两个脚本
29—35分钟：执行6项自动测试
35—40分钟：完成5项手工验收
40—43分钟：执行13文件机械核对
43—45分钟：提交并建立dev-v0.1标签
```

## 16. 本章完成检查

只有以下项目全部通过，才进入S07《从dev-v0.1到dev-v0.2：数据库与查询》。

- [ ] 本版从个人S0干净提交开始。
- [ ] 项目结构包含规定的13个终点文件。
- [ ] 首页、实验室列表和静态预约表单均可打开。
- [ ] 三个页面共享导航、页脚和版本信息。
- [ ] 列表显示三条内存示例数据及正确状态。
- [ ] `lab=2`能够预选人工智能实验室。
- [ ] 预约按钮保持禁用，数据不会保存。
- [ ] 我能解释路由、模板继承、循环、判断和查询参数。
- [ ] 5项手工验收均通过。
- [ ] 自动测试显示`6 passed`。
- [ ] 机械核对显示13行`PASS`。
- [ ] `git status --short`没有输出。
- [ ] 最新提交已经建立`dev-v0.1`标签。
- [ ] 个人记录册已填写终点提交号、测试结果和本版理解。
