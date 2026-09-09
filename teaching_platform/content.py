"""平台显示的 C0—C8 学生任务、向导内容与手工验收场景。"""

from __future__ import annotations


CHECKPOINT_ORDER = tuple(f"C{number}" for number in range(9))


TASKS = {
    "C0": {
        "title": "看懂项目起点 S0",
        "summary": "查看起点中的3个文件，判断它为什么还不是一个网站。",
        "knowledge": [
            "requirements.txt 记录项目依赖，.gitignore 说明哪些本机文件不进入版本库。",
            "初始化开发环境.bat 用来创建独立 Python 环境并安装依赖。",
            "没有 app.py 和页面文件时，项目还不能向浏览器提供网站。",
        ],
        "guide": {
            "goal": "本步只做一件事：找到 S0 的3个文件，判断它为什么还不能启动网站。",
            "outcome": "完成后，你能说清“开发环境准备好”为什么不等于“软件已经做出来”。",
            "prediction": {
                "question": "如果现在就尝试启动网站，最可能出现什么情况？",
                "hint": "先凭直觉选一个。这里不计对错，保存后平台才会告诉你要验证什么。",
                "options": [
                    {"id": "A", "text": "可以打开完整的实验室预约网站"},
                    {"id": "B", "text": "不能启动网站，因为还没有 Web 程序入口 app.py"},
                    {"id": "C", "text": "浏览器会自动根据 requirements.txt 生成网页"},
                ],
                "answer": "B",
                "feedback": "S0 只准备依赖和环境入口，没有 Web 程序入口，因此还不能启动网站。",
            },
            "apply": {
                "title": "S0 已由平台准备好",
                "description": "创建个人工作区时，平台已经复制3个起点文件并建立 Git 基线，不需要你再生成一次。",
                "button": "准备 S0 起点",
            },
            "experience": {
                "title": "亲手检查3个起点文件",
                "instruction": "按顺序完成下面3个动作。先看文件，再勾选“我已完成”；不要凭文字说明直接跳过。",
                "steps": [
                    "单击“打开文件观察器”，确认根目录中只有3个课程文件。",
                    "分别打开 requirements.txt、.gitignore 和 初始化开发环境.bat，看看它们写了什么。",
                    "在文件树中寻找 app.py，确认当前确实没有这个文件。",
                ],
                "confirm": "我已查看3个文件，并确认没有 app.py",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "three_files", "text": "根目录中能看到 requirements.txt、.gitignore、初始化开发环境.bat"},
                    {"id": "no_app", "text": "当前文件树中没有 app.py"},
                    {"id": "no_page", "text": "当前还没有可以打开的预约系统页面"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：为什么 S0 还不是一个网站？",
                "starter": "S0 已经准备了……，但还缺少……，所以……",
                "example": "例如：S0 已经准备了依赖安装方式，但还没有 Web 程序入口，所以浏览器得不到页面。请用自己的话作答。",
            },
        },
    },
    "C1": {
        "title": "建立项目目录",
        "summary": "建立 static、templates、tests 三个目录，理解目录和功能的区别。",
        "knowledge": [
            "static 保存 CSS 等静态资源，templates 保存 HTML 页面，tests 保存自动测试。",
            "目录结构帮助程序找到资源，也帮助开发者分清文件职责。",
            "建立空目录只是准备工作，不会自动产生网页功能。",
        ],
        "guide": {
            "goal": "本步只做一件事：建立3个职责明确的目录，并确认网站仍然不能启动。",
            "outcome": "完成后，你能指出页面、样式和测试以后分别放在哪里。",
            "prediction": {
                "question": "只创建 static、templates、tests 三个空目录后，网站会怎样？",
                "hint": "想一想：文件夹本身会执行程序吗？",
                "options": [
                    {"id": "A", "text": "网站会自动出现首页"},
                    {"id": "B", "text": "网站仍不能启动，但项目的文件职责更清楚了"},
                    {"id": "C", "text": "系统会自动生成数据库"},
                ],
                "answer": "B",
                "feedback": "目录只规定文件以后放在哪里；没有 app.py，仍然没有可执行的 Web 程序。",
            },
            "apply": {
                "title": "让平台生成 C1 项目结构",
                "description": "平台将准确创建 static、templates、tests 三个空目录，原有3个起点文件保持不变。",
                "button": "生成3个项目目录",
            },
            "experience": {
                "title": "亲手核对目录结构",
                "instruction": "打开文件观察器，把目录名称与它的职责对应起来。",
                "steps": [
                    "确认 static、templates、tests 都位于项目根目录。",
                    "确认3个目录当前都是空的。",
                    "再次确认根目录仍然没有 app.py。",
                ],
                "confirm": "我已找到3个目录，并确认网站仍不能启动",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "directories", "text": "static、templates、tests 三个目录都已出现"},
                    {"id": "empty", "text": "三个目录当前没有页面、样式或测试文件"},
                    {"id": "still_no_app", "text": "根目录仍没有 app.py，网站仍不能启动"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：为什么建立目录不等于完成功能？",
                "starter": "这些目录规定了……，但目录中还没有……，所以……",
                "example": "例如：目录规定了不同文件的存放位置，但没有程序和页面，所以用户还看不到功能。",
            },
        },
    },
    "C2": {
        "title": "运行第一个 Flask 页面",
        "summary": "加入最小 app.py，打通浏览器、路由和 Python 函数的最短链路。",
        "knowledge": [
            "Flask(__name__) 创建 Web 应用对象。",
            "@app.get('/') 把根网址与一个 Python 函数连接起来。",
            "浏览器发出 GET 请求，路由函数返回文字或页面响应。",
        ],
        "guide": {
            "goal": "本步只做一件事：运行第一个能被浏览器访问的 Flask 页面。",
            "outcome": "完成后，你能指出 app.py 中的应用对象、根路由和返回结果。",
            "prediction": {
                "question": "加入带有根路由的 app.py 后，打开网站根地址会看到什么？",
                "hint": "当前还没有让 app.py 使用 HTML 模板。",
                "options": [
                    {"id": "A", "text": "只看到一行系统名称和版本文字"},
                    {"id": "B", "text": "直接看到带导航和卡片的完整首页"},
                    {"id": "C", "text": "直接进入 MySQL 登录页面"},
                ],
                "answer": "A",
                "feedback": "最小路由直接返回一行文字，它证明请求链路已打通，但还没有完整界面。",
            },
            "apply": {
                "title": "让平台加入最小 Web 程序",
                "description": "平台将加入 VERSION 和临时 app.py；这是本课程第一次获得可运行的网站。",
                "button": "生成最小 Flask 应用",
            },
            "experience": {
                "title": "亲手启动并访问网站",
                "instruction": "代码由平台准确加入，但启动、打开、刷新和观察必须由你亲手完成。",
                "steps": [
                    "在文件观察器中打开 app.py，找到 Flask(__name__)、@app.get('/') 和 return。",
                    "单击“启动学生项目”，再单击出现的“打开学生项目”。",
                    "确认页面只显示一行“校园实验室预约系统 dev-v0.1”，然后返回本页。",
                ],
                "confirm": "我已打开 app.py，并在浏览器看到一行版本文字",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "app_exists", "text": "根目录中已经有 app.py 和 VERSION"},
                    {"id": "route_seen", "text": "app.py 中能找到根路由 @app.get('/')"},
                    {"id": "plain_text", "text": "浏览器页面只显示一行系统名称与版本文字"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：浏览器访问根地址后，为什么能看到这行文字？",
                "starter": "浏览器请求……，Flask 根据……找到……，然后返回……",
                "example": "例如：浏览器请求根地址，Flask 根据根路由找到 index 函数，再把函数返回的文字交给浏览器。",
            },
        },
    },
    "C3": {
        "title": "加入首页模板和样式",
        "summary": "加入 HTML 与 CSS 文件，观察“文件已经存在”和“程序已经使用”的差别。",
        "knowledge": [
            "base.html 复用公共页面骨架，index.html 填充本页内容。",
            "style.css 控制显示效果，不负责业务逻辑。",
            "模板只有被 render_template 调用后才会形成浏览器响应。",
        ],
        "guide": {
            "goal": "本步只做一件事：加入页面资源，并验证页面为什么暂时不变。",
            "outcome": "完成后，你能解释“文件存在”为什么不等于“程序正在使用它”。",
            "prediction": {
                "question": "只加入 base.html、index.html 和 style.css，不修改 app.py，刷新首页会怎样？",
                "hint": "观察 app.py 当前 return 的仍然是什么。",
                "options": [
                    {"id": "A", "text": "首页立刻变成完整样式"},
                    {"id": "B", "text": "首页仍是一行文字，因为路由还没有调用模板"},
                    {"id": "C", "text": "Flask 会拒绝启动"},
                ],
                "answer": "B",
                "feedback": "模板和 CSS 虽已存在，但 app.py 仍直接返回文字，所以页面保持不变正是正确结果。",
            },
            "apply": {
                "title": "让平台加入页面资源",
                "description": "平台将加入共享布局、首页模板和样式文件，但暂不修改 app.py。",
                "button": "加入 HTML 与 CSS 文件",
            },
            "experience": {
                "title": "亲手比较文件与运行结果",
                "instruction": "先看新文件，再刷新网站。重点是发现“页面没有变化”也是有意义的结果。",
                "steps": [
                    "在文件观察器中找到 templates/base.html、templates/index.html、static/style.css。",
                    "打开 app.py，确认根路由仍直接 return 一行文字。",
                    "启动或刷新学生项目，确认页面仍是一行文字。",
                ],
                "confirm": "我已查看3个新文件，并确认浏览器页面暂时不变",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "resources_exist", "text": "两个 HTML 文件和一个 CSS 文件都已出现"},
                    {"id": "app_unchanged", "text": "app.py 仍然直接返回文字，没有调用 render_template"},
                    {"id": "page_unchanged", "text": "刷新后页面仍是一行文字，而不是完整首页"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：为什么文件已经加入，页面却没有变化？",
                "starter": "虽然项目中已经有……，但是 app.py 仍然……，所以……",
                "example": "例如：虽然 HTML 已存在，但路由仍直接返回文字，没有加载模板，所以浏览器看不到新页面。",
            },
        },
    },
    "C4": {
        "title": "加入实验室列表模板",
        "summary": "查看 Jinja2 循环和判断，理解模板、数据、路由缺一不可。",
        "knowledge": [
            "Jinja2 循环把多条数据转换为重复页面结构。",
            "条件判断可根据实验室状态显示不同操作。",
            "模板不能自行成为网址，也不能自行获得业务数据。",
        ],
        "guide": {
            "goal": "本步只做一件事：读懂实验室列表模板，并验证它还不能单独成为页面。",
            "outcome": "完成后，你能说出一个动态页面需要模板、数据和路由共同配合。",
            "prediction": {
                "question": "只加入 labs.html 后，直接访问 /labs 会发生什么？",
                "hint": "想一想：当前 app.py 中是否已经定义 /labs 路由。",
                "options": [
                    {"id": "A", "text": "显示3间实验室"},
                    {"id": "B", "text": "不能得到列表页面，因为还没有 /labs 路由和数据"},
                    {"id": "C", "text": "自动创建实验室数据库"},
                ],
                "answer": "B",
                "feedback": "labs.html 只是页面模板；没有 /labs 路由把数据传给它，浏览器无法获得列表页面。",
            },
            "apply": {
                "title": "让平台加入列表模板",
                "description": "平台将只加入 templates/labs.html，刻意暂不加入路由和实验室数据。",
                "button": "加入实验室列表模板",
            },
            "experience": {
                "title": "亲手寻找模板需要的数据",
                "instruction": "打开模板看它需要什么，再到 app.py 中确认这些内容是否已经提供。",
                "steps": [
                    "打开 templates/labs.html，找到 for 循环和状态判断。",
                    "打开 app.py，确认当前没有 /labs 路由，也没有传入 labs 数据。",
                    "访问根页面确认仍是一行文字；也可访问 /labs 观察当前无法得到列表页面。",
                ],
                "confirm": "我已找到循环和判断，并确认当前没有 /labs 路由",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "labs_template", "text": "templates/labs.html 已出现，并包含对 labs 的循环"},
                    {"id": "no_labs_route", "text": "app.py 中还没有 /labs 路由和实验室数据"},
                    {"id": "no_list_page", "text": "当前还看不到可用的实验室列表页面"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：为什么一个模板文件不能独立成为动态页面？",
                "starter": "动态列表页面需要……提供网址、……提供数据、……负责显示；当前缺少……",
                "example": "例如：路由负责接收请求并传入数据，模板负责显示；当前缺少路由和数据，所以模板不能独立工作。",
            },
        },
    },
    "C5": {
        "title": "连接成完整 V0.1 页面",
        "summary": "用最终 app.py 连接路由、数据、模板和查询参数。",
        "knowledge": [
            "路由选择页面，render_template 把数据交给模板。",
            "LABS 是进程内示例数据，不是 SQLite 持久化数据。",
            "lab=2 是查询参数，用来预选表单中的实验室。",
        ],
        "guide": {
            "goal": "本步只做一件事：把已有文件连接起来，亲手走通3个正式页面。",
            "outcome": "完成后，你能沿着 URL→路由→数据→模板说清一个页面怎样产生。",
            "prediction": {
                "question": "最终 app.py 调用模板并提供 LABS 数据后，哪个结果符合 V0.1？",
                "hint": "V0.1 只做静态原型，预约提交尚未实现。",
                "options": [
                    {"id": "A", "text": "首页、实验室列表、预约表单可访问，但提交按钮禁用"},
                    {"id": "B", "text": "只能看到一行文字"},
                    {"id": "C", "text": "预约数据已经写入 SQLite"},
                ],
                "answer": "A",
                "feedback": "C5 形成3个可访问页面，并支持 lab=2 预选；V0.1 明确不保存表单数据。",
            },
            "apply": {
                "title": "让平台连接完整页面",
                "description": "平台将替换为最终 app.py，并加入预约表单模板，把前面准备的资源真正连接起来。",
                "button": "生成完整 V0.1 页面",
            },
            "experience": {
                "title": "亲手走通3个业务页面",
                "instruction": "必须实际点击导航和表单入口，不只看平台给出的说明。",
                "steps": [
                    "启动并打开学生项目，查看首页。",
                    "进入实验室列表，确认共3间实验室，其中2间可预约、1间维护中。",
                    "从人工智能实验室进入预约表单，确认下拉框预选正确；填写字段并观察提交按钮仍禁用。",
                ],
                "confirm": "我已走通3个页面，并确认表单当前不能提交",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "three_pages", "text": "首页、实验室列表、预约申请3个页面都能打开"},
                    {"id": "three_labs", "text": "列表显示3间实验室，其中2间可预约、1间维护中"},
                    {"id": "lab_selected", "text": "从人工智能实验室进入表单后，对应实验室已被预选"},
                    {"id": "submit_disabled", "text": "表单可以填写，但提交按钮处于禁用状态"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：一个实验室列表页面是怎样从网址产生的？",
                "starter": "浏览器访问……，Flask 路由……，把……交给……，最终……",
                "example": "例如：浏览器访问 /labs，路由把 LABS 数据交给 labs.html，模板循环生成3张实验室卡片。",
            },
        },
    },
    "C6": {
        "title": "使用运行与测试入口",
        "summary": "区分启动网站的入口、运行测试的入口和测试用例本身。",
        "knowledge": [
            "批处理脚本把固定目录检查和命令封装成可重复入口。",
            "启动入口运行应用，测试入口调用 pytest。",
            "安装了测试工具并不代表项目已经编写测试用例。",
        ],
        "guide": {
            "goal": "本步只做一件事：分别运行网站和 pytest，观察两个入口产生的不同结果。",
            "outcome": "完成后，你能分清测试工具、测试入口和测试用例。",
            "prediction": {
                "question": "已经安装 pytest、也加入运行测试脚本，但 tests 中还没有测试文件，此时会怎样？",
                "hint": "工具能够运行，不等于已经有内容可运行。",
                "options": [
                    {"id": "A", "text": "自动显示 6 passed"},
                    {"id": "B", "text": "pytest 能启动，但提示没有收集到测试用例"},
                    {"id": "C", "text": "网站因此无法打开"},
                ],
                "answer": "B",
                "feedback": "C6 只有测试入口，没有 tests/test_app.py；“没有测试用例”是本步要观察的正确结果。",
            },
            "apply": {
                "title": "让平台加入两个运行入口",
                "description": "平台将加入“启动系统.bat”和“运行测试.bat”，但暂不加入自动测试文件。",
                "button": "加入启动与测试脚本",
            },
            "experience": {
                "title": "亲手运行网站和空测试集",
                "instruction": "本步必须去测试页运行一次测试。看到“尚无测试用例”不是失败，而是观察目标。",
                "steps": [
                    "在文件观察器中比较两个 .bat 文件调用的命令。",
                    "启动学生项目，确认网站仍然正常。",
                    "进入测试页，单击“运行自动测试”，观察尚无测试用例的提示，再返回本页。",
                ],
                "confirm": "我已运行网站和 pytest，并看到“尚无测试用例”",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "two_scripts", "text": "项目中已经有启动系统和运行测试两个脚本"},
                    {"id": "site_ok", "text": "加入脚本后，原有网站仍能正常打开"},
                    {"id": "no_tests", "text": "pytest 可以运行，但提示当前没有测试用例"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：为什么 pytest 能运行却没有测试结果？",
                "starter": "项目已经有……，但 tests 中还没有……，所以 pytest……",
                "example": "例如：项目已有 pytest 工具和运行入口，但还没有测试文件，所以 pytest 能启动却收集不到用例。",
            },
        },
    },
    "C7": {
        "title": "完成手工与自动测试",
        "summary": "先写预期并亲手验收，再加入自动测试获得可重复证据。",
        "knowledge": [
            "测试的核心是比较预期结果与实际结果。",
            "手工测试适合验证用户操作和视觉结果，自动测试适合重复核对稳定规则。",
            "参数化可以让一个测试函数对多个网址分别形成测试用例。",
        ],
        "guide": {
            "goal": "本步只做一件事：先完成5项手工验收，再运行自动测试得到 6 passed。",
            "outcome": "完成后，你手中会同时有人工操作证据和可重复的自动测试证据。",
            "prediction": {
                "question": "为什么不能只看到“6 passed”就认为测试工作全部完成？",
                "hint": "想一想：自动程序是否真的像用户一样点击、阅读和判断界面。",
                "options": [
                    {"id": "A", "text": "因为自动测试不能替代所有用户操作和页面体验检查"},
                    {"id": "B", "text": "因为 6 是一个错误的测试数量"},
                    {"id": "C", "text": "因为手工测试不需要预期结果"},
                ],
                "answer": "A",
                "feedback": "手工验收与自动测试关注点不同。本步要求两类证据都具备，而不是相互替代。",
            },
            "apply": {
                "title": "先完成手工验收，再加入自动测试",
                "description": "请先到测试页完成5项手工用例。全部通过后，平台才允许加入 tests/test_app.py。",
                "button": "手工验收已完成，加入自动测试文件",
            },
            "experience": {
                "title": "亲手查看自动测试证据",
                "instruction": "测试文件加入后，必须亲自运行并读到 6 passed，同时打开文件找出一条断言。",
                "steps": [
                    "进入测试页运行自动测试，确认结果为 6 passed。",
                    "在文件观察器中打开 tests/test_app.py。",
                    "找到一条 assert，说明它在核对哪个页面结果。",
                ],
                "confirm": "我已看到 6 passed，并找到一条自动测试断言",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "manual_five", "text": "5项手工测试都记录了预期、实际结果和“通过”结论"},
                    {"id": "test_file", "text": "tests/test_app.py 已加入项目"},
                    {"id": "six_passed", "text": "最近一次自动测试明确显示 6 passed"},
                ],
            },
            "explanation": {
                "question": "任选一项测试，用一句话说明它的输入、操作、预期和失败含义。",
                "starter": "这项测试以……为输入，执行……，预期……；如果失败，说明……",
                "example": "例如：测试访问 /labs，预期返回200并包含实验室名称；失败说明列表页面或路由出现问题。",
            },
        },
    },
    "C8": {
        "title": "恢复故障并冻结 V0.1",
        "summary": "经历一次可恢复故障，用回归测试和 Git 证据确认里程碑。",
        "knowledge": [
            "先记录现象和判断，再恢复文件，才能形成可复用的诊断经验。",
            "恢复文件后必须重新运行回归测试，不能只看错误消失。",
            "Git 提交保存完整快照，标签给稳定里程碑一个固定名称。",
        ],
        "guide": {
            "goal": "本步只做一件事：完成一次故障发现—判断—恢复—回归测试，再冻结 dev-v0.1。",
            "outcome": "完成后，你会得到一个带提交、标签、测试和故障恢复记录的 V0.1 证据包。",
            "prediction": {
                "question": "如果首页路由仍在，但 templates/index.html 被移走，打开首页最可能看到什么？",
                "hint": "路由会继续尝试加载一个已经不存在的模板。",
                "options": [
                    {"id": "A", "text": "页面自动退回纯文字版本"},
                    {"id": "B", "text": "出现 TemplateNotFound，首页无法正常生成"},
                    {"id": "C", "text": "系统自动从 GitHub 下载模板"},
                ],
                "answer": "B",
                "feedback": "路由仍调用 index.html，文件缺失会触发 TemplateNotFound；恢复后还要重新测试所有功能。",
            },
            "apply": {
                "title": "进入 V0.1 发布前检查",
                "description": "C8 不新增业务功能。平台将固定终点文件状态，随后带你完成一次受控故障与回归。",
                "button": "进入故障恢复与发布阶段",
            },
            "experience": {
                "title": "亲手完成故障恢复闭环",
                "instruction": "按页面顺序操作：注入故障→阅读证据→写出判断→恢复→重新运行6项测试。",
                "steps": [
                    "单击“注入可恢复故障”，阅读 TemplateNotFound 证据。",
                    "根据证据填写一句故障判断，再由平台恢复准确模板。",
                    "进入测试页重新运行全部测试，确认这一次仍为 6 passed。",
                ],
                "confirm": "我已完成故障判断与恢复，并在恢复后重新得到 6 passed",
            },
            "observation": {
                "question": "请只勾选你刚才亲眼确认的结果",
                "items": [
                    {"id": "fault_seen", "text": "模板移走后，平台捕获到 TemplateNotFound 证据"},
                    {"id": "fault_recovered", "text": "写出判断后，templates/index.html 已恢复"},
                    {"id": "regression_passed", "text": "故障恢复后重新运行测试，结果为 6 passed"},
                    {"id": "thirteen_files", "text": "当前终点由13个受控项目文件组成"},
                ],
            },
            "explanation": {
                "question": "请用一句话说明：为什么恢复页面后还必须重新运行全部测试？",
                "starter": "恢复文件只能证明……，重新运行全部测试才能证明……，因此……",
                "example": "例如：错误消失只说明首页模板已回来，回归测试还要确认恢复操作没有破坏其他页面。",
            },
        },
    },
}


MANUAL_TEST_SCENARIOS = (
    {
        "id": "MT-V01-01",
        "title": "未登录打开首页",
        "suggested_action": "打开首页并观察系统名称、版本和业务说明。",
        "expected_example": "应显示系统名称、dev-v0.1 和本版功能说明。",
    },
    {
        "id": "MT-V01-02",
        "title": "打开实验室列表",
        "suggested_action": "打开实验室列表，统计实验室及其状态。",
        "expected_example": "应显示3间实验室，其中2间可预约、1间维护中。",
    },
    {
        "id": "MT-V01-03",
        "title": "从人工智能实验室进入预约表单",
        "suggested_action": "单击人工智能实验室的“填写预约信息”。",
        "expected_example": "应打开预约表单，并自动选中人工智能实验室。",
    },
    {
        "id": "MT-V01-04",
        "title": "填写表单并观察提交按钮",
        "suggested_action": "填写页面字段，尝试使用提交按钮。",
        "expected_example": "字段可以填写，但提交按钮应保持禁用，数据不会保存。",
    },
    {
        "id": "MT-V01-05",
        "title": "检查三个页面的导航",
        "suggested_action": "在首页、实验室和预约申请页分别使用导航。",
        "expected_example": "三个页面都应显示相同导航，并能在页面之间切换。",
    },
)
