from httpx import AsyncClient


async def test_register_user(ac: AsyncClient):
    response = await ac.post("/users/register", params={
        "email": "test1@testsss.com",
        "password": "te11sssst"
    })

    assert response.status_code == 200
