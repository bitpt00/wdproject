from flask import Flask, render_template, request


VERSION = "dev-v0.1"

# V0.1暂时使用内存中的示例数据。
# V0.2会把这些数据迁移到SQLite数据库。
LABS = [
    {
        "id": 1,
        "name": "软件工程实验室",
        "location": "信息楼 A301",
        "capacity": 40,
        "equipment": "台式计算机、投影设备",
        "status": "可预约",
    },
    {
        "id": 2,
        "name": "人工智能实验室",
        "location": "信息楼 A305",
        "capacity": 32,
        "equipment": "GPU工作站、投影设备",
        "status": "可预约",
    },
    {
        "id": 3,
        "name": "网络技术实验室",
        "location": "信息楼 B201",
        "capacity": 36,
        "equipment": "网络实验箱、台式计算机",
        "status": "维护中",
    },
]


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__)
    app.config.from_mapping(TESTING=False)

    if test_config:
        app.config.update(test_config)

    @app.context_processor
    def inject_version():
        return {"app_version": VERSION}

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/labs")
    def lab_list():
        return render_template("labs.html", labs=LABS)

    @app.get("/reservations/new")
    def reservation_form():
        selected_lab_id = request.args.get("lab", type=int)
        return render_template(
            "reservation_form.html",
            labs=LABS,
            selected_lab_id=selected_lab_id,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

