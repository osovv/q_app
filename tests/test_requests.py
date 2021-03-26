import pytest
from app.api.server import server


@pytest.fixture(scope='session', autouse=True)
def client():
    with server.app.test_client() as client:
        yield client


def test_get_initial(client):
    resp = client.get('/users')
    assert resp.status_code == 200
    assert len(resp.get_json()) == 0


def test_post_not_existing(client):
    resp = client.post('/users', json={
        "username": "andrew",
        "password": "1984",
        "email": "andrew@gmail.com"
    })
    assert resp.status_code == 201


def test_post_existing_username(client):
    resp = client.post('/users', json={
        "username": "andrew",
        "password": "1984",
        "email": "random@gmail.com"
    })
    assert resp.status_code == 404
    assert resp.get_json() == {
        'error': '404 Not Found: User with username "andrew" already exists.'
    }


def test_post_existing_email(client):
    resp = client.post('/users', json={
        "username": "matthew",
        "password": "1984",
        "email": "andrew@gmail.com"
    })
    assert resp.status_code == 404
    assert resp.get_json() == {
        'error': '404 Not Found: User with email "andrew@gmail.com" already exists.'
    }


def test_get_existing(client):
    resp = client.get('/user/andrew')
    assert resp.status_code == 200
    assert resp.get_json() == {
        "username": "andrew",
        "password": "1984",
        "email": "andrew@gmail.com"
    }


def test_get_not_existing(client):
    resp = client.get('/user/matthew')
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "404 Not Found: User not found"}


def test_put_existing(client):
    resp = client.put('/user/andrew', json={
        "password": "2001",
        "email": "miet@gmail.com"
    })
    assert resp.status_code == 200
    assert resp.get_json() == {
        "username": "andrew",
        "password": "2001",
        "email": "miet@gmail.com"
    }


def test_put_not_existing(client):
    resp = client.put('/user/matthew', json={
        "password": "2001",
        "email": "miet@gmail.com"
    })
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "404 Not Found: User not found"}


def test_delete_existing(client):
    resp_get = client.get('/user/andrew')
    assert resp_get.status_code == 200
    resp = client.delete('/user/andrew')
    assert resp.status_code == 204
    resp_get = client.get('/user/andrew')
    assert resp_get.status_code == 404


def test_delete_not_existing(client):
    resp_get = client.get('/user/matthew')
    assert resp_get.status_code == 404
    resp = client.delete('/user/matthew')
    assert resp.status_code == 404
    assert resp.get_json() == {'error': '404 Not Found: User matthew not found'}
