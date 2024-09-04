import pytest
from app import create_app, db
from app.models import Task

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'No tasks yet' in response.data

def test_add_task(client):
    response = client.post('/add', data={
        'title': 'Test Task',
        'description': 'This is a test task.',
        'done': False
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data
