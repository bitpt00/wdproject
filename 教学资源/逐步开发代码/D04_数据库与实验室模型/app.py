"""D04：把实验室数据从 Python 列表迁移到 SQLite 数据库。"""

from pathlib import Path

from flask import Flask, render_template, request
from sqlalchemy import func, select

from models import Lab, db


VERSION = "D04"

# 这组数据只负责数据库第一次启动时的初始化。
# 页面显示数据时，不再直接读取这个列表，而是查询 Lab 表。
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


def seed_labs():
    """仅在 Lab 表为空时写入课堂统一使用的四条样例数据。"""
    lab_count = db.session.scalar(select(func.count()).select_from(Lab))
    if lab_count == 0:
        db.session.add_all(Lab(**data) for data in LAB_SEED_DATA)
        db.session.commit()


def create_app(test_config=None):
    """创建应用、连接 SQLite、建表并注册页面路由。"""
    app = Flask(__name__, instance_relative_config=True)
    database_path = Path(app.instance_path) / "campus_lab.db"
    app.config.from_mapping(
        TESTING=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path.as_posix()}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    # 数据库扩展必须先绑定应用，才能创建表和执行查询。
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_labs()

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

    @app.get("/labs")
    def lab_list():
        # 与 V0.1 的关键区别：数据通过 SQL 查询从 Lab 表读出。
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()
        return render_template("labs.html", labs=labs)

    @app.get("/reservations/new")
    def reservation_form():
        selected_lab_id = request.args.get("lab", type=int)
        labs = db.session.scalars(
            select(Lab).where(Lab.status == "可预约").order_by(Lab.id)
        ).all()
        return render_template(
            "reservation_form.html",
            labs=labs,
            selected_lab_id=selected_lab_id,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
