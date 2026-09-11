"""D08 数据模型：用户、实验室和开放时段。"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        return {"student": "学生", "approver": "审批教师", "admin": "实验室管理员"}.get(self.role, "未知角色")


class Lab(db.Model):
    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="可预约")
    description = db.Column(db.Text, nullable=False, default="")

    # 一间实验室可以有多个开放时段；删除实验室时同时删除它的时段。
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
    """某间实验室在某天的一段开放时间。"""

    __tablename__ = "time_slots"

    id = db.Column(db.Integer, primary_key=True)
    # 外键把每条时段连接到一间实验室。
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"), index=True, nullable=False)
    booking_date = db.Column(db.Date, index=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=True)

    lab = db.relationship("Lab", back_populates="time_slots")

    @property
    def date_label(self):
        weekdays = "一二三四五六日"
        return f"{self.booking_date:%Y-%m-%d} 周{weekdays[self.booking_date.weekday()]}"

    @property
    def time_label(self):
        return f"{self.start_time:%H:%M}—{self.end_time:%H:%M}"

    @property
    def is_available(self):
        # D08 尚无预约表，因此这里只检查时段和实验室是否开放。
        return self.is_open and self.lab.is_available
