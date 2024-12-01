from starlette.testclient import TestClient

from main_router import app
from schemas.auth import UserLogin, UserRegister, UserResponse

client = TestClient(app=app)

def test_requires_authentication():
    response_stats = client.get("/fs/stats/")
    response_upload = client.get("/fs/stats/")
    assert response_stats.status_code == 403
    assert response_upload.status_code == 403

def test_register_user():
    user = UserRegister(user='JORGE', name='Usuario de JORGE', email='email@gmail.com', password='123456789')
    response_register = client.post("/auth/register/", json=user.model_dump())
    assert response_register.status_code == 200

def test_authenticate_valid_user():
    user_login = UserLogin(user='JORGE', password='123456789')
    response_login = client.post("/auth/authenticate/", json=user_login.model_dump())
    assert response_login.status_code == 200

def test_authenticate_invalid_user():
    user_login = UserLogin(user='malusuario', password='blabla')
    response_login = client.post("/auth/authenticate/", json=user_login.model_dump())
    assert response_login.status_code == 403

def test_upload_file():
    user_login = UserLogin(user='JORGE', password='123456789')
    response_login = client.post("/auth/authenticate/", json=user_login.model_dump())
    body = response_login.json()
    token = body['jwt']
    
    file = open('requirements.txt', 'rb')
    response_file = client.post("/fs/file/?file_name=requirements.txt&file_path=", files={'file': file})
    file.close()

    assert response_file.status_code == 200

def test_cant_upload_file_with_invalid_path():
    user_login = UserLogin(user='JORGE', password='123456789')
    response_login = client.post("/auth/authenticate/", json=user_login.model_dump())
    body = response_login.json()
    token = body['jwt']
    
    file = open('requirements.txt', 'rb')
    response_file = client.post("/fs/file/?file_name=requirements.txt&file_path=malpath//", files={'file': file})
    file.close()

    assert response_file.status_code == 422

def test_get_stats_for_admin():
    user_login = UserLogin(user='fpaesani', password='123456')
    response_login = client.post("/auth/authenticate/", json=user_login.model_dump())
    response_stats = client.get("/fs/stats/")

    assert response_stats.status_code == 200

def test_not_get_stats_for_non_admin():
    user_login = UserLogin(user='JORGE', password='123456789')
    response_login = client.post("/auth/authenticate/", json=user_login.model_dump())
    response_stats = client.get("/fs/stats/")

    assert response_stats.status_code == 403