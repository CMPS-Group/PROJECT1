import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_invalid_username(client):
    response = client.post('/register', json={
        'username': '',
        'password': 'ValidPass123',
        'role': 'buyer'
    })
    assert response.status_code == 400
    assert b'Invalid username' in response.data

def test_register_invalid_password(client):
    response = client.post('/register', json={
        'username': 'validuser',
        'password': 'short',
        'role': 'buyer'
    })
    assert response.status_code == 400
    assert b'Invalid password' in response.data

def test_register_invalid_role(client):
    response = client.post('/register', json={
        'username': 'validuser',
        'password': 'ValidPass123',
        'role': 'hacker'
    })
    assert response.status_code == 400
    assert b'Invalid role' in response.data

def test_login_invalid_username(client):
    response = client.post('/login', json={
        'username': '',
        'password': 'ValidPass123'
    })
    assert response.status_code == 400
    assert b'Invalid username' in response.data

def test_login_invalid_password(client):
    response = client.post('/login', json={
        'username': 'validuser',
        'password': 'short'
    })
    assert response.status_code == 400
    assert b'Invalid password' in response.data
