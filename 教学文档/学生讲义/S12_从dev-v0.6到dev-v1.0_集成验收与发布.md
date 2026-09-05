# S12 从dev-v0.6到dev-v1.0：集成、验收与发布

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 生命周期位置 | 系统集成、验收与发布 |
| 起点 | 已测试并提交的`dev-v0.6` |
| 起点能力 | 学生预约、教师审批、输入校验、安全防伪和错误处理均可使用 |
| 终点 | `dev-v1.0`手工开发阶段完整发布基线 |
| 对应需求 | 新实现REQ-07、REQ-10；完整验收REQ-01—REQ-10 |
| 课时 | 第23—24课时，共90分钟 |
| 正式参考标签 | `dev-v1.0` |
| 教师参考提交 | `6827c0b` |
| 自动测试 | 34项全部通过 |

V0.6已经有学生和审批教师两条业务线。V1.0补齐管理员，并把七次开发形成的功能连接成可验收、可说明、可冻结的整体：

```text
学生查询实验室并提交预约
→ 审批教师通过或驳回
→ 学生查看结果并在允许状态下取消
→ 管理员在没有有效预约时维护实验室状态
→ 版本页说明发布内容
→ 健康接口证明应用和数据库可用
→ 自动测试与手工验收共同提供发布证据
```

版本号从0.6到1.0不是漏掉0.7、0.8和0.9，而是表示本课程约定的第一套完整范围已经达到发布基线。

## 2. 完整代码资源

- [A12 dev-v1.0完整代码附录](../完整代码附录/A12_dev-v1.0_完整代码.md)
- `教学资源\版本终点核对包\dev-v1.0`

A12由冻结标签机械生成，包含终点全部33个文件的完整代码、原始字节数、行数和SHA-256。正文负责说明复制顺序、运行结果和知识；所有终点文件以A12为最终核对依据。

## 3. 开始前检查`dev-v0.6`

停止服务器，在个人项目根目录执行：

```powershell
git status --short
git describe --tags --exact-match HEAD
.\.venv\Scripts\python.exe -m pytest -q
```

必须得到：工作区干净、当前标签为`dev-v0.6`、`28 passed`。

在记录册填写：

```text
版本名称：V1.0 集成、验收与发布
起点版本或提交号：填写自己的dev-v0.6提交号
本版要解决的问题：管理员功能尚未开放，七次开发缺少统一的端到端验收和发布证据
本版验收标准：管理员可安全启停实验室；版本与健康入口可用；REQ-01—REQ-10通过；34项测试通过
```

## 4. 先理解集成、系统测试、验收和发布

### 4.1 四个词分别回答什么问题

| 活动 | 核心问题 | 本项目的证据 |
| --- | --- | --- |
| 集成 | 各模块连接后，数据能否正确传递 | 学生的预约能进入教师队列，取消后管理员可以停用实验室 |
| 系统测试 | 完整系统在正常和异常场景下是否正确 | 浏览器手工用例、34项自动测试 |
| 验收 | 用户最初要求的功能是否全部达到 | REQ-01—REQ-10追踪表逐项通过 |
| 发布 | 哪一份经过验证的代码可以交付和恢复 | 干净提交、`VERSION`、README和`dev-v1.0`标签一致 |

测试全部通过但没有对应需求，不能说明做的是用户需要的系统；页面演示成功但没有固定提交，也不能说明以后还能找到同一份代码。

### 4.2 什么叫端到端测试

端到端不是把每个页面各打开一次，而是让一条真实业务数据穿过多个角色和模块：

```text
同一条Booking
PENDING（学生创建）
→ APPROVED（教师处理）
→ CANCELLED（学生取消）

同一条Booking关联的Lab
有PENDING或APPROVED时不能停用
→ Booking变为CANCELLED后可以停用
```

这条链路同时检查登录、角色、表单、CSRF、数据库关系、状态转换、历史记录和管理员规则，比几个互不相干的页面截图更能说明系统已经集成。

### 4.3 发布基线必须包含什么

本课程的最小发布基线包括：

- 源码与锁定依赖；
- 本机启动方法和演示账号；
- 明确版本号；
- 可观察的版本页与健康接口；
- 自动测试和端到端验收结果；
- 一个工作区干净、可定位的Git标签。

它仍是本机教学系统，不等于互联网生产部署。真实上线还需要正式Web服务器、HTTPS、密钥管理、数据库备份、日志监控和运维责任人。

## 5. 本版真实变化

`dev-v0.6`到`dev-v1.0`共有13个文件变化，其中新增6个、修改7个：

```text
新增
├─ README.md                    运行方法、账号和七个版本说明
├─ static/favicon.svg           浏览器页签图标
├─ templates/admin_labs.html   管理员实验室状态页面
├─ templates/version.html      版本、运行数据和技术路线
├─ tests/conftest.py           全测试共享的应用与客户端夹具
└─ tests/test_acceptance.py    三角色端到端验收

修改
├─ VERSION                     dev-v0.6 → dev-v1.0
├─ app.py                      管理员、版本、健康、环境配置与发布启动
├─ static/style.css            管理和版本页面样式
├─ templates/base.html         管理入口、页签图标和版本链接
├─ templates/dashboard.html    管理员统计与入口
├─ templates/index.html        V1.0完整能力说明
└─ tests/test_app.py           管理、健康和版本测试，共享夹具
```

本版不修改`models.py`、`validators.py`、依赖版本和已有预约/审批模板，不需要数据库结构迁移。终点共有33个受控文件。

## 6. 第一个小终点：一次同步完整生产文件

### 6.1 本步骤目标

目标：补齐管理员模块和发布入口，同时保持V0.6全部功能可运行。由于完整`app.py`同时包含管理员、配置和健康路由，本章采用一次同步复制，后面按功能分段理解。

从A12完整代码附录按下表操作：

| 文件 | 动作 | 可观察结果 |
| --- | --- | --- |
| `VERSION` | 整体替换 | 版本变为`dev-v1.0` |
| `app.py` | 用完整549行覆盖 | 增加管理员、版本、健康和发布配置 |
| `static/style.css` | 用完整1043行覆盖 | 新页面样式完整 |
| `templates/admin_labs.html` | 新建完整39行文件 | 管理员看到4间实验室和操作按钮 |
| `templates/version.html` | 新建完整36行文件 | 页面显示版本和运行数据 |
| `templates/base.html` | 整体替换 | 管理入口、版本链接和页签图标出现 |
| `templates/dashboard.html` | 整体替换 | 管理员看到总数与开放数 |
| `templates/index.html` | 整体替换 | 首页显示三角色集成结果 |
| `static/favicon.svg` | 新建完整4行文件 | 浏览器页签出现蓝色L图标 |
| `README.md` | 新建完整29行文件 | 项目根目录有运行与版本说明 |

执行语法检查：

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py models.py validators.py
```

没有输出才继续。复制后先不要建立V1.0标签，发布必须在验收之后。

### 6.2 启动并观察三个发布入口

双击`启动系统.bat`，检查：

1. 首页顶部和页脚都显示`dev-v1.0`。
2. 页脚“版本与运行信息”可打开`/version`。
3. `/version`显示4间实验室、4名演示用户和当前预约数量。
4. 单击“查看JSON健康检查”打开`/health`。
5. `/health`返回包含`status: ok`、`version: dev-v1.0`、`database: ok`的JSON。
6. 使用管理员`A001 / 123456`登录，工作台显示实验室总数4、开放数3，并出现“实验室管理”。

预约数量会随个人数据库中的历史操作变化，不要求固定为0；实验室和用户的初始数量应分别为4和4。

## 7. 第二个小终点：理解并验证管理员业务规则

### 7.1 两个新路由

| 请求 | 角色 | 作用 |
| --- | --- | --- |
| `GET /admin/labs` | 仅管理员 | 查询并显示全部实验室 |
| `POST /admin/labs/<lab_id>/toggle` | 仅管理员 | 在“可预约”和“维护中”之间切换 |

页面隐藏学生和审批教师的入口只是界面设计，`@role_required("admin")`才是服务器端权限边界。每间实验室都有独立POST表单，并继承V0.6的防伪令牌检查。

### 7.2 停用前为什么要查有效预约

管理员把一间开放实验室设为维护中之前，路由会联结`Booking`与`TimeSlot`，检查这间实验室是否存在以下状态：

```text
PENDING   待审批，学生已经提交
APPROVED  已通过，已经形成使用承诺
```

只要找到一条，返回400且不改变实验室状态。`REJECTED`和`CANCELLED`不再占用资源，因此不阻止停用。

规则顺序是：

```text
检查管理员身份
→ 查找实验室，不存在则404
→ 若当前可预约，先查询有效预约
→ 有有效预约：400，不保存
→ 无有效预约：改为维护中并提交
→ 当前维护中：恢复为可预约并提交
```

这体现跨模块约束：管理员模块不能只改`Lab.status`，必须先理解预约模块的数据状态。

### 7.3 先完成一次独立的管理检查

在新种子数据中，“网络技术实验室”初始为维护中。使用管理员账号进入实验室管理：

1. 单击它的“恢复开放”，预期提示已恢复开放。
2. 再单击“设为维护中”，只要该实验室没有有效预约，预期成功。
3. 退出管理员，使用学生账号直接打开`/admin/labs`，预期403。

操作之后理解：前两步验证正常状态切换，第三步验证权限；真正的预约冲突在第11节端到端验收中验证。

## 8. 第三个小终点：理解版本、健康和外部配置

### 8.1 `/version`和`/health`用途不同

| 入口 | 面向对象 | 输出 | 主要用途 |
| --- | --- | --- | --- |
| `/version` | 人 | HTML页面、版本、数量、技术路线 | 演示、验收和人工确认 |
| `/health` | 程序或运维人员 | 简短JSON | 自动判断应用和数据库查询是否可用 |

`health()`先执行一次数据库查询，再返回`database="ok"`。如果数据库连接失败，请求会失败，而不会给出虚假的正常结论。

### 8.2 为什么配置不能全部写死在源码

V1.0优先从环境变量读取三项运行配置：

| 环境变量 | 作用 | 未设置时的课堂默认值 |
| --- | --- | --- |
| `CAMPUS_LAB_SECRET_KEY` | 签名会话数据 | 课堂演示密钥 |
| `CAMPUS_LAB_DATABASE_URL` | 数据库连接地址 | 项目`instance`目录中的SQLite |
| `CAMPUS_LAB_PORT` | 监听端口 | 5000 |

代码不变，运行环境可以不同，这叫配置与代码分离。用当前PowerShell窗口做一次独立运行实验：

```powershell
$env:CAMPUS_LAB_SECRET_KEY = "v1-local-acceptance-secret"
$env:CAMPUS_LAB_DATABASE_URL = "sqlite:///acceptance-v1.db"
$env:CAMPUS_LAB_PORT = "5050"
.\.venv\Scripts\python.exe app.py
```

手工打开`http://127.0.0.1:5050/health`，应返回V1.0健康JSON。这个数据库与平时的`campus_lab.db`分开，适合完成可重复的干净验收；相对SQLite文件会放在应用的`instance`目录。如果该文件已经有课堂数据，可把URL中的文件名改为`acceptance-v1-2.db`。

按`Ctrl+C`停止后清除本窗口的临时配置：

```powershell
Remove-Item Env:CAMPUS_LAB_SECRET_KEY
Remove-Item Env:CAMPUS_LAB_DATABASE_URL
Remove-Item Env:CAMPUS_LAB_PORT
```

再双击`启动系统.bat`会恢复端口5000和默认数据库。V1.0关闭了调试模式，修改源码后需要手工重启；课堂内置服务器仍不是正式互联网部署服务器。

### 8.3 README为什么属于发布内容

一份代码如果只有作者自己知道怎样运行，就还不能可靠交付。V1.0的README明确给出：项目用途、技术路线、初始化、启动、地址、三个账号、七个基线和测试命令。请直接使用A12中的完整README，不把个人密码或本机绝对路径写进去。

## 9. 第四个小终点：建立共享测试环境和端到端验收

### 9.1 新建共享夹具

新建`tests\conftest.py`，完整内容如下：

```python
import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()
```

`conftest.py`是pytest自动发现的共享配置。`tmp_path`为每次测试建立临时目录，测试不会读写课堂手工操作的`instance\campus_lab.db`。测试显式注入密钥和数据库地址，也验证了`create_app(test_config)`支持不同运行环境。

### 9.2 整体替换应用测试

从A12复制完整369行`tests/test_app.py`覆盖现有文件。V1.0把重复的`app`和`client`夹具移到`conftest.py`，并新增五类功能测试：

- 健康接口与版本页；
- 管理员正常改变实验室状态；
- 非管理员不能进入管理功能；
- 有有效预约时不能停用实验室；
- 管理页面的所有POST操作都有防伪令牌。

不要把V0.6文件与V1.0片段拼接，否则容易同时保留两套夹具或漏掉令牌测试。

### 9.3 新建完整端到端测试

从A12复制完整92行`tests/test_acceptance.py`。该文件只包含一项测试，但它连续执行：

```text
学生20260001登录并提交
→ 教师T1001登录并通过
→ 学生重新登录并取消
→ 管理员A001登录并停用关联实验室
→ 数据库确认状态历史为PENDING、APPROVED、CANCELLED
→ 数据库确认实验室为维护中
```

这1项不是“只测了一个小功能”，而是最终验收的关键业务主线。测试文件的完整代码必须来自A12，正文流程图不能代替可运行源码。

## 10. 执行34项自动测试

完全停止服务器，执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

预期：

```text
..................................                                       [100%]
34 passed
```

测试项构成：

| 文件 | 测试项数 | 作用 |
| --- | ---: | --- |
| `tests/test_validators.py` | 4 | 输入校验单元测试 |
| `tests/test_app.py` | 29 | 页面、数据库、身份、权限、业务、安全、管理和运行接口集成测试 |
| `tests/test_acceptance.py` | 1 | 三角色端到端验收 |
| 合计 | 34 | 旧功能回归与V1.0新增功能全部验证 |

`test_app.py`有28个测试函数，其中导航测试使用两个参数运行两次，因此形成29个测试项。

分别运行各层证据：

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_validators.py -q
.\.venv\Scripts\python.exe -m pytest tests\test_app.py -q
.\.venv\Scripts\python.exe -m pytest tests\test_acceptance.py -q
```

预期依次为`4 passed`、`29 passed`、`1 passed`。若最后一项失败，不能以另外33项成功为理由发布，因为跨角色连接仍可能有问题。

## 11. 在独立数据库中完成手工端到端验收

### 11.1 准备干净验收环境

用第8.2节的三个环境变量运行端口5050和`acceptance-v1.db`。第一次使用该文件时应有4间实验室、4名用户、16个未来时段和0条预约。

打开一个浏览器窗口，以下每次切换角色都先单击“退出”，不能直接访问登录页覆盖当前会话。

### 11.2 学生提交并记录关联实验室

用`20260001 / 123456`登录：

1. 选择“软件工程实验室”的一个可预约时段。
2. 用途填写“课程最终验收演示”。
3. 人数填写20，联系方式填写`13800000001`。
4. 提交后记录预约编号、实验室名称和时段。

预期状态为待审批，时间线有`PENDING`创建记录。

### 11.3 管理员验证待审批预约会阻止停用

退出学生，使用`A001 / 123456`登录，进入实验室管理，对刚才关联的“软件工程实验室”单击“设为维护中”。

预期返回400并提示仍有待审批或已通过预约；实验室仍为可预约。把提示和实际状态记入REQ-07验收记录。

### 11.4 教师通过后再次验证冲突

退出管理员，使用`T1001 / 123456`登录，在待审批队列打开该预约，意见填写：

```text
验收信息完整，同意。
```

通过后，再切换到管理员尝试停用同一实验室。预期仍返回400，因为`APPROVED`也是有效预约。

### 11.5 学生取消后管理员完成停用

切回学生，在“我的预约”中打开该预约并取消。确认时间线依次包含：

```text
PENDING → APPROVED → CANCELLED
```

再次切换管理员，停用同一实验室。预期成功变为维护中。截图或记录成功结果后，再单击“恢复开放”，使演示环境便于后续使用。

### 11.6 检查版本和健康证据

不登录也能打开：

```text
http://127.0.0.1:5050/version
http://127.0.0.1:5050/health
```

记录V1.0版本、4间实验室、4名用户、至少1条预约和健康JSON。最后停止服务器并按第8.2节清除三个临时环境变量。

## 12. 用需求追踪表作出发布决定

在记录册逐项填写“通过/不通过”和证据，不能只写“系统能运行”：

| 需求 | V1.0验收证据 |
| --- | --- |
| REQ-01 | 首页和实验室列表可访问，系统名称与入口可见 |
| REQ-02 | 4间种子实验室来自SQLite；关键词、状态筛选和详情有效；不存在编号404 |
| REQ-03 | 三类账号登录后入口不同；错误密码、未登录和错误角色行为正确 |
| REQ-04 | 学生合法提交生成唯一编号和待审批记录；冲突时段不能重复预约 |
| REQ-05 | 学生只能查看本人预约，可取消待审批或已通过预约 |
| REQ-06 | 教师能通过或有理由地驳回，不能重复审批，历史可追踪 |
| REQ-07 | 只有管理员能启停；待审批或已通过预约阻止停用 |
| REQ-08 | 输入服务端校验、POST令牌、400/403/404说明页有效 |
| REQ-09 | 34项自动测试通过，包含正常、异常、权限和端到端流程 |
| REQ-10 | 虚拟环境可启动；README、`/version`、`/health`和环境配置可验证 |

发布判定规则：

```text
REQ-01—REQ-10全部通过
AND 34项自动测试通过
AND 手工端到端主线通过
AND 终点33文件一致
AND Git工作区干净
= 允许冻结dev-v1.0
```

任一P0需求、端到端主线或自动回归失败，结论必须是“暂不发布”，先记录缺陷、修复并重新回归。

## 13. 常见问题与恢复

### 问题1：管理员工作台仍显示“功能尚未开放”

`templates/dashboard.html`仍是V0.6。按A12整体替换，同时确认`app.py`向模板传入`lab_count`和`available_lab_count`。

### 问题2：管理员无法停用开放实验室

先看错误说明。若提示仍有待审批或已通过预约，这是规则正确工作，不是程序故障；应由学生取消或由教师驳回相关预约，再重试。

### 问题3：打开`/version`出现`TemplateNotFound`

确认完整文件位于`templates\version.html`，不是项目根目录，也不是`templates\versions.html`。

### 问题4：`/health`返回500

健康路由会真实查询数据库。检查`CAMPUS_LAB_DATABASE_URL`是否拼写正确、对应目录是否可写，并重新启动。清除错误环境变量后可回到默认SQLite。

### 问题5：设置5050后，双击批处理仍打开5000页面

端口实验应在设置变量的同一个PowerShell中直接运行`python app.py`，并手工打开5050。批处理内置的自动打开地址仍是5000。

### 问题6：测试报找不到`app`或`client`夹具

确认`tests\conftest.py`名称和目录正确，并完整复制20行内容。pytest会自动加载它，不需要在每个测试文件中导入。

### 问题7：测试数是33或35

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

检查是否漏了`test_acceptance.py`、漏了参数化导航项，或仍保留S11的临时边界测试。

### 问题8：代码改完但页面没有变化

V1.0以`debug=False`运行，不自动重新加载。按`Ctrl+C`完全停止，再重新启动。

### 完整恢复方法

保留个人`.git`、`.venv`和历史标签，用`教学资源\版本终点核对包\dev-v1.0`覆盖全部33个受控文件。测试数据库与手工数据库互不混用；重新运行34项测试，再执行第11节主线。

## 14. 终点源码机械核对

把参考路径改为教师资料在本机的实际位置：

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v1.0"
$courseFiles = @(
    ".gitignore",
    "README.md",
    "VERSION",
    "app.py",
    "models.py",
    "pytest.ini",
    "requirements.txt",
    "static\favicon.svg",
    "static\style.css",
    "templates\admin_labs.html",
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
    "templates\version.html",
    "tests\conftest.py",
    "tests\test_acceptance.py",
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

必须得到33行`PASS`。`instance`中的普通数据库与独立验收数据库都不属于发布源码。

### 14.1 最终代码核对索引

| 终点内容 | 完整代码或准确来源 |
| --- | --- |
| 全部33个文件 | A12完整代码附录，逐文件完整代码块 |
| 10个生产新增/修改文件 | 第6节按A12一次同步 |
| `tests/conftest.py` | 第9.1节完整20行代码；A12精确核对 |
| `tests/test_app.py` | 第9.2节按A12完整369行整体替换 |
| `tests/test_acceptance.py` | 第9.3节按A12完整92行新建 |
| 其余20个文件 | 从`dev-v0.6`保持不变，由33文件比较验证 |

## 15. 提交并建立`dev-v1.0`发布标签

只有第12节发布判定全部满足后执行：

```powershell
git status --short
git diff --stat
git add README.md VERSION app.py static\favicon.svg static\style.css
git add templates\admin_labs.html templates\base.html templates\dashboard.html
git add templates\index.html templates\version.html
git add tests\conftest.py tests\test_acceptance.py tests\test_app.py
git commit -m "release: integrate and verify dev-v1.0"
git tag -a dev-v1.0 -m "Release integrated course system dev-v1.0"
```

发布后检查：

```powershell
git status --short
git log --oneline --decorate -8
git tag --list
git show dev-v1.0:VERSION
git diff --stat dev-v0.6 dev-v1.0
.\.venv\Scripts\python.exe -m pytest -q
```

预期：工作区干净；标签指向本次发布提交；版本为`dev-v1.0`；最终回归仍为`34 passed`。把提交号、标签、验收结论和证据位置写入记录册。

## 16. 本章练习

### 练习1：作出发布决定

假设33项测试通过，但三角色端到端测试在管理员停用处失败；写出“发布/暂不发布”的决定、依据和下一步。不能用通过率百分比代替关键流程判断。

本练习不修改源码，无需恢复。

### 练习2：验证外部端口配置

把`CAMPUS_LAB_PORT`临时设为5051，启动后用浏览器和`Invoke-RestMethod http://127.0.0.1:5051/health`各检查一次，再清除变量。

本练习只改变当前PowerShell环境，按第8.2节清除即可恢复。

### 练习3：破坏管理员冲突规则

提交V1.0后，临时把`Booking.status.in_(["PENDING", "APPROVED"])`改为只检查`PENDING`，运行：

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_app.py::test_admin_cannot_disable_lab_with_active_booking -q
```

解释为什么测试数据当前为待审批时可能仍通过，以及还应增加一个“已通过预约阻止停用”的用例。这是在识别测试覆盖空白，不是宣布错误修改正确。

恢复：

```powershell
git restore app.py
```

### 练习4：建立一条完整追踪链

任选REQ-07或REQ-10，写出“需求编号→实现版本→路由或文件→自动测试→手工验收证据→发布标签”。每一环必须能指向真实名称。

本练习不修改源码，无需恢复。

### 练习5：比较标签而不切换版本

```powershell
git show dev-v0.6:VERSION
git show dev-v1.0:VERSION
git diff --stat dev-v0.6 dev-v1.0
```

说明为什么发布标签比“最终版”“最终版2”文件夹更容易定位、比较和恢复。

本练习只读取Git历史，无需恢复。

## 17. 两课时推进建议

### 第23课时：管理员集成与发布配置

```text
0—7分钟：区分集成、系统测试、验收和发布
7—18分钟：按A12同步10个生产文件并语法检查
18—28分钟：管理员恢复/停用无预约实验室，验证非管理员403
28—36分钟：讲有效预约为什么阻止停用
36—42分钟：检查/version、/health和README
42—45分钟：用5050端口和独立数据库准备验收环境
```

### 第24课时：端到端验收与发布冻结

```text
0—8分钟：复制conftest、应用测试和端到端测试
8—15分钟：运行4、29、1及全部34项测试
15—31分钟：执行学生—管理员冲突—教师—学生—管理员手工主线
31—37分钟：逐项完成REQ-01—REQ-10追踪与发布判定
37—41分钟：执行33文件机械核对
41—45分钟：提交、建立dev-v1.0标签并完成最终回归
```

## 18. 本章完成检查

- [ ] 起点是28项测试通过且工作区干净的`dev-v0.6`。
- [ ] 我能区分集成、系统测试、验收测试和发布。
- [ ] V1.0的13个新增/修改文件全部来自A12完整代码。
- [ ] 管理员工作台显示4间实验室和3间初始开放实验室。
- [ ] 只有管理员能打开实验室管理和执行状态操作。
- [ ] 没有有效预约的实验室可以停用并恢复。
- [ ] 有`PENDING`或`APPROVED`预约时停用返回400且状态不变。
- [ ] `/version`显示V1.0、技术路线和实际数据数量。
- [ ] `/health`返回应用、版本和数据库正常信息。
- [ ] 我能用环境变量改变密钥、数据库和端口，并恢复默认环境。
- [ ] README包含运行、账号、版本和测试说明。
- [ ] 测试使用临时数据库，不污染手工操作数据。
- [ ] 4项单元、29项集成和1项端到端测试分别通过。
- [ ] 全部自动测试显示`34 passed`。
- [ ] 手工主线形成`PENDING→APPROVED→CANCELLED`历史，之后管理员可停用。
- [ ] REQ-01—REQ-10都有明确验收结论和证据。
- [ ] 机械核对显示33行`PASS`。
- [ ] Git工作区干净，发布提交和`dev-v1.0`标签一致。
- [ ] 我能说明本机教学发布与真实互联网生产部署的差距。
