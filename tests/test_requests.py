from app.api.server import test_client


def test_get_initial():
    resp = test_client.get('/users')
    assert resp.status_code == 200
    assert len(resp.get_json()) == 0


def test_post_not_existing():
    resp = test_client.post('/users', json={
        "username": "andrew",
        "password": "1984",
        "email": "andrew@gmail.com"
    })
    assert resp.status_code == 201


def test_post_existing_username():
    resp = test_client.post('/users', json={
        "username": "andrew",
        "password": "1984",
        "email": "random@gmail.com"
    })
    assert resp.status_code == 404
    assert resp.get_json() == {
        'error': '404 Not Found: User with username "andrew" already exists.'
    }


def test_post_existing_email():
    resp = test_client.post('/users', json={
        "username": "matthew",
        "password": "1984",
        "email": "andrew@gmail.com"
    })
    assert resp.status_code == 404
    assert resp.get_json() == {
        'error': '404 Not Found: User with email "andrew@gmail.com" already exists.'
    }


def test_get_existing():
    resp = test_client.get('/user/andrew')
    assert resp.status_code == 200
    assert resp.get_json() == {
        "username": "andrew",
        "password": "1984",
        "email": "andrew@gmail.com"
    }


def test_get_not_existing():
    resp = test_client.get('/user/matthew')
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "404 Not Found: User not found"}


def test_put_existing():
    resp = test_client.put('/user/andrew', json={
        "password": "2001",
        "email": "miet@gmail.com"
    })
    assert resp.status_code == 200
    assert resp.get_json() == {
        "username": "andrew",
        "password": "2001",
        "email": "miet@gmail.com"
    }


def test_put_not_existing():
    resp = test_client.put('/user/matthew', json={
        "password": "2001",
        "email": "miet@gmail.com"
    })
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "404 Not Found: User not found"}


"""
For some reason flask.app.test_client.delete() doesn't work. Need to look it up.

def test_delete_existing():
    resp = test_client.delete('/user/andrew')
    assert resp.status_code == 200


def test_delete_not_existing():
    resp = test_client.delete('/user/matthew')
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "404 Not Found: User not found"}
"""
