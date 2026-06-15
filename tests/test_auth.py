import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_register_success(ac: AsyncClient):
    """Тест успешной регистрации пользователя."""
    response = await ac.post(
        "/api/v1/auth/register",
        json={"email": "tester@example.com", "password": "superpassword"}
    )
    
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "tester@example.com"
    assert "password" not in response.json()

async def test_register_duplicate_email(ac: AsyncClient):
    """Тест того, что нельзя создать двух юзеров с одинаковой почтой."""
    await ac.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    response = await ac.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "differentpassword"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Пользователь с таким email уже зарегистрирован"

async def test_login_success(ac: AsyncClient):
    """Тест успешного логина и выдачи токена."""
    payload = {"email": "login@example.com", "password": "correct_password"}
    await ac.post("/api/v1/auth/register", json=payload)
    
    response = await ac.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"