import pytest
from sqlalchemy import select

from app import create_app
from models import User, db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    return create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}"})


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username="20260001", password="123456"):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)


def test_home_is_available(client):
    page = client.get("/").get_data(as_text=True)
    assert "D06" in page
    assert "使用演示账号登录" in page


def test_users_are_seeded_with_password_hash(app):
    with app.app_context():
        users = db.session.scalars(select(User).order_by(User.id)).all()
    assert [user.username for user in users] == ["20260001", "T1001", "A001"]
    assert users[0].password_hash != "123456"
    assert users[0].check_password("123456")


def test_login_creates_session_and_shows_user(client):
    page = login(client).get_data(as_text=True)
    assert "张晨，登录成功" in page
    assert "登录会话已经建立" in page
    assert "欢迎回来" in page


def test_another_account_uses_same_generic_page(client):
    page = login(client, username="T1001").get_data(as_text=True)
    assert "李老师，登录成功" in page
    assert "登录会话已经建立" in page


def test_invalid_password_does_not_login(client):
    page = login(client, password="wrong").get_data(as_text=True)
    assert "账号或密码错误" in page
    assert "登录系统" in page


def test_dashboard_requires_login(client):
    page = client.get("/dashboard", follow_redirects=True).get_data(as_text=True)
    assert "请先登录" in page
    assert "登录系统" in page


def test_logged_in_name_is_visible_on_other_page(client):
    login(client)
    assert "张晨" in client.get("/labs").get_data(as_text=True)


def test_logout_clears_session(client):
    login(client)
    client.post("/logout")
    assert client.get("/dashboard").status_code == 302


def test_reservation_page_is_still_public(client):
    assert client.get("/reservations/new").status_code == 200
