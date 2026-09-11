"""D01：能够在浏览器中访问的第一个 Flask 程序。"""

from flask import Flask


CHECKPOINT = "D01"


def create_app(test_config=None):
    """创建应用对象；后面的所有页面都会注册到这个对象上。"""
    app = Flask(__name__)
    app.config.from_mapping(TESTING=False)

    # 自动测试会传入临时配置，正常课堂启动时这里不会执行。
    if test_config:
        app.config.update(test_config)

    # 路由把浏览器地址“/”与下面的函数连接起来。
    @app.get("/")
    def index():
        return (
            "<h1>校园实验室预约系统</h1>"
            "<p>D01 已完成：浏览器已经能够访问第一个 Flask 页面。</p>"
        )

    return app


app = create_app()


if __name__ == "__main__":
    # 服务器只监听本机 5000 端口，关闭命令窗口即可停止。
    app.run(host="127.0.0.1", port=5000, debug=True)
