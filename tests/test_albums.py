import pytest

from src.utils.validators import assert_albums_schema


@pytest.mark.albums
def test_get_all_albums(albums_client):
    response = albums_client.get_all_albums()

    assert response.status_code == 200, f"Status code is not 200"
    data = response.json()
    assert isinstance(data, list), f"Response /albums is not a list"
    assert len(data) > 0, f"The list of albums is empty"

    for album in data:
        assert_albums_schema(album)


@pytest.mark.albums
def test_get_albums_by_user(albums_client, test_data):
    response = albums_client.get_albums_for_specific_user(test_data["sample_user_ids"][0])
    assert response.status_code == 200, f"Status code is not 200"
    data = response.json()

    assert data[-1]["id"] == 10, f"The user does not have 10 albums"
