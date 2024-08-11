import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to", [(1, "2024-07-01", "2024-07-20")]
)
async def test_crud_booking(
    room_id, date_from, date_to, authenticated_user: AsyncClient
):
    new_booking = await authenticated_user.post(
        "/bookings/add",
        params={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert new_booking.json()["id"]
    await authenticated_user.delete(f"/bookings/{new_booking.json()['id']}")
    booking = await authenticated_user.get(f"/bookings/{new_booking.json()['id']}")
    assert booking.status_code == 404


async def test_get_and_delete_bookings(authenticated_user: AsyncClient):
    response = await authenticated_user.get("/bookings/")
    for booking in response.json():
        await authenticated_user.delete(f"/bookings/{booking['id']}")
    response = await authenticated_user.get("/bookings/")
    assert len(response.json()) == 0
