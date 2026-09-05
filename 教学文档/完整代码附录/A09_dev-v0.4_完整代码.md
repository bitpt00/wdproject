# dev-v0.4 完整代码核对附录

> 本附录由冻结版本终点包机械生成，不是手工重新整理的代码。文件内容只统一为LF换行；原始字节数与SHA-256用于核对终点资源。

## 1. 文件清单

| 路径 | 原始字节数 | 代码行数 | 原始文件SHA-256 |
| --- | ---: | ---: | --- |
| `.gitignore` | 62 | 6 | `bb1173460471204c4b38c69ac9b1fe238efe3a175a029a3977a659bff182d955` |
| `VERSION` | 10 | 1 | `8c7ff9ee3da47c6c12c012a1ebc27891586964c93adabdd0f7b39d99c484cbcf` |
| `app.py` | 12195 | 362 | `89e1adf151b0e5f7c2030787145c1c846a853184e980c14600d9c3f8af596c62` |
| `models.py` | 4911 | 138 | `1bd6bce158ef2802ae5e0de6bae229dd65787038bb787b790e8533eb92eef539` |
| `requirements.txt` | 54 | 3 | `1f2fb163b1f8c0cae49cf5a4a8279685080d4c3126ae0e77527fa2ce231766f3` |
| `static/style.css` | 14160 | 877 | `e8e26bf6fee77ff24162b866f22d9d5dbe763a869bfe5a96aadc4e997253275c` |
| `templates/base.html` | 2859 | 66 | `922b57fc1328208e539790ec2a24972e4d5e65e4a8c88ad9816e1287fda15cc8` |
| `templates/booking_detail.html` | 2276 | 44 | `857bdfa5f749d7741f5eff9dd5b6bcb47861792b519bb21ef6894b6206150253` |
| `templates/dashboard.html` | 2255 | 52 | `b627a12318e7ea9d53c8981352c4d99f4be4aec11856e06b0529d8ed799a9e12` |
| `templates/index.html` | 2994 | 66 | `49ea8c47ffd165cb6b5fbd9ba495da72979be0f1f5f95a348b0731991b61ad74` |
| `templates/lab_detail.html` | 2607 | 59 | `3c821ec3df6b87b98339eab0cb23308f5cca75655899b3e8f0f934fda5f84b74` |
| `templates/labs.html` | 2989 | 71 | `c4a1825e54699474e6598b5f36deae7db8ac8a765f02dc979c9629a5429557d9` |
| `templates/login.html` | 1595 | 33 | `8bf1d1b294b3e59ce75527187ad4d7f1e2d57c7a5faa665423969d92dca6dddf` |
| `templates/my_bookings.html` | 1685 | 42 | `9df3f4e6aa7ac1fed874de65fdaf28d49cca7a010171cbdd92145157c66be2e8` |
| `templates/reserve.html` | 2249 | 44 | `259d4336a5b983672bec1b18393faffd416ae6bcabee4f4564b209dc60c723b1` |
| `tests/test_app.py` | 6411 | 204 | `6ccac1f053955695d4bd817940ab657107c888511549950bf771b784f5bdfe2f` |
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

### `VERSION`

```text
dev-v0.4
```

### `app.py`

```python
from pathlib import Path
from functools import wraps
from datetime import date, datetime, time, timedelta
from uuid import uuid4

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func, or_, select

from models import Booking, Lab, TimeSlot, User, db


VERSION = "dev-v0.4"

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
        my_booking_count = 0
        if g.user.role == "student":
            my_booking_count = db.session.scalar(
                select(func.count()).select_from(Booking).where(Booking.user_id == g.user.id)
            )
        return render_template("dashboard.html", my_booking_count=my_booking_count)

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
            abort(400)

        form_data = {
            "purpose": request.form.get("purpose", "").strip(),
            "attendee_count": request.form.get("attendee_count", "").strip(),
            "contact": request.form.get("contact", "").strip(),
        }
        errors = []
        if request.method == "POST":
            if len(form_data["purpose"]) < 5:
                errors.append("使用目的至少填写5个字。")

            try:
                attendee_count = int(form_data["attendee_count"])
            except ValueError:
                attendee_count = 0
            if attendee_count < 1 or attendee_count > slot.lab.capacity:
                errors.append(f"参加人数应在1至{slot.lab.capacity}人之间。")

            if len(form_data["contact"]) < 6:
                errors.append("请填写有效的联系方式。")

            if not errors:
                booking = Booking(
                    booking_no=f"YY{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}",
                    user=g.user,
                    time_slot=slot,
                    purpose=form_data["purpose"],
                    attendee_count=attendee_count,
                    contact=form_data["contact"],
                )
                db.session.add(booking)
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
            abort(403)
        return render_template("booking_detail.html", booking=booking)

    @app.post("/bookings/<int:booking_id>/cancel")
    @role_required("student")
    def cancel_booking(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404)
        if booking.user_id != g.user.id:
            abort(403)
        if not booking.can_cancel:
            abort(400)

        booking.status = "CANCELLED"
        booking.cancelled_at = datetime.now()
        db.session.commit()
        flash(f"预约{booking.booking_no}已取消。", "success")
        return redirect(url_for("booking_detail", booking_id=booking.id))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
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

    bookings = db.relationship("Booking", back_populates="user", lazy="select")

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cancelled_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="bookings")
    time_slot = db.relationship("TimeSlot", back_populates="bookings")

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
```

### `requirements.txt`

```text
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
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

    .booking-actions {
        align-items: flex-start;
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
        开发教学版 {{ app_version }} · 学生预约完整闭环
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
            </dl>
            {% if booking.can_cancel %}
            <form method="post" action="{{ url_for('cancel_booking', booking_id=booking.id) }}" onsubmit="return confirm('确定取消这条预约吗？')">
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
            <p>学生已经可以提交申请，dev-v0.5将在此加入真正的审批队列。</p>
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
            <span class="prototype-label">dev-v0.4观察点</span>
            <h2>数据如何走完一圈</h2>
            <p>从页面表单进入路由，完成服务器端校验后写入预约表，再按当前登录用户查询并显示。</p>
        </aside>
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
                本版本已经打通学生从选择时段、提交申请，到查看和取消预约的完整过程。
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
            <p>学生提交的数据会真正写入SQLite，并在“我的预约”中持续可见。</p>
            <ul class="check-list">
                <li>从实验室中选择开放时段</li>
                <li>校验用途、人数和联系方式</li>
                <li>生成唯一预约编号并保存</li>
                <li>学生可查看和取消自己的申请</li>
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
                <span class="state later">dev-v0.5加入教师审批</span>
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

### `tests/test_app.py`

```python
import pytest
from sqlalchemy import func, select

from app import LAB_SEED_DATA, create_app
from models import Booking, Lab, TimeSlot, User, db


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
    return client.post(f"/reserve/{slot_id}", data=data, follow_redirects=True)


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.4" in response.get_data(as_text=True)


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

    response = client.post(f"/bookings/{booking_id}/cancel", follow_redirects=True)

    assert "已取消" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Booking, booking_id).status == "CANCELLED"


def test_student_cannot_view_another_students_booking(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    client.post("/logout")
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
