# dev-v1.0 完整代码核对附录

> 本附录由冻结版本终点包机械生成，不是手工重新整理的代码。文件内容只统一为LF换行；原始字节数与SHA-256用于核对终点资源。

## 1. 文件清单

| 路径 | 原始字节数 | 代码行数 | 原始文件SHA-256 |
| --- | ---: | ---: | --- |
| `.gitignore` | 62 | 6 | `bb1173460471204c4b38c69ac9b1fe238efe3a175a029a3977a659bff182d955` |
| `README.md` | 1100 | 29 | `7b1f550f2d4e5dc8d725df62e5b79006d9dd250cafa1163fcc558d21cf9fc346` |
| `VERSION` | 10 | 1 | `3d20990274d541e37de57959a15324bacf8d87f884787d27157509347b3f1fd3` |
| `app.py` | 19616 | 549 | `73e5395bd7a4fbd632ec4002d69749a750c010468875d0061105eab30c8d2082` |
| `models.py` | 6463 | 179 | `2ae9bb8171924b4ac7afe16e95807a3d95973ca6ecaa95c71bbda86e3d38ddc1` |
| `pytest.ini` | 44 | 3 | `aa4bde9d537aff058b95c3beab92bdd6f2547ffbdac1a95bb29f8cf2921fba37` |
| `requirements.txt` | 54 | 3 | `1f2fb163b1f8c0cae49cf5a4a8279685080d4c3126ae0e77527fa2ce231766f3` |
| `static/favicon.svg` | 175 | 4 | `d00de2c785c4ee6e21301d31333cd6c2fb0a417f41fb6f05dd65d28133b8f752` |
| `static/style.css` | 16963 | 1043 | `3c5a649da700cf3bfa397c89d89d5a5e716a2ba4565692f6946a057ea87f685f` |
| `templates/admin_labs.html` | 1595 | 39 | `7f6fa7880a9932a872dd6d61597a317df7419d3b2f69cbd10e8a237329f0f9ea` |
| `templates/approval_detail.html` | 3180 | 64 | `e5d7b0f701f70e44b20564421827387b3e5238dfd1e386dbdfebb1433e37b70e` |
| `templates/approvals.html` | 2247 | 43 | `35d470bffdf5d85226f4318e0d8efd0dd931ac4f3a47196e1fbc060a1e9361c6` |
| `templates/base.html` | 3508 | 72 | `23e7c4e68ae03bca749cbbb2747848a14c681786f6aaad1a8a16b5c814920bc5` |
| `templates/booking_detail.html` | 3059 | 58 | `b3e3008faa396b67af683e49d7d338ff4a0b20c309b2b6275502ee2581d32a9a` |
| `templates/dashboard.html` | 2369 | 52 | `9c583c774ff937b29cc3ba99044ae77286fb6920a8d7287934a3ac464ab94f9e` |
| `templates/errors/400.html` | 536 | 14 | `a629a413545b74a90486fdf7dd5eaae2acaf6ea30083339deeaea96e1c793fdf` |
| `templates/errors/403.html` | 543 | 14 | `06f5144cdc98493f3f9b38b46d735eb65ad5dafc03320a1c4f061ffeac846670` |
| `templates/errors/404.html` | 490 | 14 | `b25f5089b0255c1b8fc4316adb15072bd53da9f9401a313b63739eb599e02c2a` |
| `templates/index.html` | 3032 | 66 | `456d0e1de6acde7cb39dad62055be8aa7871690da2d46e59917a79c3efdb56f8` |
| `templates/lab_detail.html` | 2607 | 59 | `3c821ec3df6b87b98339eab0cb23308f5cca75655899b3e8f0f934fda5f84b74` |
| `templates/labs.html` | 2989 | 71 | `c4a1825e54699474e6598b5f36deae7db8ac8a765f02dc979c9629a5429557d9` |
| `templates/login.html` | 1676 | 34 | `c809aa81522c84b34f39f942607c28858db087ae061d0d32b2c08984421dab64` |
| `templates/my_bookings.html` | 1685 | 42 | `9df3f4e6aa7ac1fed874de65fdaf28d49cca7a010171cbdd92145157c66be2e8` |
| `templates/reserve.html` | 2330 | 45 | `1d2afb9d6e2931a8497f392b82fadc4cbf40b7662cc1d7965297c60b51438a1a` |
| `templates/version.html` | 1387 | 36 | `5b075d1351fd8bc4b0fc55dd4cac760b59016f3d280a392254114a059f38cf9e` |
| `tests/conftest.py` | 411 | 20 | `5dcf769de597031247ecb5f313d99a4eb59d1c9e0712c0c95b1ab58b52f19789` |
| `tests/test_acceptance.py` | 2897 | 92 | `56a5cbbf536d1474f9741be1e42813985a916109faa8f04f28834daa1e63b884` |
| `tests/test_app.py` | 12157 | 369 | `da0169dfeb9f81c28b11d9c6baf095698dc7b9f8d978d96ff0ae9c1b95d60a70` |
| `tests/test_validators.py` | 1333 | 46 | `88990ad8d87a940e48e9ae426ff9c480a39b4d98747859d3dde17904318bf0b3` |
| `validators.py` | 1499 | 40 | `19fb2fbe61938a622e67295e3aa60f50bb0c26c82002962fbc129b8c16d9549e` |
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

### `README.md`

```markdown
# 校园实验室预约与审批系统（开发教学版）

这是“软件项目开发”课程的贯穿案例。项目采用 Flask、Jinja2、Flask-SQLAlchemy 和 SQLite，学生可以在一台普通笔记本上完成从页面到数据库的完整开发过程。

## 本机运行

1. 双击 `初始化开发环境.bat`，只在项目目录创建独立的 `.venv`。
2. 双击 `启动系统.bat`。
3. 浏览器访问 `http://127.0.0.1:5000`。

演示账号统一密码为 `123456`：

- 学生：`20260001`
- 审批教师：`T1001`
- 实验室管理员：`A001`

## 七个代码基线

| 标签 | 开发结果 |
| --- | --- |
| `dev-v0.1` | Flask网站骨架与静态原型 |
| `dev-v0.2` | SQLite数据库与实验室查询 |
| `dev-v0.3` | 用户登录与角色权限 |
| `dev-v0.4` | 学生预约完整闭环 |
| `dev-v0.5` | 教师审批完整流程 |
| `dev-v0.6` | 校验、安全、错误处理与自动测试 |
| `dev-v1.0` | 三角色集成、验收与发布 |

运行测试：双击 `运行测试.bat`，或执行 `.venv\Scripts\python.exe -m pytest -q`。
```

### `VERSION`

```text
dev-v1.0
```

### `app.py`

```python
from pathlib import Path
from functools import wraps
from datetime import date, datetime, time, timedelta
from hmac import compare_digest
import os
from secrets import token_urlsafe
from uuid import uuid4

from flask import Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import func, inspect, or_, select, text

from models import Booking, BookingHistory, Lab, TimeSlot, User, db
from validators import validate_approval_form, validate_booking_form


VERSION = "dev-v1.0"

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
        "username": "20260018",
        "display_name": "林悦",
        "department": "视觉传达专业",
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
        labs = [Lab(**data) for data in LAB_SEED_DATA]
        db.session.add_all(labs)
        db.session.flush()
    else:
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()

    existing_usernames = set(db.session.scalars(select(User.username)).all())
    users_added = False
    for data in USER_SEED_DATA:
        if data["username"] not in existing_usernames:
            user = User(**data)
            user.set_password("123456")
            db.session.add(user)
            users_added = True

    slot_count = db.session.scalar(select(func.count()).select_from(TimeSlot))
    if slot_count == 0:
        tomorrow = date.today() + timedelta(days=1)
        slot_specs = [
            (tomorrow, time(8, 0), time(10, 0)),
            (tomorrow, time(10, 10), time(12, 10)),
            (tomorrow + timedelta(days=1), time(14, 0), time(16, 0)),
            (tomorrow + timedelta(days=2), time(8, 0), time(10, 0)),
        ]
        for lab in labs:
            for booking_date, start_time, end_time in slot_specs:
                db.session.add(
                    TimeSlot(
                        lab=lab,
                        booking_date=booking_date,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )

    if lab_count == 0 or users_added or slot_count == 0:
        db.session.commit()


def find_active_booking(slot_id):
    return db.session.scalar(
        select(Booking).where(
            Booking.time_slot_id == slot_id,
            Booking.status.in_(["PENDING", "APPROVED"]),
        )
    )


def upgrade_database_schema():
    """让从dev-v0.4升级的本地SQLite数据库补齐审批字段。"""
    inspector = inspect(db.engine)
    if "bookings" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("bookings")}
    additions = {
        "review_comment": "VARCHAR(300)",
        "reviewed_by_id": "INTEGER",
        "reviewed_at": "DATETIME",
    }
    missing = [(name, data_type) for name, data_type in additions.items() if name not in columns]
    if missing:
        with db.engine.begin() as connection:
            for name, data_type in missing:
                connection.execute(text(f"ALTER TABLE bookings ADD COLUMN {name} {data_type}"))


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
                abort(403, description="当前账号没有访问这个功能的权限。")
            return view(**kwargs)

        return wrapped_view

    return decorator


def csrf_token():
    """为当前浏览器会话生成一个表单防伪令牌。"""
    if "_csrf_token" not in session:
        session["_csrf_token"] = token_urlsafe(24)
    return session["_csrf_token"]


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__, instance_relative_config=True)
    database_path = Path(app.instance_path) / "campus_lab.db"
    app.config.from_mapping(
        TESTING=False,
        SECRET_KEY=os.environ.get("CAMPUS_LAB_SECRET_KEY", "classroom-demo-secret-key"),
        MAX_CONTENT_LENGTH=1024 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "CAMPUS_LAB_DATABASE_URL",
            f"sqlite:///{database_path.as_posix()}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        upgrade_database_schema()
        seed_database()

    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.user = db.session.get(User, user_id) if user_id else None

    @app.before_request
    def protect_post_requests():
        if request.method == "POST":
            expected = session.get("_csrf_token", "")
            submitted = request.form.get("_csrf_token", "")
            if not expected or not compare_digest(expected, submitted):
                abort(400, description="表单已过期或来源无效，请返回页面后重新操作。")

    @app.context_processor
    def inject_version():
        return {"app_version": VERSION, "csrf_token": csrf_token}

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
        my_booking_count = 0
        pending_count = 0
        lab_count = 0
        available_lab_count = 0
        if g.user.role == "student":
            my_booking_count = db.session.scalar(
                select(func.count()).select_from(Booking).where(Booking.user_id == g.user.id)
            )
        elif g.user.role == "approver":
            pending_count = db.session.scalar(
                select(func.count()).select_from(Booking).where(Booking.status == "PENDING")
            )
        elif g.user.role == "admin":
            lab_count = db.session.scalar(select(func.count()).select_from(Lab))
            available_lab_count = db.session.scalar(
                select(func.count()).select_from(Lab).where(Lab.status == "可预约")
            )
        return render_template(
            "dashboard.html",
            my_booking_count=my_booking_count,
            pending_count=pending_count,
            lab_count=lab_count,
            available_lab_count=available_lab_count,
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
        future_slots = db.session.scalars(
            select(TimeSlot)
            .where(TimeSlot.lab_id == lab.id, TimeSlot.booking_date >= date.today())
            .order_by(TimeSlot.booking_date, TimeSlot.start_time)
        ).all()
        return render_template("lab_detail.html", lab=lab, time_slots=future_slots)

    @app.route("/reserve/<int:slot_id>", methods=["GET", "POST"])
    @role_required("student")
    def reserve(slot_id):
        slot = db.session.get(TimeSlot, slot_id)
        if slot is None:
            abort(404)
        if not slot.is_open or not slot.lab.is_available or find_active_booking(slot.id):
            abort(400, description="该时段当前不可预约，请返回实验室详情重新选择。")

        form_data, errors = validate_booking_form(request.form, slot.lab.capacity)
        if request.method == "POST":
            if not errors:
                booking = Booking(
                    booking_no=f"YY{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}",
                    user=g.user,
                    time_slot=slot,
                    purpose=form_data["purpose"],
                    attendee_count=form_data["attendee_count_value"],
                    contact=form_data["contact"],
                )
                db.session.add(booking)
                db.session.flush()
                db.session.add(
                    BookingHistory(
                        booking=booking,
                        actor=g.user,
                        from_status=None,
                        to_status="PENDING",
                        note="学生提交预约申请。",
                    )
                )
                db.session.commit()
                flash(f"预约{booking.booking_no}已提交，等待教师审批。", "success")
                return redirect(url_for("booking_detail", booking_id=booking.id))

            for error in errors:
                flash(error, "error")

        return render_template("reserve.html", slot=slot, form_data=form_data)

    @app.get("/my-bookings")
    @role_required("student")
    def my_bookings():
        bookings = db.session.scalars(
            select(Booking)
            .where(Booking.user_id == g.user.id)
            .order_by(Booking.created_at.desc())
        ).all()
        return render_template("my_bookings.html", bookings=bookings)

    @app.get("/bookings/<int:booking_id>")
    @role_required("student")
    def booking_detail(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404)
        if booking.user_id != g.user.id:
            abort(403, description="只能查看自己提交的预约。")
        return render_template("booking_detail.html", booking=booking)

    @app.post("/bookings/<int:booking_id>/cancel")
    @role_required("student")
    def cancel_booking(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404)
        if booking.user_id != g.user.id:
            abort(403, description="只能取消自己提交的预约。")
        if not booking.can_cancel:
            abort(400, description="当前状态的预约不能取消。")

        booking.status = "CANCELLED"
        booking.cancelled_at = datetime.now()
        db.session.add(
            BookingHistory(
                booking=booking,
                actor=g.user,
                from_status="PENDING" if booking.reviewed_at is None else "APPROVED",
                to_status="CANCELLED",
                note="学生取消预约。",
            )
        )
        db.session.commit()
        flash(f"预约{booking.booking_no}已取消。", "success")
        return redirect(url_for("booking_detail", booking_id=booking.id))

    @app.get("/approvals")
    @role_required("approver")
    def approvals():
        status = request.args.get("status", "PENDING")
        allowed_statuses = {"PENDING", "APPROVED", "REJECTED", "CANCELLED", "ALL"}
        if status not in allowed_statuses:
            status = "PENDING"

        statement = select(Booking).order_by(Booking.created_at.desc())
        if status != "ALL":
            statement = statement.where(Booking.status == status)
        bookings = db.session.scalars(statement).all()
        return render_template("approvals.html", bookings=bookings, selected_status=status)

    @app.get("/approvals/<int:booking_id>")
    @role_required("approver")
    def approval_detail(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404)
        return render_template("approval_detail.html", booking=booking)

    @app.post("/approvals/<int:booking_id>/decision")
    @role_required("approver")
    def approval_decision(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404)
        if booking.status != "PENDING":
            abort(400, description="这条申请已经处理，不能重复审批。")

        decision, comment, errors = validate_approval_form(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("approval_detail.html", booking=booking), 400

        new_status = "APPROVED" if decision == "approve" else "REJECTED"
        booking.status = new_status
        booking.review_comment = comment or "审批通过。"
        booking.reviewer = g.user
        booking.reviewed_at = datetime.now()
        db.session.add(
            BookingHistory(
                booking=booking,
                actor=g.user,
                from_status="PENDING",
                to_status=new_status,
                note=booking.review_comment,
            )
        )
        db.session.commit()

        flash(f"预约{booking.booking_no}已{booking.status_label}。", "success")
        return redirect(url_for("approval_detail", booking_id=booking.id))

    @app.get("/admin/labs")
    @role_required("admin")
    def admin_labs():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()
        return render_template("admin_labs.html", labs=labs)

    @app.post("/admin/labs/<int:lab_id>/toggle")
    @role_required("admin")
    def toggle_lab(lab_id):
        lab = db.session.get(Lab, lab_id)
        if lab is None:
            abort(404)

        if lab.is_available:
            active_booking = db.session.scalar(
                select(Booking)
                .join(TimeSlot)
                .where(
                    TimeSlot.lab_id == lab.id,
                    Booking.status.in_(["PENDING", "APPROVED"]),
                )
            )
            if active_booking:
                abort(
                    400,
                    description="该实验室仍有待审批或已通过的预约，不能直接停用。",
                )
            lab.status = "维护中"
            message = f"{lab.name}已设为维护中。"
        else:
            lab.status = "可预约"
            message = f"{lab.name}已恢复开放。"

        db.session.commit()
        flash(message, "success")
        return redirect(url_for("admin_labs"))

    @app.get("/version")
    def version_info():
        counts = {
            "labs": db.session.scalar(select(func.count()).select_from(Lab)),
            "users": db.session.scalar(select(func.count()).select_from(User)),
            "bookings": db.session.scalar(select(func.count()).select_from(Booking)),
        }
        return render_template("version.html", counts=counts)

    @app.get("/health")
    def health():
        db.session.scalar(select(func.count()).select_from(Lab))
        return jsonify(status="ok", version=VERSION, database="ok")

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("errors/400.html", error=error), 400

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html", error=error), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("CAMPUS_LAB_PORT", "5000")),
        debug=False,
    )
```

### `models.py`

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


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

    bookings = db.relationship(
        "Booking",
        back_populates="user",
        foreign_keys="Booking.user_id",
        lazy="select",
    )

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

    time_slots = db.relationship(
        "TimeSlot",
        back_populates="lab",
        cascade="all, delete-orphan",
        order_by="TimeSlot.booking_date, TimeSlot.start_time",
    )

    @property
    def is_available(self):
        return self.status == "可预约"


class TimeSlot(db.Model):
    """实验室开放的一个具体日期和时间段。"""

    __tablename__ = "time_slots"

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"), index=True, nullable=False)
    booking_date = db.Column(db.Date, index=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=True)

    lab = db.relationship("Lab", back_populates="time_slots")
    bookings = db.relationship("Booking", back_populates="time_slot", lazy="select")

    @property
    def date_label(self):
        weekdays = "一二三四五六日"
        return f"{self.booking_date:%Y-%m-%d} 周{weekdays[self.booking_date.weekday()]}"

    @property
    def time_label(self):
        return f"{self.start_time:%H:%M}—{self.end_time:%H:%M}"

    @property
    def active_booking(self):
        return next(
            (booking for booking in self.bookings if booking.status in {"PENDING", "APPROVED"}),
            None,
        )

    @property
    def is_available(self):
        return self.is_open and self.lab.is_available and self.active_booking is None


class Booking(db.Model):
    """学生提交的一次实验室预约申请。"""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    booking_no = db.Column(db.String(40), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey("time_slots.id"), index=True, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    attendee_count = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), index=True, nullable=False, default="PENDING")
    review_comment = db.Column(db.String(300))
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cancelled_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="bookings", foreign_keys=[user_id])
    reviewer = db.relationship("User", foreign_keys=[reviewed_by_id])
    time_slot = db.relationship("TimeSlot", back_populates="bookings")
    histories = db.relationship(
        "BookingHistory",
        back_populates="booking",
        cascade="all, delete-orphan",
        order_by="BookingHistory.created_at.desc()",
    )

    @property
    def status_label(self):
        return {
            "PENDING": "待审批",
            "APPROVED": "已通过",
            "REJECTED": "已驳回",
            "CANCELLED": "已取消",
        }.get(self.status, self.status)

    @property
    def status_class(self):
        return {
            "PENDING": "warning",
            "APPROVED": "success",
            "REJECTED": "danger",
            "CANCELLED": "secondary",
        }.get(self.status, "secondary")

    @property
    def can_cancel(self):
        return self.status in {"PENDING", "APPROVED"}


class BookingHistory(db.Model):
    """保存预约状态的每一次变化，便于追踪审批过程。"""

    __tablename__ = "booking_histories"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), index=True, nullable=False)
    from_status = db.Column(db.String(20))
    to_status = db.Column(db.String(20), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    note = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    booking = db.relationship("Booking", back_populates="histories")
    actor = db.relationship("User", foreign_keys=[actor_id])

    @property
    def to_status_label(self):
        return {
            "PENDING": "待审批",
            "APPROVED": "已通过",
            "REJECTED": "已驳回",
            "CANCELLED": "已取消",
        }.get(self.to_status, self.to_status)
```

### `pytest.ini`

```text
[pytest]
testpaths = tests
addopts = -ra
```

### `requirements.txt`

```text
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
pytest==9.1.1
```

### `static/favicon.svg`

```text
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="16" fill="#2563eb"/>
  <path d="M20 15h9v27h17v8H20z" fill="#fff"/>
</svg>
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

.button.danger {
    color: #ffffff;
    background: #b42318;
}

.button.danger:hover {
    background: #912018;
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

.status.success {
    color: #067647;
    background: #dcfae6;
}

.status.warning {
    color: #93370d;
    background: #fef0c7;
}

.status.danger {
    color: #b42318;
    background: #fee4e2;
}

.status.secondary {
    color: #475467;
    background: #eaecf0;
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

.subheading {
    margin: 30px 0 12px;
    font-size: 18px;
}

.slot-list {
    border-top: 1px solid var(--line);
}

.slot-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding: 15px 0;
    border-bottom: 1px solid var(--line);
}

.slot-row > div {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.slot-row span {
    color: var(--muted);
    font-size: 14px;
}

.list-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.booking-list {
    display: grid;
    gap: 14px;
}

.booking-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 22px;
    padding: 22px 24px;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: #ffffff;
    box-shadow: var(--shadow-sm);
}

.booking-row h2 {
    margin: 5px 0 7px;
    color: var(--navy);
    font-size: 19px;
}

.booking-row p {
    margin: 0;
    color: var(--muted);
}

.booking-no {
    color: var(--blue-dark);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.04em;
}

.booking-actions {
    display: flex;
    align-items: flex-end;
    flex-direction: column;
    gap: 10px;
    flex-shrink: 0;
}

.status-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 18px;
}

.status-tabs a {
    padding: 9px 15px;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--muted);
    background: #ffffff;
    text-decoration: none;
}

.status-tabs a.active {
    border-color: var(--blue);
    color: #ffffff;
    background: var(--blue);
}

.decision-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.timeline {
    margin-top: 26px;
    padding-top: 6px;
    border-top: 1px solid var(--line);
}

.timeline-item {
    position: relative;
    padding: 16px 0 0 18px;
    border-left: 2px solid #d0d5dd;
}

.timeline-item::before {
    position: absolute;
    top: 21px;
    left: -6px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--blue);
    content: "";
}

.timeline-item strong,
.timeline-item span {
    display: block;
}

.timeline-item span {
    margin-top: 3px;
    color: var(--muted);
    font-size: 12px;
}

.timeline-item p {
    margin: 5px 0 0;
    color: var(--muted);
    font-size: 14px;
}

.error-page {
    display: flex;
    min-height: 520px;
    align-items: center;
    padding: 60px 0;
}

.error-card {
    max-width: 660px;
    padding: 54px;
    border: 1px solid var(--line);
    border-radius: 20px;
    background: #ffffff;
    box-shadow: var(--shadow);
    text-align: center;
}

.error-code {
    color: var(--blue);
    font-size: 64px;
    font-weight: 900;
    letter-spacing: -0.05em;
}

.error-card h1 {
    margin: 6px 0 10px;
    color: var(--navy);
}

.error-card p {
    margin: 0 0 26px;
    color: var(--muted);
}

.version-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 24px 0;
}

.metric-grid div {
    padding: 18px 12px;
    border-radius: 12px;
    background: #f5f8ff;
    text-align: center;
}

.metric-grid strong,
.metric-grid span {
    display: block;
}

.metric-grid strong {
    color: var(--blue-dark);
    font-size: 28px;
}

.metric-grid span {
    color: var(--muted);
    font-size: 13px;
}

.architecture-list {
    display: grid;
    gap: 14px;
    margin: 24px 0 0;
    padding-left: 24px;
    color: var(--muted);
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

.site-footer a {
    color: #b9c8d8;
    text-decoration: none;
}

.site-footer a:hover {
    color: #ffffff;
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

    .version-grid {
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

    .booking-row,
    .list-toolbar,
    .slot-row {
        align-items: stretch;
        flex-direction: column;
    }

    .decision-actions {
        grid-template-columns: 1fr;
    }

    .metric-grid {
        grid-template-columns: 1fr;
    }

    .booking-actions {
        align-items: flex-start;
    }
}
```

### `templates/admin_labs.html`

```html
{% extends "base.html" %}

{% block title %}实验室管理｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">实验室管理员工作区</p>
        <h1>实验室管理</h1>
        <p>调整实验室服务状态。存在有效预约时，系统会阻止直接停用。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container lab-grid">
        {% for lab in labs %}
        <article class="lab-card">
            <div class="lab-card-top">
                <span class="lab-id">LAB-{{ "%03d"|format(lab.id) }}</span>
                <span class="status {{ 'open' if lab.is_available else 'closed' }}">{{ lab.status }}</span>
            </div>
            <h2>{{ lab.name }}</h2>
            <dl class="lab-details">
                <div><dt>位置</dt><dd>{{ lab.location }}</dd></div>
                <div><dt>容量</dt><dd>{{ lab.capacity }}人</dd></div>
            </dl>
            <form method="post" action="{{ url_for('toggle_lab', lab_id=lab.id) }}">
                <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
                {% if lab.is_available %}
                <button class="button danger full" type="submit">设为维护中</button>
                {% else %}
                <button class="button primary full" type="submit">恢复开放</button>
                {% endif %}
            </form>
        </article>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

### `templates/approval_detail.html`

```html
{% extends "base.html" %}

{% block title %}审批申请｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <a class="back-link" href="{{ url_for('approvals') }}">← 返回审批队列</a>
        <p class="eyebrow">{{ booking.booking_no }}</p>
        <h1>审核预约申请</h1>
        <p>申请人：{{ booking.user.display_name }}（{{ booking.user.username }}）</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container form-layout">
        <article class="detail-card">
            <div class="lab-card-top">
                <h2>{{ booking.time_slot.lab.name }}</h2>
                <span class="status {{ booking.status_class }}">{{ booking.status_label }}</span>
            </div>
            <dl class="detail-list">
                <div><dt>预约时段</dt><dd>{{ booking.time_slot.date_label }} {{ booking.time_slot.time_label }}</dd></div>
                <div><dt>使用目的</dt><dd>{{ booking.purpose }}</dd></div>
                <div><dt>参加人数</dt><dd>{{ booking.attendee_count }}人 / 容量{{ booking.time_slot.lab.capacity }}人</dd></div>
                <div><dt>联系方式</dt><dd>{{ booking.contact }}</dd></div>
                <div><dt>所属专业</dt><dd>{{ booking.user.department }}</dd></div>
            </dl>
        </article>

        <aside class="stage-panel">
            {% if booking.status == 'PENDING' %}
            <span class="prototype-label">审批决定</span>
            <h2>通过或驳回</h2>
            <form method="post" action="{{ url_for('approval_decision', booking_id=booking.id) }}">
                <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
                <div class="form-row">
                    <label for="comment">审批意见</label>
                    <textarea id="comment" name="comment" rows="4" placeholder="通过可不填；驳回必须说明原因"></textarea>
                </div>
                <div class="decision-actions">
                    <button class="button primary" type="submit" name="decision" value="approve">通过申请</button>
                    <button class="button danger" type="submit" name="decision" value="reject">驳回申请</button>
                </div>
            </form>
            {% else %}
            <span class="prototype-label">审批结果</span>
            <h2>{{ booking.status_label }}</h2>
            {% if booking.reviewer %}<p>{{ booking.reviewer.display_name }}：{{ booking.review_comment }}</p>{% endif %}
            {% endif %}

            <div class="timeline">
                {% for history in booking.histories %}
                <div class="timeline-item">
                    <strong>{{ history.to_status_label }}</strong>
                    <span>{{ history.created_at.strftime('%m-%d %H:%M') }} · {{ history.actor.display_name }}</span>
                    <p>{{ history.note }}</p>
                </div>
                {% endfor %}
            </div>
        </aside>
    </div>
</section>
{% endblock %}
```

### `templates/approvals.html`

```html
{% extends "base.html" %}

{% block title %}预约审批｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">审批教师工作区</p>
        <h1>预约审批</h1>
        <p>核对申请内容，在待审批、已处理和全部记录之间切换。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container">
        <nav class="status-tabs" aria-label="审批状态筛选">
            <a class="{{ 'active' if selected_status == 'PENDING' else '' }}" href="{{ url_for('approvals', status='PENDING') }}">待审批</a>
            <a class="{{ 'active' if selected_status == 'APPROVED' else '' }}" href="{{ url_for('approvals', status='APPROVED') }}">已通过</a>
            <a class="{{ 'active' if selected_status == 'REJECTED' else '' }}" href="{{ url_for('approvals', status='REJECTED') }}">已驳回</a>
            <a class="{{ 'active' if selected_status == 'ALL' else '' }}" href="{{ url_for('approvals', status='ALL') }}">全部</a>
        </nav>

        <div class="result-summary">当前列表共 <strong>{{ bookings|length }}</strong> 条申请</div>
        <div class="booking-list">
            {% for booking in bookings %}
            <article class="booking-row">
                <div>
                    <span class="booking-no">{{ booking.booking_no }} · {{ booking.user.display_name }}</span>
                    <h2>{{ booking.time_slot.lab.name }}</h2>
                    <p>{{ booking.time_slot.date_label }} · {{ booking.time_slot.time_label }} · {{ booking.attendee_count }}人</p>
                </div>
                <div class="booking-actions">
                    <span class="status {{ booking.status_class }}">{{ booking.status_label }}</span>
                    <a class="text-link" href="{{ url_for('approval_detail', booking_id=booking.id) }}">审核申请</a>
                </div>
            </article>
            {% else %}
            <div class="empty-state"><h2>当前没有申请</h2><p>学生提交后会出现在这里。</p></div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```

### `templates/base.html`

```html
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}校园实验室预约系统{% endblock %}</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.svg') }}" type="image/svg+xml">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="version-strip">
        开发教学版 {{ app_version }} · 集成、验收与发布
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
                <a class="{{ 'active' if request.endpoint in ['my_bookings', 'booking_detail', 'reserve'] else '' }}" href="{{ url_for('my_bookings') }}">我的预约</a>
                {% elif g.user.role == 'approver' %}
                <a class="{{ 'active' if request.endpoint in ['approvals', 'approval_detail'] else '' }}" href="{{ url_for('approvals') }}">预约审批</a>
                {% elif g.user.role == 'admin' %}
                <a class="{{ 'active' if request.endpoint == 'admin_labs' else '' }}" href="{{ url_for('admin_labs') }}">实验室管理</a>
                {% endif %}
                {% endif %}
            </nav>
            <div class="user-area">
                {% if g.user %}
                <span class="user-chip"><strong>{{ g.user.display_name }}</strong><small>{{ g.user.role_name }}</small></span>
                <form class="inline-form" method="post" action="{{ url_for('logout') }}">
                    <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
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
            <a href="{{ url_for('version_info') }}">版本与运行信息 · {{ app_version }}</a>
        </div>
    </footer>
</body>
</html>
```

### `templates/booking_detail.html`

```html
{% extends "base.html" %}

{% block title %}预约详情｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <a class="back-link" href="{{ url_for('my_bookings') }}">← 返回我的预约</a>
        <p class="eyebrow">{{ booking.booking_no }}</p>
        <h1>预约详情</h1>
        <p>创建于 {{ booking.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container detail-layout">
        <article class="detail-card">
            <div class="lab-card-top">
                <h2>{{ booking.time_slot.lab.name }}</h2>
                <span class="status {{ booking.status_class }}">{{ booking.status_label }}</span>
            </div>
            <dl class="detail-list">
                <div><dt>预约时段</dt><dd>{{ booking.time_slot.date_label }} {{ booking.time_slot.time_label }}</dd></div>
                <div><dt>使用目的</dt><dd>{{ booking.purpose }}</dd></div>
                <div><dt>参加人数</dt><dd>{{ booking.attendee_count }}人</dd></div>
                <div><dt>联系方式</dt><dd>{{ booking.contact }}</dd></div>
                {% if booking.reviewer %}
                <div><dt>审批教师</dt><dd>{{ booking.reviewer.display_name }}</dd></div>
                <div><dt>审批意见</dt><dd>{{ booking.review_comment }}</dd></div>
                {% endif %}
            </dl>
            {% if booking.can_cancel %}
            <form method="post" action="{{ url_for('cancel_booking', booking_id=booking.id) }}" onsubmit="return confirm('确定取消这条预约吗？')">
                <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
                <button class="button danger" type="submit">取消预约</button>
            </form>
            {% endif %}
        </article>
        <aside class="stage-panel">
            <span class="prototype-label">状态说明</span>
            <h2>{{ booking.status_label }}</h2>
            {% if booking.status == 'PENDING' %}<p>申请已保存，等待审批教师处理。</p>{% endif %}
            {% if booking.status == 'CANCELLED' %}<p>申请已由学生取消，该时段可以重新预约。</p>{% endif %}
            {% if booking.status == 'APPROVED' %}<p>申请已通过，仍可在使用前取消。</p>{% endif %}
            {% if booking.status == 'REJECTED' %}<p>申请未通过，当前记录保留用于查询。</p>{% endif %}
            <div class="timeline">
                {% for history in booking.histories %}
                <div class="timeline-item">
                    <strong>{{ history.to_status_label }}</strong>
                    <span>{{ history.created_at.strftime('%m-%d %H:%M') }} · {{ history.actor.display_name }}</span>
                    <p>{{ history.note }}</p>
                </div>
                {% endfor %}
            </div>
        </aside>
    </div>
</section>
{% endblock %}
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
            <h2>我的预约</h2>
            <p>已经提交 {{ my_booking_count }} 条申请，可以查看状态或取消申请。</p>
            <a class="text-link" href="{{ url_for('my_bookings') }}">查看我的预约</a>
        </article>
        {% elif g.user.role == 'approver' %}
        <article class="feature-card">
            <span class="step-number">01</span>
            <h2>审批队列</h2>
            <p>当前有 {{ pending_count }} 条待审批申请，请核对实验室、时段、人数和用途。</p>
            <a class="text-link" href="{{ url_for('approvals') }}">进入审批队列</a>
        </article>
        {% else %}
        <article class="feature-card">
            <span class="step-number">01</span>
            <h2>实验室维护</h2>
            <p>共 {{ lab_count }} 间实验室，其中 {{ available_lab_count }} 间开放，可调整服务状态。</p>
            <a class="text-link" href="{{ url_for('admin_labs') }}">进入实验室管理</a>
        </article>
        {% endif %}

        <aside class="stage-panel">
            <span class="prototype-label">dev-v1.0验收点</span>
            <h2>三种角色已经集成</h2>
            <p>学生发起业务，审批教师改变预约状态，管理员维护基础资源；自动测试验证角色之间的数据衔接。</p>
        </aside>
    </div>
</section>
{% endblock %}
```

### `templates/errors/400.html`

```html
{% extends "base.html" %}

{% block title %}请求无法处理｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="error-page">
    <div class="container error-card">
        <span class="error-code">400</span>
        <h1>这次操作无法完成</h1>
        <p>{{ error.description or '提交的数据不符合要求，请检查后重试。' }}</p>
        <a class="button primary" href="{{ request.referrer or url_for('index') }}">返回上一页</a>
    </div>
</section>
{% endblock %}
```

### `templates/errors/403.html`

```html
{% extends "base.html" %}

{% block title %}没有访问权限｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="error-page">
    <div class="container error-card">
        <span class="error-code">403</span>
        <h1>当前账号不能访问</h1>
        <p>{{ error.description or '请切换到具备相应权限的账号。' }}</p>
        <a class="button primary" href="{{ url_for('dashboard') if g.user else url_for('login') }}">返回可用页面</a>
    </div>
</section>
{% endblock %}
```

### `templates/errors/404.html`

```html
{% extends "base.html" %}

{% block title %}页面不存在｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="error-page">
    <div class="container error-card">
        <span class="error-code">404</span>
        <h1>没有找到这个页面</h1>
        <p>网址可能输入有误，或者这条数据已经不存在。</p>
        <a class="button primary" href="{{ url_for('index') }}">返回首页</a>
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
                学生预约、教师审批、管理员维护三条业务线已经集成，并通过端到端验收测试。
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
            <p>这是课程手工开发阶段的完整发布基线，可从三个角色体验系统全过程。</p>
            <ul class="check-list">
                <li>学生：查询、提交、查看、取消</li>
                <li>教师：查看待办、通过、驳回</li>
                <li>管理员：启用和停用实验室</li>
                <li>版本页、健康检查和验收测试齐备</li>
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
                <span class="state available">学生预约闭环已完成</span>
            </article>
            <article class="feature-card">
                <span class="step-number">03</span>
                <h3>审批与管理</h3>
                <p>教师审批申请，管理员维护实验室的可用状态。</p>
                <span class="state available">三种角色全部可用</span>
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
            <h2 class="subheading">开放时段</h2>
            <div class="slot-list">
                {% for slot in time_slots %}
                <div class="slot-row">
                    <div>
                        <strong>{{ slot.date_label }}</strong>
                        <span>{{ slot.time_label }}</span>
                    </div>
                    {% if slot.is_available %}
                        {% if g.user and g.user.role == 'student' %}
                        <a class="button small" href="{{ url_for('reserve', slot_id=slot.id) }}">选择时段</a>
                        {% elif not g.user %}
                        <a class="text-link" href="{{ url_for('login') }}">登录后预约</a>
                        {% else %}
                        <span class="state available">当前空闲</span>
                        {% endif %}
                    {% else %}
                    <span class="state later">不可预约</span>
                    {% endif %}
                </div>
                {% else %}
                <p class="text-muted">暂时没有开放时段。</p>
                {% endfor %}
            </div>
        </article>
        <aside class="stage-panel">
            <span class="prototype-label">预约规则</span>
            <h2>先选资源，再填申请</h2>
            <p>每条时段属于一间实验室；已有待审批或已通过申请的时段，不能再被重复预约。</p>
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
                <a class="text-link" href="{{ url_for('lab_detail', lab_id=lab.id) }}">查看详情与时段</a>
                {% if not lab.is_available %}<span class="text-muted">当前不能预约</span>{% endif %}
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
            <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
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

### `templates/my_bookings.html`

```html
{% extends "base.html" %}

{% block title %}我的预约｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">学生个人中心</p>
        <h1>我的预约</h1>
        <p>只显示当前登录学生自己提交的预约申请。</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container">
        <div class="list-toolbar">
            <span>共 {{ bookings|length }} 条记录</span>
            <a class="button primary" href="{{ url_for('lab_list') }}">新建预约</a>
        </div>
        <div class="booking-list">
            {% for booking in bookings %}
            <article class="booking-row">
                <div>
                    <span class="booking-no">{{ booking.booking_no }}</span>
                    <h2>{{ booking.time_slot.lab.name }}</h2>
                    <p>{{ booking.time_slot.date_label }} · {{ booking.time_slot.time_label }} · {{ booking.purpose }}</p>
                </div>
                <div class="booking-actions">
                    <span class="status {{ booking.status_class }}">{{ booking.status_label }}</span>
                    <a class="text-link" href="{{ url_for('booking_detail', booking_id=booking.id) }}">查看详情</a>
                </div>
            </article>
            {% else %}
            <div class="empty-state">
                <h2>还没有预约记录</h2>
                <p>先查询实验室，再选择一个开放时段。</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```

### `templates/reserve.html`

```html
{% extends "base.html" %}

{% block title %}提交预约｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <a class="back-link" href="{{ url_for('lab_detail', lab_id=slot.lab.id) }}">← 返回实验室详情</a>
        <p class="eyebrow">学生预约申请</p>
        <h1>{{ slot.lab.name }}</h1>
        <p>{{ slot.date_label }} · {{ slot.time_label }} · 最多{{ slot.lab.capacity }}人</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container form-layout">
        <form class="reservation-form" method="post" action="{{ url_for('reserve', slot_id=slot.id) }}">
            <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
            <div class="form-row">
                <label for="purpose">使用目的</label>
                <textarea id="purpose" name="purpose" rows="4" required placeholder="例如：数字媒体课程作品展示">{{ form_data.purpose }}</textarea>
            </div>
            <div class="form-columns">
                <div class="form-row">
                    <label for="attendee_count">参加人数</label>
                    <input id="attendee_count" name="attendee_count" type="number" min="1" max="{{ slot.lab.capacity }}" value="{{ form_data.attendee_count }}" required>
                </div>
                <div class="form-row">
                    <label for="contact">联系方式</label>
                    <input id="contact" name="contact" value="{{ form_data.contact }}" required placeholder="手机或校园短号">
                </div>
            </div>
            <button class="button primary full" type="submit">确认提交预约</button>
        </form>

        <aside class="stage-panel">
            <span class="prototype-label">本次申请人</span>
            <h2>{{ g.user.display_name }}</h2>
            <div class="stage-item"><strong>账号</strong><p>{{ g.user.username }}</p></div>
            <div class="stage-item"><strong>所属专业</strong><p>{{ g.user.department }}</p></div>
            <div class="stage-item next"><strong>提交后状态</strong><p>待审批（dev-v0.5由教师处理）</p></div>
        </aside>
    </div>
</section>
{% endblock %}
```

### `templates/version.html`

```html
{% extends "base.html" %}

{% block title %}版本与运行信息｜校园实验室预约系统{% endblock %}

{% block content %}
<section class="page-heading">
    <div class="container">
        <p class="eyebrow">发布基线</p>
        <h1>{{ app_version }}</h1>
        <p>校园实验室预约与审批系统 · 手工开发阶段完整版本</p>
    </div>
</section>

<section class="section compact-top">
    <div class="container version-grid">
        <article class="detail-card">
            <h2>运行数据</h2>
            <div class="metric-grid">
                <div><strong>{{ counts.labs }}</strong><span>实验室</span></div>
                <div><strong>{{ counts.users }}</strong><span>演示用户</span></div>
                <div><strong>{{ counts.bookings }}</strong><span>预约记录</span></div>
            </div>
            <a class="text-link" href="{{ url_for('health') }}">查看JSON健康检查</a>
        </article>
        <article class="detail-card">
            <h2>技术路线</h2>
            <ol class="architecture-list">
                <li>浏览器与Jinja2页面</li>
                <li>Flask路由和业务校验</li>
                <li>Flask-SQLAlchemy数据模型</li>
                <li>SQLite本地数据库</li>
            </ol>
        </article>
    </div>
</section>
{% endblock %}
```

### `tests/conftest.py`

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

### `tests/test_acceptance.py`

```python
from sqlalchemy import select

from models import Booking, Lab, TimeSlot, db


def post_with_csrf(client, path, data=None, **kwargs):
    with client.session_transaction() as browser_session:
        token = browser_session.setdefault("_csrf_token", "acceptance-csrf-token")
    form_data = dict(data or {})
    form_data["_csrf_token"] = token
    return client.post(path, data=form_data, **kwargs)


def login(client, username):
    return post_with_csrf(
        client,
        "/login",
        {"username": username, "password": "123456"},
        follow_redirects=True,
    )


def logout(client):
    return post_with_csrf(client, "/logout", follow_redirects=True)


def test_three_roles_complete_one_end_to_end_workflow(app, client):
    """验收主线：学生提交—教师通过—学生取消—管理员停用。"""
    login(client, "20260001")
    with app.app_context():
        slot = db.session.scalar(
            select(TimeSlot).join(Lab).where(Lab.status == "可预约").order_by(TimeSlot.id)
        )
        slot_id = slot.id
        lab_id = slot.lab_id

    submitted = post_with_csrf(
        client,
        f"/reserve/{slot_id}",
        {
            "purpose": "课程最终验收演示",
            "attendee_count": "20",
            "contact": "13800000001",
        },
        follow_redirects=True,
    )
    assert submitted.status_code == 200
    assert "待审批" in submitted.get_data(as_text=True)
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))

    logout(client)
    login(client, "T1001")
    approved = post_with_csrf(
        client,
        f"/approvals/{booking_id}/decision",
        {"decision": "approve", "comment": "验收信息完整，同意。"},
        follow_redirects=True,
    )
    assert approved.status_code == 200
    assert "已通过" in approved.get_data(as_text=True)

    logout(client)
    login(client, "20260001")
    cancelled = post_with_csrf(
        client,
        f"/bookings/{booking_id}/cancel",
        follow_redirects=True,
    )
    assert cancelled.status_code == 200
    assert "已取消" in cancelled.get_data(as_text=True)

    logout(client)
    login(client, "A001")
    disabled = post_with_csrf(
        client,
        f"/admin/labs/{lab_id}/toggle",
        follow_redirects=True,
    )
    assert disabled.status_code == 200
    assert "已设为维护中" in disabled.get_data(as_text=True)

    with app.app_context():
        booking = db.session.get(Booking, booking_id)
        lab = db.session.get(Lab, lab_id)
        assert booking.status == "CANCELLED"
        assert [item.to_status for item in reversed(booking.histories)] == [
            "PENDING",
            "APPROVED",
            "CANCELLED",
        ]
        assert lab.status == "维护中"
```

### `tests/test_app.py`

```python
import pytest
from sqlalchemy import func, select

from app import LAB_SEED_DATA
from models import Booking, BookingHistory, Lab, TimeSlot, User, db


def post_with_csrf(client, path, data=None, **kwargs):
    """模拟浏览器携带页面中的CSRF令牌提交表单。"""
    with client.session_transaction() as browser_session:
        token = browser_session.setdefault("_csrf_token", "test-csrf-token")
    form_data = dict(data or {})
    form_data["_csrf_token"] = token
    return client.post(path, data=form_data, **kwargs)


def login(client, username="20260001", password="123456"):
    return post_with_csrf(
        client,
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def first_slot_id(app):
    with app.app_context():
        return db.session.scalar(select(TimeSlot.id).order_by(TimeSlot.id))


def submit_booking(client, slot_id, **overrides):
    data = {
        "purpose": "数字媒体课程作品展示",
        "attendee_count": "20",
        "contact": "13800000001",
    }
    data.update(overrides)
    return post_with_csrf(client, f"/reserve/{slot_id}", data=data, follow_redirects=True)


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v1.0" in response.get_data(as_text=True)


def test_database_is_seeded(app):
    with app.app_context():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()
        users = db.session.scalars(select(User).order_by(User.id)).all()
        slots = db.session.scalars(select(TimeSlot).order_by(TimeSlot.id)).all()

    assert len(labs) == len(LAB_SEED_DATA)
    assert labs[0].name == "软件工程实验室"
    assert [user.role for user in users] == ["student", "student", "approver", "admin"]
    assert users[0].password_hash != "123456"
    assert len(slots) == len(LAB_SEED_DATA) * 4


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
    assert "开放时段" in page


def test_unknown_lab_returns_404(client):
    assert client.get("/labs/999").status_code == 404


def test_reservation_page_contains_required_fields(app, client):
    login(client)
    response = client.get(f"/reserve/{first_slot_id(app)}")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'name="purpose"' in page
    assert 'name="attendee_count"' in page
    assert 'name="contact"' in page
    assert "确认提交预约" in page


def test_student_can_submit_and_view_booking(app, client):
    login(client)
    response = submit_booking(client, first_slot_id(app))
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "已提交，等待教师审批" in page
    assert "待审批" in page
    assert "数字媒体课程作品展示" in page

    with app.app_context():
        booking = db.session.scalar(select(Booking))
        assert booking.status == "PENDING"
        assert booking.user.username == "20260001"
        assert booking.histories[0].to_status == "PENDING"


def test_invalid_attendee_count_is_not_saved(app, client):
    login(client)
    response = submit_booking(client, first_slot_id(app), attendee_count="999")

    assert "参加人数应在" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.scalar(select(func.count()).select_from(Booking)) == 0


def test_student_can_cancel_own_booking(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))

    response = post_with_csrf(
        client,
        f"/bookings/{booking_id}/cancel",
        follow_redirects=True,
    )

    assert "已取消" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Booking, booking_id).status == "CANCELLED"
        history_statuses = db.session.scalars(
            select(BookingHistory.to_status).order_by(BookingHistory.id)
        ).all()
        assert history_statuses == ["PENDING", "CANCELLED"]


def test_student_cannot_view_another_students_booking(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    post_with_csrf(client, "/logout")
    login(client, username="20260018")

    assert client.get(f"/bookings/{booking_id}").status_code == 403


def test_student_can_login_and_see_student_dashboard(client):
    response = login(client)
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "张晨，您好" in page
    assert "学生工作台" in page
    assert "我的预约" in page


def test_invalid_password_does_not_create_session(client):
    response = login(client, password="wrong-password")
    page = response.get_data(as_text=True)

    assert "账号或密码错误" in page
    assert "登录系统" in page


def test_anonymous_user_is_redirected_to_login(client):
    response = client.get("/dashboard", follow_redirects=True)

    assert "请先登录" in response.get_data(as_text=True)
    assert "登录系统" in response.get_data(as_text=True)


def test_approver_cannot_open_student_reservation_page(app, client):
    login(client, username="T1001")

    assert client.get(f"/reserve/{first_slot_id(app)}").status_code == 403


def test_approver_can_approve_pending_booking(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    post_with_csrf(client, "/logout")
    login(client, username="T1001")

    queue_page = client.get("/approvals").get_data(as_text=True)
    assert "数字媒体课程作品展示" not in queue_page
    assert "张晨" in queue_page

    response = post_with_csrf(
        client,
        f"/approvals/{booking_id}/decision",
        data={"decision": "approve", "comment": "信息完整，同意使用。"},
        follow_redirects=True,
    )
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "已通过" in page
    assert "信息完整，同意使用" in page
    with app.app_context():
        booking = db.session.get(Booking, booking_id)
        assert booking.status == "APPROVED"
        assert booking.reviewer.username == "T1001"
        assert [history.to_status for history in reversed(booking.histories)] == [
            "PENDING",
            "APPROVED",
        ]


def test_rejection_requires_a_reason(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    post_with_csrf(client, "/logout")
    login(client, username="T1001")

    response = post_with_csrf(
        client,
        f"/approvals/{booking_id}/decision",
        data={"decision": "reject", "comment": "无"},
    )

    assert response.status_code == 400
    assert "驳回时请填写" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Booking, booking_id).status == "PENDING"


def test_student_cannot_open_approval_queue(client):
    login(client)

    assert client.get("/approvals").status_code == 403


def test_processed_booking_cannot_be_reviewed_twice(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    post_with_csrf(client, "/logout")
    login(client, username="T1001")
    post_with_csrf(
        client,
        f"/approvals/{booking_id}/decision",
        data={"decision": "approve", "comment": "同意"},
    )

    assert post_with_csrf(
        client,
        f"/approvals/{booking_id}/decision",
        data={"decision": "reject", "comment": "重复操作"},
    ).status_code == 400


def test_logout_clears_login_session(client):
    login(client)
    post_with_csrf(client, "/logout")

    assert client.get("/dashboard").status_code == 302


def test_post_without_csrf_token_is_rejected(client):
    response = client.post(
        "/login",
        data={"username": "20260001", "password": "123456"},
    )

    assert response.status_code == 400
    assert "表单已过期或来源无效" in response.get_data(as_text=True)


def test_custom_error_pages_explain_the_problem(app, client):
    missing = client.get("/labs/999")
    assert missing.status_code == 404
    assert "没有找到这个页面" in missing.get_data(as_text=True)

    login(client, username="T1001")
    forbidden = client.get(f"/reserve/{first_slot_id(app)}")
    assert forbidden.status_code == 403
    assert "当前账号不能访问" in forbidden.get_data(as_text=True)


def test_health_and_version_endpoints(client):
    health = client.get("/health")

    assert health.status_code == 200
    assert health.get_json() == {
        "status": "ok",
        "version": "dev-v1.0",
        "database": "ok",
    }
    version_page = client.get("/version").get_data(as_text=True)
    assert "手工开发阶段完整版本" in version_page
    assert "Flask-SQLAlchemy" in version_page


def test_admin_can_change_lab_service_status(app, client):
    login(client, username="A001")
    with app.app_context():
        maintenance_lab_id = db.session.scalar(
            select(Lab.id).where(Lab.status == "维护中")
        )

    response = post_with_csrf(
        client,
        f"/admin/labs/{maintenance_lab_id}/toggle",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "已恢复开放" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Lab, maintenance_lab_id).status == "可预约"


def test_non_admin_cannot_manage_labs(client):
    login(client)

    assert client.get("/admin/labs").status_code == 403


def test_admin_cannot_disable_lab_with_active_booking(app, client):
    login(client)
    slot_id = first_slot_id(app)
    submit_booking(client, slot_id)
    with app.app_context():
        lab_id = db.session.get(TimeSlot, slot_id).lab_id
    post_with_csrf(client, "/logout")
    login(client, username="A001")

    response = post_with_csrf(client, f"/admin/labs/{lab_id}/toggle")

    assert response.status_code == 400
    assert "仍有待审批或已通过的预约" in response.get_data(as_text=True)


def test_admin_page_contains_csrf_protected_actions(client):
    login(client, username="A001")
    page = client.get("/admin/labs").get_data(as_text=True)

    assert "实验室管理" in page
    assert page.count('name="_csrf_token"') >= len(LAB_SEED_DATA) + 1


@pytest.mark.parametrize("path", ["/", "/labs"])
def test_navigation_is_visible_on_each_page(client, path):
    page = client.get(path).get_data(as_text=True)

    assert "首页" in page
    assert "实验室" in page
    assert "登录" in page
```

### `tests/test_validators.py`

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

### `validators.py`

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
