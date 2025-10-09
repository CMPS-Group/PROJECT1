import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def get_token(client, username, password, role):
    # Register user
    client.post('/register', json={
        'username': username,
        'password': password,
        'role': role
    })
    # Login user
    response = client.post('/login', json={
        'username': username,
        'password': password
    })
    return response.get_json().get('access_token')

def auth_header(token):
    return {'Authorization': f'Bearer {token}'}

def test_seller_add_product_invalid_name(client):
    token = get_token(client, 'seller1', 'SellerPass123', 'seller')
    response = client.post('/seller/products', json={
        'name': 'x'*65,
        'description': 'desc',
        'price': 10,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid product name' in response.data

    # Name empty
    response = client.post('/seller/products', json={
        'name': '',
        'description': 'desc',
        'price': 10,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid product name' in response.data
    token = get_token(client, 'seller1', 'SellerPass123', 'seller')
    response = client.post('/seller/products', json={
        'name': 'x'*65,
        'description': 'desc',
        'price': 10,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid product name' in response.data

    # Name empty
    response = client.post('/seller/products', json={
        'name': '',
        'description': 'desc',
        'price': 10,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid product name' in response.data

def test_seller_add_product_invalid_price(client):
    token = get_token(client, 'seller2', 'SellerPass123', 'seller')
    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': -1,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid price' in response.data

    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': 100001,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid price' in response.data
    token = get_token(client, 'seller2', 'SellerPass123', 'seller')
    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': -1,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid price' in response.data

    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': 100001,
        'inventory': 5
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid price' in response.data

def test_seller_add_product_invalid_inventory(client):
    token = get_token(client, 'seller3', 'SellerPass123', 'seller')
    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': 10,
        'inventory': -1
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid inventory value' in response.data

    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': 10,
        'inventory': 100001
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid inventory value' in response.data
    token = get_token(client, 'seller3', 'SellerPass123', 'seller')
    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': 10,
        'inventory': -1
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid inventory value' in response.data

    response = client.post('/seller/products', json={
        'name': 'ValidName',
        'description': 'desc',
        'price': 10,
        'inventory': 100001
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid inventory value' in response.data

def test_admin_add_discount_invalid_code(client):
    token = get_token(client, 'admin1', 'AdminPass123', 'admin')
    response = client.post('/admin/discounts', json={
        'code': '',
        'percentage': 10
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid discount code' in response.data

    response = client.post('/admin/discounts', json={
        'code': 'x'*17,
        'percentage': 10
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid discount code' in response.data
    token = get_token(client, 'admin1', 'AdminPass123', 'admin')
    response = client.post('/admin/discounts', json={
        'code': '',
        'percentage': 10
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid discount code' in response.data

    response = client.post('/admin/discounts', json={
        'code': 'x'*17,
        'percentage': 10
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid discount code' in response.data

def test_admin_add_discount_invalid_percentage(client):
    token = get_token(client, 'admin2', 'AdminPass123', 'admin')
    response = client.post('/admin/discounts', json={
        'code': 'DISCOUNT10',
        'percentage': 0
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid percentage' in response.data

    response = client.post('/admin/discounts', json={
        'code': 'DISCOUNT10',
        'percentage': 101
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid percentage' in response.data
    token = get_token(client, 'admin2', 'AdminPass123', 'admin')
    response = client.post('/admin/discounts', json={
        'code': 'DISCOUNT10',
        'percentage': 0
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid percentage' in response.data

    response = client.post('/admin/discounts', json={
        'code': 'DISCOUNT10',
        'percentage': 101
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid percentage' in response.data

def test_admin_update_user_role_invalid_role(client):
    token = get_token(client, 'admin3', 'AdminPass123', 'admin')
    response = client.put('/admin/users/1/role', json={
        'role': 'hacker'
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid role' in response.data
    token = get_token(client, 'admin3', 'AdminPass123', 'admin')
    response = client.put('/admin/users/1/role', json={
        'role': 'hacker'
    }, headers=auth_header(token))
    assert response.status_code == 400
    assert b'Invalid role' in response.data
