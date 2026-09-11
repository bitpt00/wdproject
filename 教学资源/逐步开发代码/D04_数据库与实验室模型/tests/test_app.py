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


def test_home_shows_database_counts(client):
    page = client.get("/").get_data(as_text=True)
    assert "D04" in page
    assert "4 间" in page
    assert "3 间可预约" in page


def test_database_is_seeded(app):
    with app.app_context():
        labs = db.session.scalars(select(Lab).order_by(Lab.id)).all()
    assert len(labs) == len(LAB_SEED_DATA)
    assert labs[0].name == "软件工程实验室"


def test_lab_page_reads_all_database_rows(client):
    page = client.get("/labs").get_data(as_text=True)
    for lab in LAB_SEED_DATA:
        assert lab["name"] in page


def test_form_reads_only_available_labs(client):
    page = client.get("/reservations/new?lab=2").get_data(as_text=True)
    assert "人工智能实验室" in page
    assert "网络技术实验室" not in page
    assert 'value="2" selected' in page


@pytest.mark.parametrize("path", ["/", "/labs", "/reservations/new"])
def test_main_pages_are_available(client, path):
    assert client.get(path).status_code == 200
