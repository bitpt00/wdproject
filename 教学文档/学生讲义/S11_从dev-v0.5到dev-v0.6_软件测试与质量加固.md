# S11 从dev-v0.5到dev-v0.6：软件测试与质量加固

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 生命周期位置 | 测试、缺陷修复与质量加固 |
| 起点 | 已测试并提交的`dev-v0.5` |
| 起点能力 | 学生预约、教师审批和状态历史已经形成完整业务闭环 |
| 终点 | `dev-v0.6`软件测试与质量加固 |
| 对应需求 | REQ-08、REQ-09；回归验证REQ-01—REQ-06 |
| 课时 | 第20—22课时，共135分钟 |
| 正式参考标签 | `dev-v0.6` |
| 教师参考提交 | `697d352` |
| 自动测试 | 28项全部通过 |

V0.5已经“能完成业务”，但还不能只凭几次正常点击就宣布质量合格。V0.6要解决四个常见问题：

```text
表单校验散落在路由中，难以单独测试
→ 把预约和审批校验提取到validators.py

浏览器只要能发出POST，就可能冒用已经登录的会话
→ 所有POST表单加入会话防伪令牌

异常只返回生硬的状态码
→ 为400、403、404提供友好错误页

人工点击难以稳定重复
→ 用pytest保存正常、异常、权限和安全场景
```

本章的重点不是背诵测试名词，而是把一项业务规则变成可重复执行的检查，并亲自经历一次“发现缺陷—定位原因—修复—回归测试”。

## 2. 完整代码资源

- [A11 dev-v0.6完整代码附录](../完整代码附录/A11_dev-v0.6_完整代码.md)
- `教学资源\版本终点核对包\dev-v0.6`

A11包含终点全部27个文件的完整代码、原始字节数、行数和SHA-256。正文只完整列出本章最适合讲解的两个小文件；`app.py`、页面和大测试文件必须从A11整体复制，不允许只复制正文中的讲解片段。

## 3. 开始前检查`dev-v0.5`

停止正在运行的服务器，在个人项目根目录执行：

```powershell
git status --short
git describe --tags --exact-match HEAD
.\.venv\Scripts\python.exe -m pytest -q
```

预期结果：

```text
工作区没有未提交文件
当前标签：dev-v0.5
......................                                                   [100%]
22 passed
```

若不是这三个结果，不进入V0.6。先按S10完成恢复、测试和提交。

在项目记录册填写本版任务：

```text
版本名称：V0.6 软件测试与质量加固
起点版本或提交号：填写自己的dev-v0.5提交号
本版要解决的问题：异常输入、安全写操作和错误路径缺少集中、可重复的验证
本版验收标准：校验器可单测；无令牌POST返回400；400/403/404有说明页；28项测试通过
```

## 4. 先建立测试的整体认识

### 4.1 测试到底在做什么

软件测试是使用明确的输入和操作去比较“实际结果”与“预期结果”。测试的目标是尽早发现风险并提供可以重复的证据，不是证明软件永远没有缺陷。

一个完整测试用例至少包含：

| 字段 | 回答的问题 | 示例 |
| --- | --- | --- |
| 用例编号 | 怎样唯一引用这次检查 | TC-BK-01 |
| 对应需求/规则 | 为什么要测 | RULE-03参加人数不能超过容量 |
| 前置条件 | 执行前系统处于什么状态 | 学生已登录，时段可预约，容量40 |
| 输入数据 | 用什么数据触发行为 | 人数41 |
| 操作步骤 | 怎样重复执行 | 选择时段、填写表单、提交 |
| 预期结果 | 正确行为是什么 | 提示1—40人，不保存预约 |
| 实际结果 | 系统真正发生了什么 | 执行后填写 |
| 结论 | 通过还是失败 | 实际与预期一致才通过 |

“点击一下看看”只有操作，没有明确预期，不能形成可复查的测试证据。

### 4.2 四个常见测试层次

| 层次 | 本项目中测什么 | 是否依赖完整网页和数据库 |
| --- | --- | --- |
| 单元测试 | `validate_booking_form()`等一个小函数 | 否 |
| 集成测试 | Flask路由、Session、ORM和临时数据库能否一起工作 | 是，使用测试客户端和临时数据库 |
| 系统测试 | 从浏览器按真实角色完成整个功能 | 是 |
| 验收测试 | 最终系统是否满足REQ-01—REQ-10 | 是，在S12集中执行 |

V0.6新增`test_validators.py`，让学生第一次清楚看到单元测试；`test_app.py`主要是集成测试；本章的手工测试属于系统层面的检查。

### 4.3 四种本课程真正要用的测试设计方法

1. **等价类**：把大量输入分为应当得到相同行为的类别，每类选代表值。例如人数可分为合法整数、过小、过大、非数字。
2. **边界值**：错误最容易出现在最小值、最大值及其相邻位置。例如容量40时选0、1、40、41。
3. **权限矩阵**：对同一功能分别使用学生、审批教师、管理员和未登录者，验证允许与禁止。
4. **状态转换**：先确定当前状态，再验证允许和禁止的下一状态。例如`PENDING→APPROVED`合法，`APPROVED→REJECTED`非法。

### 4.4 先设计，再执行

把下面至少8项抄入记录册“测试用例”表，暂时不要修改代码：

| 用例编号 | 方法 | 前置条件与输入 | 预期结果 |
| --- | --- | --- | --- |
| TC-BK-01 | 等价类 | 目的“课程作品展示”、人数20、合法联系方式 | 保存预约，状态为待审批 |
| TC-BK-02 | 边界值 | 实验室容量40，人数1 | 接受 |
| TC-BK-03 | 边界值 | 实验室容量40，人数40 | 接受 |
| TC-BK-04 | 边界值 | 实验室容量40，人数0 | 拒绝且不保存 |
| TC-BK-05 | 边界值 | 实验室容量40，人数41 | 拒绝且不保存 |
| TC-BK-06 | 等价类 | 人数输入`abc` | 拒绝且不保存 |
| TC-ROLE-01 | 权限矩阵 | 审批教师访问学生预约页 | 返回403 |
| TC-STATE-01 | 状态转换 | 已审批申请再次提交审批决定 | 返回400，状态和历史不改变 |
| TC-WEB-01 | 异常路径 | 访问`/labs/999` | 返回404说明页 |
| TC-SEC-01 | 安全路径 | 登录POST不携带防伪令牌 | 返回400说明页，不建立登录会话 |

操作之后理解：测试数据不是随便编几个数字。每个数字都来自需求、容量边界、角色权限或状态规则，因此失败时能指出究竟违反了哪条约定。

## 5. 本版真实变化

从`dev-v0.5`到`dev-v0.6`共有16个文件发生变化：

```text
新增
├─ validators.py                 预约与审批校验函数
├─ pytest.ini                   pytest的测试目录和报告配置
├─ tests/test_validators.py     4项单元测试
└─ templates/errors/
   ├─ 400.html                  请求或表单无效
   ├─ 403.html                  没有权限
   └─ 404.html                  页面或数据不存在

修改
├─ VERSION                      dev-v0.5 → dev-v0.6
├─ app.py                       调用校验器、检查令牌、注册错误处理器
├─ tests/test_app.py            所有合法POST携带令牌，新增2类异常测试
├─ static/style.css             错误页和提示样式
└─ 6个模板
   ├─ login.html                登录令牌
   ├─ base.html                 退出令牌与版本说明
   ├─ reserve.html              预约令牌
   ├─ booking_detail.html       取消令牌
   ├─ approval_detail.html      审批令牌
   └─ index.html                V0.6阶段说明
```

其余11个文件从V0.5保持不变。终点共27个受控文件。

## 6. 第一个小终点：把校验逻辑变成可单独测试的函数

### 6.1 本步骤目标和文件动作

目标：不启动浏览器、不连接数据库，也能验证预约和审批输入规则。

新建根目录文件`validators.py`，完整内容如下：

```python
def validate_booking_form(form, capacity):
    """清洗并校验预约表单，返回可保存的数据和错误列表。"""
    data = {
        "purpose": form.get("purpose", "").strip(),
        "attendee_count": form.get("attendee_count", "").strip(),
        "contact": form.get("contact", "").strip(),
    }
    errors = []

    if not 5 <= len(data["purpose"]) <= 200:
        errors.append("使用目的应填写5至200个字。")

    try:
        attendee_count = int(data["attendee_count"])
    except (TypeError, ValueError):
        attendee_count = 0
    if attendee_count < 1 or attendee_count > capacity:
        errors.append(f"参加人数应在1至{capacity}人之间。")

    if not 6 <= len(data["contact"]) <= 50:
        errors.append("联系方式应填写6至50个字符。")

    data["attendee_count_value"] = attendee_count
    return data, errors


def validate_approval_form(form):
    """校验审批决定；驳回必须说明原因。"""
    decision = form.get("decision", "")
    comment = form.get("comment", "").strip()
    errors = []

    if decision not in {"approve", "reject"}:
        errors.append("请选择通过或驳回。")
    if decision == "reject" and not 3 <= len(comment) <= 300:
        errors.append("驳回时请填写3至300个字的原因。")
    if decision == "approve" and len(comment) > 300:
        errors.append("审批意见不能超过300个字。")

    return decision, comment, errors
```

语法检查：

```powershell
.\.venv\Scripts\python.exe -m py_compile validators.py
```

没有输出表示语法通过。

### 6.2 新建完整单元测试

新建`tests\test_validators.py`，完整内容如下：

```python
from validators import validate_approval_form, validate_booking_form


def test_booking_validator_returns_clean_data():
    data, errors = validate_booking_form(
        {
            "purpose": " 课程作品展示 ",
            "attendee_count": "20",
            "contact": " 13800000001 ",
        },
        capacity=40,
    )

    assert errors == []
    assert data["purpose"] == "课程作品展示"
    assert data["attendee_count_value"] == 20
    assert data["contact"] == "13800000001"


def test_booking_validator_collects_multiple_errors():
    _, errors = validate_booking_form(
        {"purpose": "短", "attendee_count": "not-a-number", "contact": "1"},
        capacity=40,
    )

    assert len(errors) == 3


def test_approval_validator_requires_rejection_reason():
    decision, comment, errors = validate_approval_form(
        {"decision": "reject", "comment": "无"}
    )

    assert decision == "reject"
    assert comment == "无"
    assert errors == ["驳回时请填写3至300个字的原因。"]


def test_approval_validator_accepts_approval_without_comment():
    decision, comment, errors = validate_approval_form(
        {"decision": "approve", "comment": ""}
    )

    assert decision == "approve"
    assert comment == ""
    assert errors == []
```

只运行这个测试文件：

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_validators.py -q
```

预期：

```text
....                                                                     [100%]
4 passed
```

### 6.3 操作之后理解三个关键点

- **清洗**：`strip()`去掉用户无意输入的首尾空格，再进行长度判断和保存。
- **一次收集多项错误**：`errors`不是遇到第一项就退出；用户可以一次看到目的、人数、联系方式的全部问题。
- **纯函数容易测试**：校验器只接收普通数据并返回普通结果，不需要页面、Session或数据库，所以测试快、失败位置清楚。

这4项测试不是为了追求数量。第一项验证正常类及数据清洗，第二项验证多个无效类，后两项验证审批规则的允许与拒绝。

### 6.4 本步骤常见问题

- `ModuleNotFoundError: No module named 'validators'`：文件必须在项目根目录，与`app.py`同级，名称必须是`validators.py`。
- 只看到`collected 0 items`：测试文件必须放在`tests`目录，文件名和函数名都以`test_`开头。
- 中文断言失败：不要凭记忆改错误提示，按上方完整代码恢复。

## 7. 第二个小终点：让应用使用校验器并保护所有POST

### 7.1 整体替换`VERSION`和`app.py`

从A11完整代码附录复制：

1. 用A11中的完整`VERSION`覆盖当前文件。
2. 用A11中的完整481行`app.py`覆盖当前文件。

执行：

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py validators.py
```

没有输出才继续。本章不能只把旧路由中的三段判断删除；必须同时完成`validators`导入和函数调用，否则运行时会找不到校验函数。

### 7.2 读懂校验器怎样进入业务路由

预约路由现在按以下顺序工作：

```text
读取表单
→ validate_booking_form(request.form, slot.lab.capacity)
→ 有错误：显示全部提示，不写数据库
→ 无错误：使用清洗后的data创建Booking
```

审批路由执行：

```text
validate_approval_form(request.form)
→ 有错误：逐条flash并返回400，不改变预约
→ 无错误：执行合法状态转换并写入历史
```

路由负责“业务流程”，校验器负责“输入是否合格”。分离后，同一规则不用依赖页面才能检查。

### 7.3 新建pytest配置

新建`pytest.ini`，完整内容如下：

```ini
[pytest]
testpaths = tests
addopts = -ra
```

它告诉pytest默认只在`tests`目录收集测试，并在失败或跳过时给出简短附加报告。它不会让错误代码自动通过，也不会改变业务功能。

### 7.4 从A11一次复制完整页面和样式

按表执行，不要漏掉任何表单：

| 文件 | 动作 | 本版作用 |
| --- | --- | --- |
| `templates/errors/400.html` | 新建完整文件 | 解释请求或表单为什么无效 |
| `templates/errors/403.html` | 新建完整文件 | 解释当前账号没有权限 |
| `templates/errors/404.html` | 新建完整文件 | 解释页面或记录不存在 |
| `templates/login.html` | 整体替换 | 登录表单加入令牌 |
| `templates/base.html` | 整体替换 | 退出表单加入令牌，更新版本说明 |
| `templates/reserve.html` | 整体替换 | 预约表单加入令牌 |
| `templates/booking_detail.html` | 整体替换 | 取消表单加入令牌 |
| `templates/approval_detail.html` | 整体替换 | 审批表单加入令牌 |
| `templates/index.html` | 整体替换 | 显示V0.6质量主题 |
| `static/style.css` | 整体替换 | 增加错误页等样式 |

每个写操作表单都必须包含这一隐藏字段：

```html
<input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
```

终点一共有5个POST表单：登录、退出、提交预约、取消预约、审批决定。首页不是表单，`index.html`只更新阶段说明。

### 7.5 操作之后理解CSRF防护

浏览器登录后会自动携带Session Cookie。恶意网页可能诱导浏览器向本系统发送一个POST，请求会顺便带上Cookie，看起来像登录用户本人操作，这类风险称为跨站请求伪造。

V0.6采用最小同步令牌流程：

```text
服务器为当前会话生成随机_csrf_token
→ Jinja2把令牌写入本站表单的隐藏字段
→ 浏览器提交POST时同时提交令牌
→ before_request比较会话令牌与表单令牌
→ 不存在或不一致：立即返回400
→ 一致：继续执行原业务路由
```

`compare_digest()`用于稳定比较令牌。CSRF令牌不能替代登录、角色授权和业务状态检查；这四道防线解决的是不同问题。

V0.6还设置：

- `MAX_CONTENT_LENGTH=1024 * 1024`：限制一次请求体最大为1 MiB。
- `SESSION_COOKIE_HTTPONLY=True`：浏览器脚本不能直接读取会话Cookie。
- `SESSION_COOKIE_SAMESITE="Lax"`：限制部分跨站携带Cookie的场景。

这是课堂项目的基础加固，不等于已经达到生产系统的全部安全要求。V0.6中的固定开发密钥只适合本机教学，S12再把发布配置移出源码。

### 7.6 本步骤可见结果

双击`启动系统.bat`，按顺序执行：

1. 打开登录页，正常登录学生账号`20260001 / 123456`。
2. 提交一条合法预约，确认仍能保存。
3. 退出后登录`T1001 / 123456`，处理该预约。
4. 学生、审批教师执行越权访问时看到403说明页。
5. 打开`http://127.0.0.1:5000/labs/999`，看到404说明页。

若所有正常POST都变成400，最可能是某个模板漏了隐藏字段；不要删除服务器端`before_request`来绕过错误。

## 8. 第三个小终点：亲自验证错误路径和安全路径

### 8.1 验证无令牌POST

退出到登录页，按`F12`打开浏览器开发者工具，在“元素/Elements”中找到登录表单里的`_csrf_token`隐藏输入，临时删除这个DOM节点，再提交正确账号密码。

预期：

- 返回400页面并显示“表单已过期或来源无效”。
- 没有进入工作台。
- 刷新登录页后，模板重新生成隐藏字段，正常登录恢复。

这里修改的只是浏览器当前页面，不是源码，无需Git恢复。它证明服务器不能相信“页面上本来有这个字段”，而必须检查真正收到的请求。

### 8.2 验证输入边界

以容量40的实验室为例，在记录册填写实际结果：

| 输入 | 预期 |
| --- | --- |
| 目的4个字 | 提示目的应为5—200字，不保存 |
| 目的5个字 | 允许继续 |
| 人数0 | 提示1—40人，不保存 |
| 人数1 | 允许 |
| 人数40 | 允许 |
| 人数41 | 提示1—40人，不保存 |
| 人数`abc` | 提示1—40人，不保存 |
| 联系方式5字符 | 提示6—50字符，不保存 |
| 联系方式6字符 | 允许 |

浏览器输入框可能先阻止0、41或非数字。为了验证服务器而不是只验证浏览器，可在开发者工具中临时删除人数输入的`min`、`max`或改变`type`，再提交。测试完刷新页面即可恢复。

### 8.3 验证400、403和404不是同一种错误

| 状态码 | 本项目触发方式 | 表示的含义 |
| ---: | --- | --- |
| 400 | 无令牌POST、重复审批、无效业务状态 | 请求已到服务器，但当前请求不能被处理 |
| 403 | 学生打开审批队列、教师打开学生预约页 | 已识别当前用户，但该角色没有权限 |
| 404 | 打开`/labs/999`或不存在的预约 | 对应页面或数据不存在 |

如果所有错误都跳回首页，用户不知道发生了什么，测试人员也难以判断是哪一类失败。友好错误页必须保留正确HTTP状态码，而不是只显示一句提示后返回200。

## 9. 替换应用测试并执行28项自动测试

### 9.1 复制完整测试文件

用A11中的完整323行`tests/test_app.py`整体覆盖个人文件。不要在V0.5测试上手工零散添加，因为V0.6所有合法POST都必须改为通过`post_with_csrf()`提交。

新增辅助函数的逻辑是：

```text
在测试客户端的Session中准备令牌
→ 把同一个令牌加入表单数据
→ 使用测试客户端发送POST
```

它模拟本站真实表单。另一个测试故意直接`client.post()`且不带令牌，应得到400。

### 9.2 执行全部测试

完全停止服务器，然后运行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

预期：

```text
............................                                             [100%]
28 passed
```

28项由以下部分构成：

| 范围 | 测试项数 | 主要证据 |
| --- | ---: | --- |
| `tests/test_validators.py` | 4 | 正常清洗、多错误收集、驳回规则、通过规则 |
| `tests/test_app.py` | 24 | 页面、数据库、查询、预约、登录、权限、审批、安全和错误页 |
| 合计 | 28 | V0.1—V0.5旧能力没有回退，V0.6新能力可验证 |

`test_app.py`只有23个测试函数，但导航测试使用两个参数运行两次，所以形成24个测试项。测试数以pytest实际收集结果为准，不用函数数量猜测。

### 9.3 分层运行并定位失败

```powershell
# 只测两个纯校验函数
.\.venv\Scripts\python.exe -m pytest tests\test_validators.py -q

# 只测无令牌POST
.\.venv\Scripts\python.exe -m pytest tests\test_app.py::test_post_without_csrf_token_is_rejected -q

# 只测错误页
.\.venv\Scripts\python.exe -m pytest tests\test_app.py::test_custom_error_pages_explain_the_problem -q

# 第一次失败就停止，并显示更完整的信息
.\.venv\Scripts\python.exe -m pytest -x -vv
```

自动测试的价值不只是最后得到绿色结果。失败报告中的测试名、实际值、预期值和调用位置，能够缩小排查范围。

## 10. 完成一次真实的缺陷闭环

### 10.1 故意制造一个边界缺陷

先复制备份：

```powershell
Copy-Item -LiteralPath validators.py -Destination validators.py.before-defect
```

把`validators.py`中的：

```python
if not 5 <= len(data["purpose"]) <= 200:
```

临时改成：

```python
if not 4 <= len(data["purpose"]) <= 200:
```

这会错误地接受4字目的。现有4项单元测试不一定发现这个问题，这正说明“测试通过”不代表“所有边界都测到了”。

### 10.2 先把失败写成测试

在`tests\test_validators.py`末尾临时增加：

```python
def test_booking_validator_rejects_four_character_purpose():
    _, errors = validate_booking_form(
        {"purpose": "课程展示", "attendee_count": "20", "contact": "123456"},
        capacity=40,
    )

    assert "使用目的应填写5至200个字。" in errors
```

运行：

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_validators.py -q
```

预期出现1项失败。把以下内容写入记录册“缺陷记录”：

```text
缺陷编号：BUG-V06-01
关联规则：使用目的5—200字
复现输入：课程展示（4字）、人数20、联系方式123456
预期结果：返回目的长度错误
实际结果：errors中没有该错误
原因：最小长度被错误地改为4
修复：恢复最小长度5
回归范围：校验器4项正式测试和全部应用测试
```

### 10.3 修复、恢复正式终点并回归

```powershell
Copy-Item -LiteralPath validators.py.before-defect -Destination validators.py -Force
Remove-Item -LiteralPath validators.py.before-defect
```

删除刚才临时增加的边界测试，使`tests\test_validators.py`恢复为A11的完整46行正式文件。再次执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

必须重新得到`28 passed`。

这里经历了完整闭环：

```text
发现异常
→ 用可重复输入稳定复现
→ 写清预期与实际
→ 定位根因
→ 修复
→ 重跑相关测试
→ 重跑全部旧测试，确认没有引入回归
→ 关闭缺陷
```

回归测试的含义是：修改后重新执行已经通过的相关测试，确认修复没有破坏旧功能。它不是“重新随便点一遍”。

## 11. 手工验收V0.6

| 用例编号 | 操作 | 预期结果 | 我的结果 |
| --- | --- | --- | --- |
| MT-V06-01 | 正常登录、退出 | 两个POST均成功 |  |
| MT-V06-02 | 删除登录页令牌后提交 | 返回400说明页，不登录 |  |
| MT-V06-03 | 合法预约并由教师审批 | 原有主流程仍能完成 |  |
| MT-V06-04 | 目的4字、人数20、联系方式合法 | 显示长度错误，不保存 |  |
| MT-V06-05 | 目的、人数和联系方式同时非法 | 一次显示3类错误，不保存 |  |
| MT-V06-06 | 审批驳回原因2字 | 返回400，预约仍为待审批 |  |
| MT-V06-07 | 审批通过意见超过300字 | 返回400，预约仍为待审批 |  |
| MT-V06-08 | 学生访问`/approvals` | 返回403友好页面 |  |
| MT-V06-09 | 打开`/labs/999` | 返回404友好页面 |  |
| MT-V06-10 | 对已处理申请重复审批 | 返回400友好页面，结果不变 |  |

每一项都在“我的结果”填写实际状态、页面提示或预约编号。只打勾不算测试记录。

## 12. 常见问题与恢复

### 问题1：所有登录和业务提交都返回400

检查5个POST表单是否都含`name="_csrf_token"`，并确认`inject_version()`返回了`csrf_token`函数。不要把`protect_post_requests()`删除。

### 问题2：报`jinja2.exceptions.UndefinedError: 'csrf_token' is undefined`

`app.py`和模板没有同步升级。用A11完整481行文件恢复`app.py`，确认上下文处理器包含：

```python
return {"app_version": VERSION, "csrf_token": csrf_token}
```

### 问题3：运行旧测试时大量POST变成400

V0.5的测试没有提交令牌。必须整体替换A11版`tests/test_app.py`，让合法POST调用`post_with_csrf()`；不能在服务器端为测试关闭安全检查。

### 问题4：错误发生后仍显示Flask默认英文页面

确认三个文件位于`templates\errors`，并确认`app.py`注册了400、403、404三个`errorhandler`。目录名不能写成`error`。

### 问题5：输入多个错误却只显示一个

校验器应把错误依次加入`errors`，全部检查完成后统一返回。不要在第一项错误处提前`return`。

### 问题6：测试数是27或29

执行：

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

核对是否漏了一个测试文件、保留了第10节的临时测试，或错误修改了参数化导航测试。

### 问题7：刷新页面后仍提示令牌过期

完全关闭该站点标签页，重新打开登录页；仍失败时清除`127.0.0.1`站点Cookie并重启服务器。不要手工固定隐藏字段的值。

### 完整恢复方法

保留个人`.git`、`.venv`、历史标签和数据库备份，用`教学资源\版本终点核对包\dev-v0.6`覆盖全部27个受控文件。确认没有`validators.py.before-defect`或临时测试，再运行28项测试。

## 13. 终点源码机械核对

把下面路径改为教师资料在本机的实际位置：

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v0.6"
$courseFiles = @(
    ".gitignore",
    "VERSION",
    "app.py",
    "models.py",
    "pytest.ini",
    "requirements.txt",
    "static\style.css",
    "templates\approval_detail.html",
    "templates\approvals.html",
    "templates\base.html",
    "templates\booking_detail.html",
    "templates\dashboard.html",
    "templates\errors\400.html",
    "templates\errors\403.html",
    "templates\errors\404.html",
    "templates\index.html",
    "templates\lab_detail.html",
    "templates\labs.html",
    "templates\login.html",
    "templates\my_bookings.html",
    "templates\reserve.html",
    "tests\test_app.py",
    "tests\test_validators.py",
    "validators.py",
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

必须得到27行`PASS`。数据库、`.venv`、`__pycache__`和pytest缓存不属于终点源码，不参加比较。

### 13.1 最终代码核对索引

| 终点内容 | 完整代码或准确来源 |
| --- | --- |
| 全部27个文件 | A11完整代码附录，逐文件完整代码块 |
| `validators.py` | 第6.1节完整40行代码；A11再次精确核对 |
| `tests/test_validators.py` | 第6.2节完整46行代码；A11再次精确核对 |
| `VERSION`、`app.py`、`pytest.ini` | 第7节按A11整体复制 |
| 6个修改模板、3个错误模板、CSS | 第7.4节按A11整体复制 |
| `tests/test_app.py` | 第9节按A11完整323行整体复制 |
| 其余11个文件 | 从`dev-v0.5`保持不变，由27文件比较验证 |

## 14. 提交并建立`dev-v0.6`标签

只有28项测试、10项手工验收、缺陷闭环和27文件核对全部通过后执行：

```powershell
git status --short
git diff --stat
git add VERSION app.py pytest.ini validators.py
git add static\style.css tests\test_app.py tests\test_validators.py
git add templates\approval_detail.html templates\base.html templates\booking_detail.html
git add templates\index.html templates\login.html templates\reserve.html
git add templates\errors\400.html templates\errors\403.html templates\errors\404.html
git commit -m "test: add validation and quality safeguards for dev-v0.6"
git tag -a dev-v0.6 -m "Complete development version 0.6"
```

验证：

```powershell
git status --short
git log --oneline --decorate -7
git tag --list
git show dev-v0.6:VERSION
git diff --stat dev-v0.5 dev-v0.6
```

预期工作区干净、`VERSION`为`dev-v0.6`，差异中出现6个新文件和10个修改文件。把提交号、28项测试、10项手工验收和`BUG-V06-01`关闭结果写入记录册。

## 15. 本章练习

### 练习1：补全预约边界用例

为使用目的5—200字、联系方式6—50字符各设计“最小值前一个、最小值、最大值、最大值后一个”四个用例，只写精确输入和预期，不需要输入200字到网页。

本练习不修改源码，无需恢复。

### 练习2：建立权限测试矩阵

以“查看个人预约、提交预约、审批预约”三项功能为行，以未登录、学生、审批教师、管理员为列，填写允许、重定向或403，并选择两项在浏览器实际验证。

本练习只产生测试记录，无需恢复。

### 练习3：观察测试能否发现模板遗漏

提交V0.6后，临时删除`templates\login.html`中的令牌隐藏字段，先运行28项自动测试，再从浏览器正常登录。记录两类检查是否都发现问题，并说明当前自动测试的覆盖空白。

恢复：

```powershell
git restore templates\login.html
```

### 练习4：破坏错误状态码

提交V0.6后，把404错误处理器返回值末尾的`, 404`临时删除，运行错误页测试，观察“页面看起来正确但HTTP状态错误”怎样被测试发现。

恢复：

```powershell
git restore app.py
.\.venv\Scripts\python.exe -m pytest -q
```

### 练习5：区分缺陷、修复和回归

使用第10节的`BUG-V06-01`，分别用一句话指出缺陷现象、根本原因、代码修复和回归范围。四项不能写成同一句“程序有错”。

本练习不修改源码，无需恢复。

## 16. 三课时推进建议

### 第20课时：从需求和规则设计测试

```text
0—6分钟：用一次“正常点击通过但边界失败”的演示引出测试
6—15分钟：讲测试用例七个字段和四个测试层次
15—27分钟：用预约人数讲等价类和边界值
27—36分钟：用三种角色讲权限矩阵，用审批讲状态转换
36—43分钟：学生在记录册完成至少8个用例
43—45分钟：抽查每个用例是否有明确预期
```

### 第21课时：校验器、安全和错误处理

```text
0—5分钟：确认V0.5为22 passed
5—17分钟：创建validators.py和4项单元测试，解释纯函数
17—29分钟：整体替换应用、配置、模板和样式
29—37分钟：用一次无令牌登录解释CSRF流程
37—43分钟：验证400、403、404和多个输入错误
43—45分钟：检查5个POST表单令牌是否齐全
```

### 第22课时：自动测试、缺陷闭环和冻结

```text
0—8分钟：替换test_app.py，运行28项测试
8—16分钟：按文件、单项和-x方式运行并读懂失败报告
16—29分钟：制造4字目的缺陷，写失败测试和缺陷记录
29—35分钟：恢复正式源码并完成28项回归
35—40分钟：完成10项手工验收中的关键抽查
40—43分钟：执行27文件机械核对
43—45分钟：提交并建立dev-v0.6标签
```

## 17. 本章完成检查

- [ ] 起点是22项测试通过且工作区干净的`dev-v0.5`。
- [ ] 我能说明测试用例的前置条件、输入、步骤、预期和实际结果。
- [ ] 我能用等价类、边界值、权限矩阵和状态转换设计用例。
- [ ] `validators.py`位于项目根目录，两个校验函数可独立调用。
- [ ] 4项校验器单元测试通过。
- [ ] 预约目的为5—200字、人数为1—容量、联系方式为6—50字符。
- [ ] 驳回原因3—300字，通过意见不超过300字。
- [ ] 登录、退出、预约、取消和审批5个POST表单都含防伪令牌。
- [ ] 无令牌POST返回400且不执行业务操作。
- [ ] 400、403、404都显示友好说明并保留正确状态码。
- [ ] 我完成了`BUG-V06-01`的复现、原因、修复和回归记录。
- [ ] 10项手工验收均记录了实际结果。
- [ ] 自动测试显示`28 passed`。
- [ ] 机械核对显示27行`PASS`。
- [ ] 工作区干净，提交和`dev-v0.6`标签可以查看。
- [ ] 我能解释单元、集成、系统、验收和回归测试在本项目中的区别。
