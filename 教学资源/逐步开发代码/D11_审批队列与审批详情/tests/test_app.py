import pytest
from sqlalchemy import select

from app import create_app
from models import Booking, BookingHistory, TimeSlot, db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username="20260001"):
    return client.post(
        "/login",
        data={"username": username, "password": "123456"},
        follow_redirects=True,
    )


def create_pending_booking(app, client):
    """先以学生身份提交一条申请，供教师端读取。"""
    login(client)
    with app.app_context():
        slot_id = db.session.scalar(select(TimeSlot.id).order_by(TimeSlot.id))
    client.post(
        f"/reserve/{slot_id}",
        data={
            "purpose": "数字媒体课程作品展示",
            "attendee_count": "20",
            "contact": "13800000001",
        },
    )
    with app.app_context():
        return db.session.scalar(select(Booking.id))


def test_home_page_shows_d11(client):
    page = client.get("/").get_data(as_text=True)
    assert "校园实验室预约与审批系统" in page
    assert "D11" in page


def test_approver_can_read_queue_and_detail(app, client):
    booking_id = create_pending_booking(app, client)
    client.post("/logout")
    login(client, "T1001")

    queue = client.get("/approvals")
    assert queue.status_code == 200
    assert "张晨" in queue.get_data(as_text=True)
    assert "查看申请" in queue.get_data(as_text=True)

    detail = client.get(f"/approvals/{booking_id}")
    page = detail.get_data(as_text=True)
    assert detail.status_code == 200
    assert "数字媒体课程作品展示" in page
    assert "先读数据，再改变状态" in page


def test_d11_does_not_expose_decision_route(app, client):
    booking_id = create_pending_booking(app, client)
    client.post("/logout")
    login(client, "T1001")

    response = client.post(
        f"/approvals/{booking_id}/decision",
        data={"decision": "approve", "comment": "同意"},
    )
    assert response.status_code == 404
    with app.app_context():
        booking = db.session.get(Booking, booking_id)
        assert booking.status == "PENDING"
        assert [item.to_status for item in booking.histories] == ["PENDING"]


def test_student_cannot_open_approval_queue(client):
    login(client)
    assert client.get("/approvals").status_code == 403
