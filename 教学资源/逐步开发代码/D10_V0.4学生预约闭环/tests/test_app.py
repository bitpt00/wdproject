import pytest
from sqlalchemy import func, select

from app import LAB_SEED_DATA, create_app
from models import Booking, Lab, TimeSlot, User, db


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


def login(client, username="20260001", password="123456"):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def first_slot_id(app):
    with app.app_context():
        return db.session.scalar(select(TimeSlot.id).order_by(TimeSlot.id))


def submit_booking(client, slot_id, **overrides):
    data = {
        "purpose": "数字媒体课程作品展示",
        "attendee_count": "20",
        "contact": "13800000001",
    }
    data.update(overrides)
    return client.post(f"/reserve/{slot_id}", data=data, follow_redirects=True)


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.4" in response.get_data(as_text=True)


def test_database_is_seeded(app):
    with app.app_context():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()
        users = db.session.scalars(select(User).order_by(User.id)).all()
        slots = db.session.scalars(select(TimeSlot).order_by(TimeSlot.id)).all()

    assert len(labs) == len(LAB_SEED_DATA)
    assert labs[0].name == "软件工程实验室"
    assert [user.role for user in users] == ["student", "student", "approver", "admin"]
    assert users[0].password_hash != "123456"
    assert len(slots) == len(LAB_SEED_DATA) * 4


def test_lab_page_shows_database_labs(client):
    response = client.get("/labs")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    for lab in LAB_SEED_DATA:
        assert lab["name"] in page


def test_lab_list_can_filter_by_keyword_and_status(client):
    page = client.get("/labs?keyword=GPU&status=可预约").get_data(as_text=True)

    assert "人工智能实验室" in page
    assert "软件工程实验室" not in page
    assert "网络技术实验室" not in page


def test_lab_detail_comes_from_database(client):
    response = client.get("/labs/2")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "人工智能实验室" in page
    assert "计算机视觉实验" in page
    assert "开放时段" in page


def test_unknown_lab_returns_404(client):
    assert client.get("/labs/999").status_code == 404


def test_reservation_page_contains_required_fields(app, client):
    login(client)
    response = client.get(f"/reserve/{first_slot_id(app)}")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'name="purpose"' in page
    assert 'name="attendee_count"' in page
    assert 'name="contact"' in page
    assert "确认提交预约" in page


def test_student_can_submit_and_view_booking(app, client):
    login(client)
    response = submit_booking(client, first_slot_id(app))
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "已提交，等待教师审批" in page
    assert "待审批" in page
    assert "数字媒体课程作品展示" in page

    with app.app_context():
        booking = db.session.scalar(select(Booking))
        assert booking.status == "PENDING"
        assert booking.user.username == "20260001"


def test_invalid_attendee_count_is_not_saved(app, client):
    login(client)
    response = submit_booking(client, first_slot_id(app), attendee_count="999")

    assert "参加人数应在" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.scalar(select(func.count()).select_from(Booking)) == 0


def test_student_can_cancel_own_booking(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))

    response = client.post(f"/bookings/{booking_id}/cancel", follow_redirects=True)

    assert "已取消" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Booking, booking_id).status == "CANCELLED"


def test_student_cannot_view_another_students_booking(app, client):
    login(client)
    submit_booking(client, first_slot_id(app))
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))
    client.post("/logout")
    login(client, username="20260018")

    assert client.get(f"/bookings/{booking_id}").status_code == 403


def test_student_can_login_and_see_student_dashboard(client):
    response = login(client)
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "张晨，您好" in page
    assert "学生工作台" in page
    assert "我的预约" in page


def test_invalid_password_does_not_create_session(client):
    response = login(client, password="wrong-password")
    page = response.get_data(as_text=True)

    assert "账号或密码错误" in page
    assert "登录系统" in page


def test_anonymous_user_is_redirected_to_login(client):
    response = client.get("/dashboard", follow_redirects=True)

    assert "请先登录" in response.get_data(as_text=True)
    assert "登录系统" in response.get_data(as_text=True)


def test_approver_cannot_open_student_reservation_page(app, client):
    login(client, username="T1001")

    assert client.get(f"/reserve/{first_slot_id(app)}").status_code == 403


def test_logout_clears_login_session(client):
    login(client)
    client.post("/logout")

    assert client.get("/dashboard").status_code == 302


@pytest.mark.parametrize("path", ["/", "/labs"])
def test_navigation_is_visible_on_each_page(client, path):
    page = client.get(path).get_data(as_text=True)

    assert "首页" in page
    assert "实验室" in page
    assert "登录" in page
