# S09 从dev-v0.3到dev-v0.4：学生预约闭环

## 1. 本次开发的固定起点和终点

| 项目 | 内容 |
| --- | --- |
| 起点 | 已测试并提交的`dev-v0.3` |
| 终点 | `dev-v0.4`学生预约闭环 |
| 对应需求 | REQ-04、REQ-05；保持REQ-01—REQ-03 |
| 课时 | 第14—17课时，共180分钟 |
| 正式参考标签 | `dev-v0.4` |
| 教师参考提交 | `88db5f4` |
| 自动测试 | 18项全部通过 |

V0.3只能证明“学生身份已识别”，预约页面仍是不能提交的原型。V0.4要让一条业务数据真正走完一圈：

```text
学生查看实验室
→ 选择开放时段
→ 填写并提交预约
→ 服务器校验
→ SQLite保存待审批记录
→ 学生查看自己的预约
→ 学生取消预约
→ 时段重新可预约
```

本版不实现教师审批，也不保存状态变化历史；这两项属于V0.5。

## 2. 完整代码从哪里复制

从本版开始文件较多。为避免长代码在排版或转抄时被省略，本章配有：

- [A09 dev-v0.4完整代码附录](../完整代码附录/A09_dev-v0.4_完整代码.md)
- `教学资源\版本终点核对包\dev-v0.4`

附录包含终点全部19个文件的完整代码、字节数和SHA-256；核对包由冻结Git标签机械导出。每一步都明确要求复制哪个**完整文件**。正文中的关键片段只用于解释，不能代替完整文件。

学生操作方式：

1. 在附录中找到指定文件标题。
2. 复制该标题下代码块的全部内容。
3. 在个人项目中新建或打开同名文件。
4. `Ctrl+A`全选旧内容，粘贴并保存。
5. 立即执行本步检查，不一次性覆盖所有文件。

## 3. 开始前检查`dev-v0.3`

```powershell
git status --short
git describe --tags --exact-match HEAD
.\.venv\Scripts\python.exe -m pytest -q
```

必须得到：工作区干净、当前标签`dev-v0.3`、`14 passed`。

在记录册复制单版本模板并填写：

```text
版本名称：V0.4 学生预约闭环
起点版本或提交号：填写自己的dev-v0.3提交号
本版要解决的问题：学生只能看到不可提交的预约原型，业务数据没有形成闭环
本版验收标准：可选时段、合法提交、查看本人预约、取消、越权阻止、18项测试通过
```

## 4. 本版终点结构和真实差异

V0.4终点有19个受控文件：

```text
my-campus-lab/
├─ app.py                         修改：时段、预约、查询、取消路由
├─ models.py                      修改：TimeSlot与Booking模型及关系
├─ VERSION                        修改为dev-v0.4
├─ requirements.txt              不变
├─ static/style.css               修改：时段与预约页面样式
├─ templates/
│  ├─ base.html                   修改
│  ├─ booking_detail.html         新增
│  ├─ dashboard.html              修改
│  ├─ index.html                  修改
│  ├─ lab_detail.html             修改
│  ├─ labs.html                   修改
│  ├─ login.html                  不变
│  ├─ my_bookings.html            新增
│  └─ reserve.html                新增
├─ tests/test_app.py              修改
├─ .gitignore                     不变
├─ 初始化开发环境.bat              不变
├─ 启动系统.bat                    不变
└─ 运行测试.bat                    不变
```

V0.3的`templates/reservation_form.html`必须删除。它是“先选实验室再自己填写日期时间”的旧原型；V0.4改为从实验室详情选择数据库中的真实`TimeSlot`。

## 5. 第一个小终点：建立时段和预约数据模型

### 5.1 替换版本文件

把`VERSION`完整改为：

```text
dev-v0.4
```

### 5.2 整体替换`models.py`

从A09附录的`models.py`代码块复制完整138行，整体覆盖个人`models.py`。不要只追加`TimeSlot`和`Booking`，因为`User`、`Lab`中也增加了关系字段。

保存后执行语法检查：

```powershell
.\.venv\Scripts\python.exe -m py_compile models.py
```

没有输出表示语法正确。

### 5.3 检查数据库表

此时V0.3的`app.py`仍可启动。执行：

```powershell
.\.venv\Scripts\python.exe -c "from app import app; from models import db; from sqlalchemy import inspect; c=app.app_context(); c.push(); print(inspect(db.engine).get_table_names()); c.pop()"
```

预期至少出现：

```text
bookings
labs
time_slots
users
```

`db.create_all()`只补建新表，不删除V0.3已有的`labs`和`users`数据。

### 5.4 操作之后理解三个关系

```text
Lab 1 ── * TimeSlot
User 1 ── * Booking
TimeSlot 1 ── * Booking
```

- 一间实验室包含多个日期与时间段。
- 一名学生可以提交多条预约。
- 同一时段可以保留取消或驳回的历史预约，但只能有一条状态为`PENDING`或`APPROVED`的有效预约。
- `active_booking`从关联预约中寻找有效占用。
- `TimeSlot.is_available`同时检查时段开放、实验室可预约和无有效占用。
- `Booking.can_cancel`允许学生取消待审批或已通过预约，为下一版本审批后的取消预留规则。

本步可见结果是数据库结构已经出现，但尚无种子时段和预约页面。

## 6. 第二个小终点：生成时段并建立业务路由

### 6.1 整体替换`app.py`

从A09附录找到`app.py`，复制完整362行，整体覆盖个人`app.py`。该文件一次加入完整业务路由，后面四个操作阶段分别观察其中不同部分。

保存后先执行：

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py
```

### 6.2 暂时不要打开网页，先检查种子数据

V0.3模板仍引用已删除的旧路由名，页面文件尚未升级。先用数据库命令检查本步结果：

```powershell
.\.venv\Scripts\python.exe -c "from app import app; from models import User,TimeSlot,Booking,db; c=app.app_context(); c.push(); print('users=',db.session.query(User).count()); print('slots=',db.session.query(TimeSlot).count()); print('bookings=',db.session.query(Booking).count()); c.pop()"
```

新建或正常升级的教学数据库应显示：

```text
users= 4
slots= 16
bookings= 0
```

V0.4增加第二个学生账号：

```text
20260018 / 123456
```

它专门用于验证“学生不能查看其他学生预约”。

### 6.3 读懂种子时段

每间实验室生成4个时段，日期从数据库首次生成时的“明天”开始：

- 明天08:00—10:00。
- 明天10:10—12:10。
- 后天14:00—16:00。
- 第三天08:00—10:00。

4间实验室乘4个时段，共16条。维护中的实验室虽然有时段记录，但`TimeSlot.is_available`会把它们判断为不可预约。

### 6.4 读懂`reserve`路由的先后顺序

完整代码已经粘贴，下面只列阅读顺序，不要把它作为替代代码：

```text
1. 按slot_id查找TimeSlot，不存在则404
2. 检查时段、实验室和有效占用，不可用则400
3. GET时准备空表单
4. POST时读取purpose、attendee_count、contact
5. 检查用途至少5字、人数1到容量、联系方式至少6字符
6. 无错误才创建Booking并commit
7. 生成YY日期-8位随机字符的booking_no
8. 跳转到本人预约详情
```

V0.4的校验仍写在路由中，只完成最基本的长度和人数检查；V0.6将把它提取为独立函数并补充上限、多错误收集和表单防伪。

### 6.5 读懂三个个人预约路由

- `/my-bookings`只查询`Booking.user_id == g.user.id`。
- `/bookings/<booking_id>`先查记录，再检查申请人是不是当前用户。
- `/bookings/<booking_id>/cancel`再次检查本人和状态，更新为`CANCELLED`并提交。

“列表只查自己的数据”和“详情再次检查所有权”必须同时存在，不能因为列表中看不见别人数据就省略详情权限。

## 7. 第三个小终点：替换学生预约页面

### 7.1 从A09附录整体复制8个模板

逐个完成，每复制一个文件就确认路径：

| 文件 | 动作 | 页面作用 |
| --- | --- | --- |
| `templates/base.html` | 整体替换 | 导航改为“我的预约” |
| `templates/dashboard.html` | 整体替换 | 显示本人预约数量和入口 |
| `templates/index.html` | 整体替换 | 显示学生闭环状态 |
| `templates/labs.html` | 整体替换 | 入口改为“查看详情与时段” |
| `templates/lab_detail.html` | 整体替换 | 列出未来时段并按权限显示操作 |
| `templates/reserve.html` | 新建并完整粘贴 | 提交用途、人数和联系方式 |
| `templates/my_bookings.html` | 新建并完整粘贴 | 只列当前学生的预约 |
| `templates/booking_detail.html` | 新建并完整粘贴 | 显示详情、状态和取消操作 |

每个完整代码块都在[A09完整代码附录](../完整代码附录/A09_dev-v0.4_完整代码.md)中，没有省略号。

### 7.2 删除旧原型模板

确认当前目录为个人项目后执行：

```powershell
Remove-Item -LiteralPath .\templates\reservation_form.html
```

这是一个明确、可由Git恢复的单文件删除。误删其他文件时，可以从`dev-v0.3`恢复：

```powershell
git restore --source dev-v0.3 -- templates\文件名
```

不要恢复`reservation_form.html`到V0.4终点。

### 7.3 复制完整样式

用终点核对包中的：

```text
教学资源\版本终点核对包\dev-v0.4\static\style.css
```

覆盖个人`static\style.css`。终点为877行、约14 KB。

### 7.4 启动并确认页面链路

```powershell
.\.venv\Scripts\python.exe app.py
```

用`20260001`登录，依次执行：

```text
工作台
→ 查询实验室
→ 打开软件工程实验室详情
→ 查看开放时段
→ 单击一个“选择时段”
→ 看到真实预约表单
```

如果首页报`BuildError`并提到`reservation_form`，说明`base.html`仍是V0.3内容；不要修改路由名来迁就旧模板，应按A09替换模板。

## 8. 第四个小终点：提交、查看、取消并重新开放

### 8.1 先验证非法输入不保存

在预约表单填写：

```text
使用目的：测试
参加人数：20
联系方式：13800000001
```

“测试”少于5个字。提交后应显示“使用目的至少填写5个字”，仍停留在表单，输入内容被保留。

返回“我的预约”，记录数不应增加。

### 8.2 提交一条合法预约

重新填写：

```text
使用目的：数字媒体课程作品展示
参加人数：20
联系方式：13800000001
```

提交后应自动进入预约详情，并看到：

- 以`YY`和日期开头的预约编号。
- 状态“待审批”。
- 实验室、日期、时间、用途、人数和联系方式。
- “取消预约”按钮。

回到工作台，预约数量应从0变为1；“我的预约”中应出现同一条记录。

### 8.3 验证有效预约占用时段

再次打开原实验室详情。刚才选择的时段应显示“不可预约”，不能再次提交。

这里不能只依靠隐藏按钮。即使人工拼出原`/reserve/<slot_id>`网址，服务器也会通过`find_active_booking`返回400。

### 8.4 验证本人数据边界

1. 复制当前预约详情网址，例如`/bookings/1`。
2. 退出`20260001`。
3. 使用`20260018`和密码`123456`登录。
4. 直接访问刚才的网址。

预期返回403。第二名学生的“我的预约”仍为空。

### 8.5 取消并重新开放

重新以`20260001`登录，打开自己的预约，单击“取消预约”并确认。

预期：

- 预约状态变为“已取消”。
- 取消按钮消失。
- 再次打开实验室详情，原时段恢复“选择时段”。

V0.4只在`Booking`上保存当前状态和`cancelled_at`，尚未保存每次变化的历史；V0.5补齐。

## 9. 替换并执行V0.4自动测试

从A09附录复制完整`tests/test_app.py`，整体覆盖个人文件。终点测试文件为204行。

关键新增检查包括：

- 4名用户和16个时段正确生成。
- 预约表单包含三个业务字段。
- 合法预约被保存为`PENDING`且属于当前学生。
- 人数超过容量不会写入数据库。
- 学生能取消自己的预约。
- 第二名学生访问他人详情返回403。
- 审批教师访问学生预约页面返回403。

停止服务器后执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

正确结果：

```text
..................                                                       [100%]
18 passed
```

测试使用临时数据库，不受手工操作留下的预约影响。

## 10. 手工验收V0.4

浏览器自身会根据`min`和`max`先阻止超容量提交。执行MT-V04-05时，可在浏览器开发者工具中临时选中人数输入框，删除当前页面DOM中的`max`属性，再输入容量加1；这不会修改源码，用于证明服务器不能只依赖浏览器校验。

| 用例编号 | 操作 | 预期结果 | 我的结果 |
| --- | --- | --- | --- |
| MT-V04-01 | 打开可预约实验室详情 | 显示未来时段和可用状态 |  |
| MT-V04-02 | 未登录单击预约入口 | 先进入登录流程 |  |
| MT-V04-03 | 教师直接访问预约网址 | 返回403 |  |
| MT-V04-04 | 学生提交少于5字用途 | 显示错误且不新增预约 |  |
| MT-V04-05 | 临时移除页面`max`属性后提交容量加1 | 服务端仍拒绝且不新增预约 |  |
| MT-V04-06 | 学生合法提交 | 生成编号，状态为待审批，工作台数量增加 |  |
| MT-V04-07 | 再次访问已占用时段 | 页面不可选择，直接网址返回400 |  |
| MT-V04-08 | 第二名学生查看第一名学生详情 | 返回403，自己的列表仍为空 |  |
| MT-V04-09 | 第一名学生取消自己的预约 | 状态变已取消，取消按钮消失 |  |
| MT-V04-10 | 取消后回到实验室详情 | 原时段恢复可预约 |  |

把10项结果填入记录册第16节，并在V0.4版本记录中写出一次成功业务的数据变化。

## 11. 常见问题与恢复

### 问题1：`no such table: time_slots`或`bookings`

确认`models.py`是A09完整版本，并完全停止、重启应用。如果数据库处于不明中间状态，把`instance/campus_lab.db`改名备份，让应用重建统一种子数据。

### 问题2：用户数仍为3或没有第二个学生

检查`USER_SEED_DATA`是否有`20260018`，以及种子函数是否通过`existing_usernames`逐个补充缺失账号。

### 问题3：没有开放时段

先用第6.2节命令确认`slots`数量。若为0，检查`slot_count == 0`分支和`db.session.commit()`缩进；仍无法判断时备份并重建本地数据库。

### 问题4：提交后数据库没有记录

查看页面是否显示用途、人数或联系方式错误。只有`errors`为空才进入创建`Booking`的分支。不要删除校验来换取“提交成功”。

### 问题5：同一时段可以重复预约

检查路由开头是否调用`find_active_booking(slot.id)`，并确认状态集合为`PENDING`和`APPROVED`。

### 问题6：可以看到别人的预约

确认列表查询带`Booking.user_id == g.user.id`，详情和取消路由也分别检查`booking.user_id != g.user.id`并返回403。

### 问题7：测试成功，但手工页面数据混乱

自动测试使用临时数据库；手工页面使用`instance/campus_lab.db`。两者互不相同。记录需要保留时先备份；只需课堂统一状态时再重建手工数据库。

### 完整恢复方法

1. 记录当前错误和复现步骤。
2. 保留个人`.git`、`.venv`和V0.3标签。
3. 从`教学资源\版本终点核对包\dev-v0.4`覆盖19个终点文件。
4. 删除终点中不存在的`templates/reservation_form.html`。
5. 必要时把本地数据库改名，让程序重建。
6. 运行18项测试并重做10项手工验收。

## 12. 终点源码机械核对

V0.4终点包由`dev-v0.4`标签机械导出，共19个受控文件。完整内容也全部收录在A09附录。

在个人项目根目录执行，先修改第一行：

```powershell
$courseAnswerRoot = "D:\course-materials\campus-lab-development\教学资源\版本终点核对包\dev-v0.4"
$courseFiles = @(
    ".gitignore",
    "VERSION",
    "app.py",
    "models.py",
    "requirements.txt",
    "static\style.css",
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

必须得到19行`PASS`。另执行：

```powershell
Test-Path .\templates\reservation_form.html
```

必须返回`False`，否则个人目录仍有V0.3遗留文件。

### 12.1 最终代码核对索引

| 终点内容 | 完整代码或准确来源 |
| --- | --- |
| 全部19个文件 | A09完整代码附录，逐文件完整代码块 |
| 12个新增或修改的非CSS文件 | A09附录；按本章第5—9节分步复制 |
| `static/style.css` | V0.4终点核对包；A09也含完整877行 |
| 7个不变文件 | 从`dev-v0.3`保留，并由19文件比较验证 |
| 删除的旧模板 | `reservation_form.html`必须不存在 |

## 13. 提交并建立`dev-v0.4`标签

只有18项测试、10项手工验收和19文件核对全部通过后执行：

```powershell
git status --short
git diff --stat
git add VERSION app.py models.py static\style.css tests\test_app.py
git add -A -- templates
git status --short
git commit -m "feat: complete student booking flow for dev-v0.4"
git tag -a dev-v0.4 -m "Complete development version 0.4"
```

验证：

```powershell
git status --short
git log --oneline --decorate -5
git tag --list
git show dev-v0.4:VERSION
git ls-tree -r --name-only dev-v0.4
```

正确结果：工作区干净；最新提交带`dev-v0.4`标签；历史标签仍在；树中有`reserve.html`而没有`reservation_form.html`。

## 14. 本章练习

所有修改类练习都在V0.4提交之后进行，结束后恢复并重新运行18项测试。

### 练习1：观察输入边界

分别提交2字用途、0人、超过容量的人数和5位联系方式，记录系统提示及预约数量是否变化。

本练习不修改源码，无需恢复。

### 练习2：观察时段占用

第一名学生提交一个时段后，用第二名学生查看同一实验室。说明页面状态和服务端`find_active_booking`为什么都需要存在。

本练习只产生可取消的课堂预约；结束后由第一名学生取消即可恢复时段。

### 练习3：破坏所有权检查再由测试发现

临时注释`booking_detail`中的申请人检查，运行测试，找到哪一项失败。

恢复方法：

```powershell
git restore app.py
.\.venv\Scripts\python.exe -m pytest -q
```

### 练习4：画出状态变化

根据实际操作画出本版已经能够产生的`PENDING → CANCELLED`，并说明为什么页面同时列出`APPROVED`和`REJECTED`，但V0.4还不能产生这两个结果。

本练习不修改源码，无需恢复。

### 练习5：关闭V0.3界面缺陷

回看记录册中的`BUG-V03-01`。V0.4已经删除旧`reservation_form.html`并改用真实`reserve.html`，重复阶段卡片不再出现。填写“处理版本”和回归结果，关闭缺陷记录。

本练习只修改记录册，无需恢复。

## 15. 四课时推进建议

### 第14课时：数据模型与表关系

```text
0—8分钟：核对V0.3并说明学生闭环
8—25分钟：替换models.py，讲解TimeSlot和Booking
25—35分钟：创建新表并查看表名
35—45分钟：分析三个一对多关系和有效预约规则
```

### 第15课时：种子时段与业务路由

```text
0—15分钟：替换app.py并通过语法检查
15—23分钟：验证4名用户、16个时段、0条预约
23—35分钟：按顺序阅读reserve路由
35—45分钟：阅读本人列表、详情和取消的三重权限
```

### 第16课时：页面与完整业务操作

```text
0—18分钟：替换8个模板、删除旧模板、复制CSS
18—25分钟：从实验室详情进入真实时段表单
25—34分钟：验证非法输入与合法提交
34—40分钟：验证时段占用与本人数据边界
40—45分钟：取消并确认时段重新开放
```

### 第17课时：测试、核对和冻结

```text
0—12分钟：替换并运行18项自动测试
12—27分钟：完成10项手工验收
27—34分钟：记录数据变化和测试结果
34—40分钟：执行19文件机械核对及旧文件检查
40—45分钟：提交并建立dev-v0.4标签
```

## 16. 本章完成检查

- [ ] 起点是14项测试通过且工作区干净的`dev-v0.3`。
- [ ] 数据库有4名用户、16个时段，初始预约为0。
- [ ] 我能解释Lab、TimeSlot、User和Booking的关系。
- [ ] 可用时段同时检查时段、实验室和有效预约。
- [ ] 学生可以从实验室详情选择真实时段。
- [ ] 不合法用途、人数或联系方式不会保存预约。
- [ ] 合法提交生成编号和`PENDING`状态。
- [ ] “我的预约”只显示当前学生数据。
- [ ] 第二名学生访问他人详情得到403。
- [ ] 待审批预约占用时段，取消后时段重新开放。
- [ ] 我知道V0.4尚无教师审批和状态历史。
- [ ] 10项手工验收均通过。
- [ ] 自动测试显示`18 passed`。
- [ ] 机械核对显示19行`PASS`，旧模板检查为`False`。
- [ ] Git工作区干净，`dev-v0.1`—`dev-v0.4`标签均存在。
- [ ] 个人记录册已填写V0.4提交号、测试结果、数据变化和缺陷回归。
