# S10 从dev-v0.4到dev-v0.5：教师审批与状态历史

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 起点 | 已测试并提交的`dev-v0.4` |
| 终点 | `dev-v0.5`教师审批与状态历史 |
| 对应需求 | REQ-06；完善REQ-04、REQ-05的状态证据 |
| 课时 | 第18—19课时，共90分钟 |
| 正式参考标签 | `dev-v0.5` |
| 教师参考提交 | `0c1944f` |
| 自动测试 | 22项全部通过 |

V0.4的预约只能停在“待审批”。V0.5形成第一个跨角色闭环：

```text
学生提交PENDING
→ 审批教师查看队列
→ 通过为APPROVED，或填写原因后驳回为REJECTED
→ 系统记录审批人、时间、意见和状态历史
→ 学生重新登录查看结果
```

本版的核心不是增加两个按钮，而是保证状态只能按规则变化、同一申请不能审批两次、每次变化有可追踪证据。

## 2. 完整代码资源

- [A10 dev-v0.5完整代码附录](../完整代码附录/A10_dev-v0.5_完整代码.md)
- `教学资源\版本终点核对包\dev-v0.5`

A10包含终点全部21个文件的完整代码块、原始字节数和SHA-256。正文中的片段用于讲解；实际操作必须按步骤复制附录中的完整文件。

## 3. 开始前检查`dev-v0.4`

```powershell
git status --short
git describe --tags --exact-match HEAD
.\.venv\Scripts\python.exe -m pytest -q
```

必须得到：工作区干净、当前标签为`dev-v0.4`、`18 passed`。

在记录册复制单版本模板：

```text
版本名称：V0.5 教师审批与状态历史
起点版本或提交号：填写自己的dev-v0.4提交号
本版要解决的问题：学生申请一直停在待审批，没有教师处理和变化记录
本版验收标准：队列可筛选、通过/驳回有效、不能重复审批、学生可看结果和历史、22项测试通过
```

## 4. 本版真实变化

V0.5终点有21个受控文件，比V0.4增加两个审批模板。

```text
models.py
├─ Booking增加review_comment、reviewed_by_id、reviewed_at
├─ User与Booking明确区分申请人和审批人外键
└─ 新增BookingHistory及状态中文属性

app.py
├─ 增加旧数据库审批字段升级
├─ 创建、取消预约时写历史
├─ 教师工作台统计待审批数量
├─ 增加审批队列和详情
└─ 增加通过、驳回和重复审批保护

templates/
├─ 新增approvals.html
├─ 新增approval_detail.html
├─ 学生详情增加审批意见和时间线
└─ 导航、工作台、首页显示审批入口和进度
```

本版没有改变依赖版本，也没有修改实验室筛选、登录页面、学生预约表单和“我的预约”模板。

## 5. 第一个小终点：扩展数据模型并升级旧数据库

### 5.1 替换`VERSION`

```text
dev-v0.5
```

### 5.2 同时整体替换两个Python文件

按顺序从A10附录复制：

1. 完整179行`models.py`覆盖个人文件。
2. 完整468行`app.py`覆盖个人文件。

必须一次完成两个文件再运行。原因是V0.4现有`bookings`表还没有三个审批列，仅替换模型后直接查询旧表会导致结构不一致。

执行语法检查：

```powershell
.\.venv\Scripts\python.exe -m py_compile models.py app.py
```

没有输出才继续。

### 5.3 启动一次完成数据库结构升级

```powershell
.\.venv\Scripts\python.exe app.py
```

看到服务器启动后按`Ctrl+C`。再执行：

```powershell
.\.venv\Scripts\python.exe -c "from app import app; from models import db; from sqlalchemy import inspect; c=app.app_context(); c.push(); i=inspect(db.engine); print('history_table=', 'booking_histories' in i.get_table_names()); print('booking_columns=', [x['name'] for x in i.get_columns('bookings') if x['name'].startswith('review')]); c.pop()"
```

预期包含：

```text
history_table= True
booking_columns= ['review_comment', 'reviewed_by_id', 'reviewed_at']
```

列顺序以实际输出为准，三个名称都出现即可。

### 5.4 操作之后理解数据库演进

`db.create_all()`能创建新的`booking_histories`表，但不会自动为已有`bookings`表添加列。因此`upgrade_database_schema()`执行：

```text
读取bookings现有列
→ 找出缺少的3个审批列
→ 对每个缺少列执行ALTER TABLE
→ 已存在时不重复增加
```

这是一段适合课堂SQLite项目的最小升级逻辑。真实长期项目通常使用专门的数据库迁移工具记录每次结构变化；这里先理解“代码升级时已有数据不能被随意丢弃”的核心问题。

### 5.5 理解申请人、审批人和历史

一条`Booking`同时关联两个`User`角色：

```text
user_id          → 提交申请的学生，必填
reviewed_by_id   → 处理申请的审批教师，处理前为空
```

所以模型必须使用`foreign_keys`明确每个关系采用哪一列，否则ORM无法判断同一个用户表的两条连接。

`Booking`保存当前状态，`BookingHistory`保存变化过程：

| 数据 | 回答的问题 |
| --- | --- |
| `Booking.status` | 这条预约现在是什么状态 |
| `Booking.review_comment` | 教师最后给出的审批意见是什么 |
| `BookingHistory.from_status` | 本次变化之前是什么状态 |
| `BookingHistory.to_status` | 本次变化之后是什么状态 |
| `BookingHistory.actor_id` | 谁执行了这次变化 |
| `BookingHistory.note` | 为什么变化或做了什么说明 |

只保存当前状态可以显示结果，但无法解释“何时、由谁、怎样变成这个结果”。

## 6. 第二个小终点：建立教师审批页面

### 6.1 从A10附录复制6个完整模板

| 文件 | 动作 | 作用 |
| --- | --- | --- |
| `templates/approvals.html` | 新建 | 按状态显示审批队列 |
| `templates/approval_detail.html` | 新建 | 显示申请信息并提交决定 |
| `templates/base.html` | 整体替换 | 为审批教师增加审批导航 |
| `templates/booking_detail.html` | 整体替换 | 学生可看审批人、意见和时间线 |
| `templates/dashboard.html` | 整体替换 | 教师看到待审批数量和队列入口 |
| `templates/index.html` | 整体替换 | 首页反映审批闭环进度 |

不要修改其他模板，它们从V0.4保持不变。

### 6.2 复制V0.5样式

用终点包中的`static/style.css`覆盖个人文件。V0.5样式为949行、约15 KB，新增状态页签、审批按钮和时间线。

### 6.3 启动并检查入口

双击`启动系统.bat`：

1. 学生账号应看到“我的预约”，看不到“预约审批”。
2. 审批教师应看到“预约审批”和工作台待审批数量。
3. 管理员仍只看到尚未开放的维护说明。

模板隐藏入口用于减少误操作，`@role_required("approver")`才是审批路由真正的权限边界。

## 7. 第三个小终点：执行一次完整跨角色流程

为避免V0.4旧记录缺少“创建历史”，本次验收使用升级到V0.5后新提交的两条预约。旧记录可以保留，不作为本次时间线样本。

### 7.1 学生提交两条申请

以`20260001`登录，在两个不同可用时段分别提交：

```text
申请A：数字媒体课程作品展示，20人，13800000001
申请B：网络课程小组实验，12人，13800000002
```

记录两个预约编号。两条都应为“待审批”，每条时间线都有“学生提交预约申请”。

### 7.2 教师先验证无效驳回

退出学生账号，以`T1001`登录：

1. 工作台待审批数量应增加2。
2. 进入审批队列，默认显示待审批申请。
3. 打开申请B。
4. 审批意见只填“无”，单击“驳回申请”。

预期返回400并提示至少填写3个字；申请仍为待审批，数据库没有新增驳回历史。

### 7.3 通过申请A

打开申请A，填写：

```text
信息完整，同意使用。
```

单击“通过申请”。预期：

- 当前状态变为已通过。
- 显示审批教师和意见。
- 时间线按页面显示顺序列出最新的已通过和之前的待审批。
- 审批表单消失，不能从页面再次处理。

### 7.4 合法驳回申请B

申请B填写：

```text
设备维护，请改选其他实验室。
```

单击驳回。状态变为已驳回，并保存原因和历史。

### 7.5 学生查看结果

退出教师账号，重新用`20260001`登录：

- “我的预约”中分别显示已通过和已驳回。
- 详情中能看到李老师和审批意见。
- 已通过申请仍可取消；已驳回申请没有取消按钮。

取消已通过的申请A后，时间线应出现三次变化：待审批、已通过、已取消；对应时段重新可预约。

## 8. 审批路由中的四道规则

打开A10附录`app.py`，找到`approval_decision`，按顺序指出：

1. **记录存在**：不存在的`booking_id`返回404。
2. **状态正确**：只有`PENDING`可以处理，其他状态返回400。
3. **决定合法**：只接受`approve`或`reject`。
4. **驳回有理由**：驳回意见少于3个字返回400，且不提交数据。

全部通过后，才同时更新当前状态、意见、审批人、时间，并新增历史记录，最后一次`commit()`保存为一个整体。

V0.5对通过意见尚未限制最大长度，也没有POST防伪令牌；V0.6会补齐这些质量规则。

## 9. 替换并执行V0.5自动测试

从A10附录复制完整284行`tests/test_app.py`，整体覆盖个人文件。

本版新增的核心测试证明：

- 新预约和取消都会产生正确历史。
- 教师能通过待审批申请。
- 驳回少于3字时状态仍为待审批。
- 学生不能打开审批队列。
- 已处理申请不能再次审批。

停止服务器并执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

预期：

```text
......................                                                   [100%]
22 passed
```

## 10. 手工验收V0.5

| 用例编号 | 操作 | 预期结果 | 我的结果 |
| --- | --- | --- | --- |
| MT-V05-01 | 学生提交两条不同预约 | 均为待审批，均有创建历史 |  |
| MT-V05-02 | 教师打开工作台和待审批队列 | 数量正确，只显示待审批申请 |  |
| MT-V05-03 | 驳回理由只填“无” | 返回400，状态和历史不改变 |  |
| MT-V05-04 | 教师通过申请A | 状态、审批人、意见、时间和历史正确 |  |
| MT-V05-05 | 对已通过申请再次提交决定 | 系统返回400，不改变已有结果 |  |
| MT-V05-06 | 教师用合法理由驳回申请B | 状态已驳回，原因和历史可见 |  |
| MT-V05-07 | 使用页签查看已通过、已驳回、全部 | 各列表内容与状态一致 |  |
| MT-V05-08 | 学生直接打开`/approvals` | 返回403 |  |
| MT-V05-09 | 学生查看两个审批结果 | 能看到审批教师和对应意见 |  |
| MT-V05-10 | 学生取消已通过申请A | 出现取消历史，原时段重新可预约 |  |

MT-V05-05的页面在审批后不再显示表单。可以使用浏览器“后退”到旧表单并再次提交，或以自动测试作为重复POST证据；无论入口怎样构造，服务端必须拒绝。

## 11. 常见问题与恢复

### 问题1：`no such column: bookings.review_comment`

说明旧数据库没有完成结构升级。确认`app.py`包含并调用`upgrade_database_schema()`，完全停止后重新启动。不要为了绕过错误删除模型字段。

### 问题2：出现`AmbiguousForeignKeysError`

`Booking`现在有申请人和审批人两条用户外键。确认A10版`User.bookings`、`Booking.user`和`Booking.reviewer`都明确配置了`foreign_keys`。

### 问题3：教师工作台数量为0，但学生已提交

确认学生查看的预约确实是`PENDING`；旧的已取消记录不计入待审批。再检查工作台查询条件是否为`Booking.status == "PENDING"`。

### 问题4：驳回失败后状态已经变化

校验必须发生在修改`booking.status`和`commit()`之前。整体恢复A10的`approval_decision`，不要只移动一行。

### 问题5：时间线没有创建记录

V0.5之前创建的旧预约不会自动补造历史。请在V0.5代码运行后新提交一条预约再观察。新建预约时必须`flush()`后添加`BookingHistory`。

### 问题6：已处理申请仍显示审批按钮

检查`approval_detail.html`是否用`booking.status == 'PENDING'`包围审批表单；即使页面有误，路由的状态检查仍必须阻止重复处理。

### 完整恢复方法

保留个人`.git`、`.venv`和历史标签，从`教学资源\版本终点核对包\dev-v0.5`覆盖全部21个终点文件。若旧数据库结构已处于不明状态，先改名备份再让系统重建。重新运行22项测试并用新预约完成跨角色验收。

## 12. 终点源码机械核对

V0.5终点包由`dev-v0.5`机械导出，共21个文件；A10收录所有完整代码。

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v0.5"
$courseFiles = @(
    ".gitignore",
    "VERSION",
    "app.py",
    "models.py",
    "requirements.txt",
    "static\style.css",
    "templates\approval_detail.html",
    "templates\approvals.html",
    "templates\base.html",
    "templates\booking_detail.html",
    "templates\dashboard.html",
    "templates\index.html",
    "templates\lab_detail.html",
    "templates\labs.html",
    "templates\login.html",
    "templates\my_bookings.html",
    "templates\reserve.html",
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

必须得到21行`PASS`。本地数据库仍不参与源码比较。

### 12.1 最终代码核对索引

| 终点内容 | 完整代码或准确来源 |
| --- | --- |
| 全部21个文件 | A10完整代码附录，逐文件完整代码块 |
| `VERSION`、`models.py`、`app.py` | 第5节按附录整体复制 |
| 6个新增或修改模板、CSS | 第6节按附录和终点包复制 |
| `tests/test_app.py` | 第9节按附录整体复制 |
| 其余10个文件 | 从`dev-v0.4`保持不变，由21文件比较验证 |

## 13. 提交并建立`dev-v0.5`标签

只有22项测试、10项手工验收和21文件核对全部通过后执行：

```powershell
git status --short
git diff --stat
git add VERSION app.py models.py static\style.css tests\test_app.py
git add templates\approval_detail.html templates\approvals.html
git add templates\base.html templates\booking_detail.html templates\dashboard.html templates\index.html
git commit -m "feat: add approval workflow for dev-v0.5"
git tag -a dev-v0.5 -m "Complete development version 0.5"
```

验证：

```powershell
git status --short
git log --oneline --decorate -6
git tag --list
git show dev-v0.5:VERSION
```

把提交号、22项测试、10项手工验收以及一条完整时间线填入记录册V0.5版本记录。

## 14. 本章练习

### 练习1：判断合法状态转换

判断以下变化是否合法并说明规则：`PENDING→APPROVED`、`PENDING→REJECTED`、`APPROVED→REJECTED`、`APPROVED→CANCELLED`。

本练习不修改源码，无需恢复。

### 练习2：比较当前状态和历史

对已通过后又取消的申请，分别指出`Booking.status`和三条`BookingHistory.to_status`回答的问题。

本练习不修改源码，无需恢复。

### 练习3：破坏重复审批保护

临时注释`approval_decision`中`booking.status != "PENDING"`的判断，运行测试并观察重复审批测试失败。

恢复方法：

```powershell
git restore app.py
.\.venv\Scripts\python.exe -m pytest -q
```

### 练习4：验证驳回原因边界

分别使用0字、1字、2字和3字原因驳回不同测试申请，说明V0.5在哪个长度开始接受。

本练习只生成课堂数据；需要统一恢复时备份并重建`instance/campus_lab.db`，不修改源码。

### 练习5：说明原子操作

解释为什么更新预约状态、审批人、审批时间和新增历史应在同一次数据库提交中完成。如果只保存状态而历史保存失败，会造成什么矛盾？

本练习不修改源码，无需恢复。

## 15. 两课时推进建议

### 第18课时：数据结构、迁移和审批页面

```text
0—7分钟：核对V0.4并画出跨角色流程
7—20分钟：替换模型与应用，执行语法检查
20—30分钟：运行旧数据库升级并检查新列、新表
30—37分钟：区分当前状态与历史，解释两条用户外键
37—45分钟：复制6个模板与CSS，检查角色入口
```

### 第19课时：跨角色验收、测试和冻结

```text
0—20分钟：学生提交两条，教师验证失败、通过和驳回
20—27分钟：学生查看结果，取消已通过申请并检查时间线
27—34分钟：替换并运行22项自动测试
34—39分钟：完成10项手工验收记录
39—42分钟：执行21文件机械核对
42—45分钟：提交并建立dev-v0.5标签
```

## 16. 本章完成检查

- [ ] 起点是18项测试通过且工作区干净的`dev-v0.4`。
- [ ] 旧数据库增加3个审批列和`booking_histories`表。
- [ ] 我能区分申请人和审批人两条用户关系。
- [ ] 新预约创建时写入待审批历史。
- [ ] 教师工作台和队列显示正确待审批数量。
- [ ] 驳回少于3字时返回400且数据不变。
- [ ] 通过和合法驳回都保存状态、审批人、时间、意见与历史。
- [ ] 已处理申请不能再次审批。
- [ ] 学生不能进入审批队列。
- [ ] 学生能查看审批结果和完整时间线。
- [ ] 已通过预约取消后增加取消历史并释放时段。
- [ ] 10项手工验收均通过。
- [ ] 自动测试显示`22 passed`。
- [ ] 机械核对显示21行`PASS`。
- [ ] Git工作区干净，最新提交有`dev-v0.5`标签。
- [ ] 个人记录册已填写V0.5提交号、测试结果和状态历史说明。
