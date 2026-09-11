from pathlib import Path
from functools import wraps
from datetime import date, datetime, time, timedelta
from uuid import uuid4

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func, inspect, or_, select, text

from models import Booking, BookingHistory, Lab, TimeSlot, User, db


VERSION = "dev-v0.5"

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
        upgrade_database_schema()
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
        pending_count = 0
        if g.user.role == "student":
            my_booking_count = db.session.scalar(
                select(func.count()).select_from(Booking).where(Booking.user_id == g.user.id)
            )
        elif g.user.role == "approver":
            pending_count = db.session.scalar(
                select(func.count()).select_from(Booking).where(Booking.status == "PENDING")
            )
        return render_template(
            "dashboard.html",
            my_booking_count=my_booking_count,
            pending_count=pending_count,
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
            abort(400)

        decision = request.form.get("decision", "")
        comment = request.form.get("comment", "").strip()
        if decision not in {"approve", "reject"}:
            abort(400)
        if decision == "reject" and len(comment) < 3:
            flash("驳回时请填写至少3个字的原因。", "error")
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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
