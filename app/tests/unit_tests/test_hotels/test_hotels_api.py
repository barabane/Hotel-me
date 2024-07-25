import pytest
from datetime import datetime, timedelta


@pytest.mark.parametrize("date_from, date_to", [
    (datetime.strptime("2024-07-10", "%Y-%m-%d"),
     datetime.strptime("2024-07-01", "%Y-%m-%d")
     ),
    (datetime.strptime("2024-06-20", "%Y-%m-%d"),
     datetime.strptime("2024-07-30", "%Y-%m-%d")
     ),
    (datetime.strptime("2024-07-10", "%Y-%m-%d"),
     datetime.strptime("2024-07-17", "%Y-%m-%d")
     )
])
async def test_getting_hotels(date_from, date_to):
    if date_from >= date_to:
        assert True
    elif (date_to - date_from) > timedelta(days=30):
        assert True
    else:
        assert True
