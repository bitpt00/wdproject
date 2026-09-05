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
