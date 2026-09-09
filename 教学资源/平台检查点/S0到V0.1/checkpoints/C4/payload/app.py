from flask import Flask


VERSION = "dev-v0.1"


def create_app(test_config=None):
    """创建并配置Flask应用。"""
    app = Flask(__name__)
    app.config.from_mapping(TESTING=False)

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return f"校园实验室预约系统 {VERSION}"

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
