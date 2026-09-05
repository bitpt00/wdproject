import pytest

from app import LABS, create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.1" in response.get_data(as_text=True)


def test_lab_page_shows_all_sample_labs(client):
    response = client.get("/labs")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    for lab in LABS:
        assert lab["name"] in page


def test_reservation_page_contains_required_fields(client):
    response = client.get("/reservations/new?lab=2")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'name="lab"' in page
    assert 'name="date"' in page
    assert 'name="start_time"' in page
    assert 'name="end_time"' in page
    assert 'name="attendees"' in page
    assert 'name="purpose"' in page
    assert 'value="2" selected' in page
    assert "提交预约（后续版本开放）" in page


@pytest.mark.parametrize("path", ["/", "/labs", "/reservations/new"])
def test_navigation_is_visible_on_each_page(client, path):
    page = client.get(path).get_data(as_text=True)

    assert "首页" in page
    assert "实验室" in page
    assert "预约申请" in page

