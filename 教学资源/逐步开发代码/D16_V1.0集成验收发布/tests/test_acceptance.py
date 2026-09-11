from sqlalchemy import select

from models import Booking, Lab, TimeSlot, db


def post_with_csrf(client, path, data=None, **kwargs):
    with client.session_transaction() as browser_session:
        token = browser_session.setdefault("_csrf_token", "acceptance-csrf-token")
    form_data = dict(data or {})
    form_data["_csrf_token"] = token
    return client.post(path, data=form_data, **kwargs)


def login(client, username):
    return post_with_csrf(
        client,
        "/login",
        {"username": username, "password": "123456"},
        follow_redirects=True,
    )


def logout(client):
    return post_with_csrf(client, "/logout", follow_redirects=True)


def test_three_roles_complete_one_end_to_end_workflow(app, client):
    """验收主线：学生提交—教师通过—学生取消—管理员停用。"""
    login(client, "20260001")
    with app.app_context():
        slot = db.session.scalar(
            select(TimeSlot).join(Lab).where(Lab.status == "可预约").order_by(TimeSlot.id)
        )
        slot_id = slot.id
        lab_id = slot.lab_id

    submitted = post_with_csrf(
        client,
        f"/reserve/{slot_id}",
        {
            "purpose": "课程最终验收演示",
            "attendee_count": "20",
            "contact": "13800000001",
        },
        follow_redirects=True,
    )
    assert submitted.status_code == 200
    assert "待审批" in submitted.get_data(as_text=True)
    with app.app_context():
        booking_id = db.session.scalar(select(Booking.id))

    logout(client)
    login(client, "T1001")
    approved = post_with_csrf(
        client,
        f"/approvals/{booking_id}/decision",
        {"decision": "approve", "comment": "验收信息完整，同意。"},
        follow_redirects=True,
    )
    assert approved.status_code == 200
    assert "已通过" in approved.get_data(as_text=True)

    logout(client)
    login(client, "20260001")
    cancelled = post_with_csrf(
        client,
        f"/bookings/{booking_id}/cancel",
        follow_redirects=True,
    )
    assert cancelled.status_code == 200
    assert "已取消" in cancelled.get_data(as_text=True)

    logout(client)
    login(client, "A001")
    disabled = post_with_csrf(
        client,
        f"/admin/labs/{lab_id}/toggle",
        follow_redirects=True,
    )
    assert disabled.status_code == 200
    assert "已设为维护中" in disabled.get_data(as_text=True)

    with app.app_context():
        booking = db.session.get(Booking, booking_id)
        lab = db.session.get(Lab, lab_id)
        assert booking.status == "CANCELLED"
        assert [item.to_status for item in reversed(booking.histories)] == [
            "PENDING",
            "APPROVED",
            "CANCELLED",
        ]
        assert lab.status == "维护中"
