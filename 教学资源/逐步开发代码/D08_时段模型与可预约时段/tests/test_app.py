import pytest
from sqlalchemy import func, select

from app import create_app
from models import Lab, TimeSlot, User, db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    return create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}"})


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username="20260001"):
    return client.post("/login", data={"username": username, "password": "123456"}, follow_redirects=True)


def test_home_shows_slot_count(client):
    page = client.get("/").get_data(as_text=True)
    assert "D08" in page
    assert "16 条时段" in page


def test_database_contains_labs_users_and_slots(app):
    with app.app_context():
        assert db.session.scalar(select(func.count()).select_from(Lab)) == 4
        assert db.session.scalar(select(func.count()).select_from(User)) == 4
        assert db.session.scalar(select(func.count()).select_from(TimeSlot)) == 16


def test_lab_detail_shows_four_future_slots(client):
    page = client.get("/labs/1").get_data(as_text=True)
    assert page.count("可预约 · D09 开放提交") == 4
    assert "08:00—10:00" in page
    assert "10:10—12:10" in page


def test_maintenance_lab_slots_are_unavailable(client):
    page = client.get("/labs/4").get_data(as_text=True)
    assert page.count("不可预约") == 4


def test_student_dashboard_points_to_lab_list(client):
    page = login(client).get_data(as_text=True)
    assert "选择开放时段" in page
    assert "查看实验室" in page


def test_unknown_lab_returns_404(client):
    assert client.get("/labs/999").status_code == 404


def test_old_reservation_form_has_been_removed(client):
    assert client.get("/reservations/new").status_code == 404


def test_login_still_works(client):
    assert "张晨，您好" in login(client).get_data(as_text=True)
