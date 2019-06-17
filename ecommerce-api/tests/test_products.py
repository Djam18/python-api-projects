import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_list_products_empty(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_create_product(client):
    response = client.post('/products', json={
        'name': 'Test Product',
        'price': 9.99,
        'stock': 10,
        'category': 'test'
    })
    assert response.status_code == 201


def test_get_product(client):
    # create first
    client.post('/products', json={'name': 'Product A', 'price': 5.0, 'stock': 5, 'category': 'A'})
    # get all and take first id
    products = client.get('/products').get_json()
    if products:
        id = products[0]['id']
        response = client.get(f'/products/{id}')
        assert response.status_code == 200


def test_get_product_not_found(client):
    response = client.get('/products/99999')
    assert response.status_code == 404


def test_update_product(client):
    client.post('/products', json={'name': 'To Update', 'price': 1.0, 'stock': 1, 'category': 'x'})
    products = client.get('/products').get_json()
    if products:
        id = products[0]['id']
        response = client.put(f'/products/{id}', json={'name': 'Updated', 'price': 2.0, 'stock': 2})
        assert response.status_code == 200
