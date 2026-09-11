"""D02：让 Flask 路由使用 Jinja2 模板生成页面。"""

from flask import Flask, render_template


CHECKPOINT = "D02"


def create_app(test_config=None):
    """创建并配置 Flask 应用。"""
    app = Flask(__name__)
    app.config.from_mapping(TESTING=False)

    if test_config:
        app.config.update(test_config)

    # 上下文处理器把 checkpoint 自动提供给所有模板。
    @app.context_processor
    def inject_checkpoint():
        return {"checkpoint": CHECKPOINT}

    @app.get("/")
    def index():
        # D01 直接返回字符串；D02 改为渲染 templates/index.html。
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
