from os import access
from wsgiref import headers
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_blogs():
    response = client.get("/blog/all")
    assert response.status_code == 200


def test_auth_error():
    response = client.post("/token",
                           data={
                               "username": "",
                               "password": ""
                           })
    access_token = response.json().get("access_token")
    assert access_token is None
    message = response.json().get("detail")[0].get("msg")
    assert message == "field required"


# TODO: How I check sqlite3.OperationalError: database is locked

def test_auth_success():
    response = client.post("/token",
                           data={
                               "username": "cat",
                               "password": "cat"
                           })
    access_token = response.json().get("access_token")
    assert access_token


def test_post_article():
    response = client.post("/token",
                           data={
                               "username": "cat",
                               "password": "cat"
                           })
    access_token = response.json().get("access_token")
    print(access_token)

    assert access_token

    response = client.post(
        "/article/",
        json={
            "title": "Test Article",
            "content": "Test Content",
            "published": True,
            "creator_id": 3
        },
        headers={
            "Authorization": "bearer " + access_token
        })

    assert response.status_code == 200
    assert response.json().get("title") == "Test Article"
