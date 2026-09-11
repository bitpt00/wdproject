import pytest
from sqlalchemy import func, select

from app import create_app
from models import Booking, TimeSlot, db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    return create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}"})


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username="20260001"):
    return client.post("/login", data={"username": username, "password": "123456"}, follow_redirects=True)


def test_home_explains_d09(client):
    page = client.get("/").get_data(as_text=True)
    assert "D09" in page
    assert "学生可以提交一条预约" in page


def test_slots_exist(app):
    with app.app_context():
        assert db.session.scalar(select(func.count()).select_from(TimeSlot)) == 16


def test_student_can_open_reserve_form(client):
    login(client)
    page = client.get("/reserve/1").get_data(as_text=True)
    assert "确认提交预约" in page
    assert "软件工程实验室" in page


def test_student_can_submit_and_view_booking(app, client):
    login(client)
    response = client.post("/reserve/1", data={"purpose": "数字媒体课程作品展示", "attendee_count": "20", "contact": "13800000000"}, follow_redirects=True)
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "预约提交成功" in page
    assert "待审批" in page
    with app.app_context():
        booking = db.session.scalar(select(Booking))
        assert booking.purpose == "数字媒体课程作品展示"
        assert booking.status == "PENDING"


def test_invalid_attendee_count_is_not_saved(app, client):
    login(client)
    page = client.post("/reserve/1", data={"purpose": "课程作品展示活动", "attendee_count": "99", "contact": "13800000000"}, follow_redirects=True).get_data(as_text=True)
    assert "参加人数应在1至40人之间" in page
    with app.app_context():
        assert db.session.scalar(select(func.count()).select_from(Booking)) == 0


def test_second_student_cannot_view_first_students_booking(app, client):
    login(client)
    client.post("/reserve/1", data={"purpose": "课程作品展示活动", "attendee_count": "20", "contact": "13800000000"})
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    client.post("/logout")
    login(client, username="20260018")
    assert client.get(f"/bookings/{booking_id}").status_code == 403


def test_teacher_cannot_reserve(client):
    login(client, username="T1001")
    assert client.get("/reserve/1").status_code == 403


def test_list_and_cancel_are_not_added_yet(client):
    login(client)
    assert client.get("/my-bookings").status_code == 404
    assert client.post("/bookings/1/cancel").status_code == 404
