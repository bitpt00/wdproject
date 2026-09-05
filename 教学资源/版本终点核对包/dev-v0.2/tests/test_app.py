import pytest
from sqlalchemy import select

from app import LAB_SEED_DATA, create_app
from models import Lab, db


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


def test_home_page_is_available(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "校园实验室预约与审批系统" in response.get_data(as_text=True)
    assert "dev-v0.2" in response.get_data(as_text=True)


def test_database_is_seeded(app):
    with app.app_context():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()

    assert len(labs) == len(LAB_SEED_DATA)
    assert labs[0].name == "软件工程实验室"


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


def test_unknown_lab_returns_404(client):
    assert client.get("/labs/999").status_code == 404


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
