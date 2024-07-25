import pytest
from app.users.dao import UserDAO


@pytest.mark.parametrize("user_id,email,exists", [
    (1, "test@test.com", True),
    (2, "artem@example.com", True),
    (5, ".....", False)
])
async def test_find_by_id(user_id, email, exists):
    user = await UserDAO.find_by_id(user_id)
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user


@pytest.mark.parametrize("email,exists", [
    ("test@test.com", True),
    ("test1@test1.com", False)
])
async def test_find_one_or_none(email, exists):
    user = await UserDAO.find_one_or_none(email=email)
    if exists:
        assert user
        assert user.email == email
    else:
        assert not user
