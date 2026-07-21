import pytest
from tracker_api.api.repository import (
    get_price_history
)


def test_get_price_history(mocker):

    fake_result = mocker.Mock()
    fake_result.fetchall.return_value = [
        (1, 1, 1, 79999, "2026-07-20"),
        (2, 1, 2, 78999, "2026-07-21")
    ]

    fake_db = mocker.Mock()
    fake_db.execute.return_value = fake_result

    result = get_price_history(1, fake_db)

    assert result == [
        (1, 1, 1, 79999, "2026-07-20"),
        (2, 1, 2, 78999, "2026-07-21")
    ]

    fake_db.execute.assert_called_once()