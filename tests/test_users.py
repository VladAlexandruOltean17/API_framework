from time import sleep

import pytest
from src.utils.validators import assert_user_schema, assert_valid_email


@pytest.mark.users
def test_get_all_users_returns_list_of_valid_users(users_client):
    """
    Verificăm că:
    - GET /users returnează 200
    - răspunsul este o listă
    - fiecare user respectă schema minimă
    """
    response = users_client.get_all_users()

    assert response.status_code == 200, "Status code nu este 200 pentru /users"
    data = response.json()
    assert isinstance(data, list), "Răspunsul /users nu este listă"
    assert len(data) > 0, "Lista de users este goală"

    for user in data:
        assert_user_schema(user)
        assert_valid_email(user["email"])


@pytest.mark.users
def test_get_invalid_user_returns_404_or_empty(users_client, test_data):
    """
    Test negativ:
    - cerem useri cu id-uri invalide
    - ne așteptăm la 404 sau obiect gol / comportament specific API-ului
    """
    for invalid_id in test_data["invalid_user_ids"]:
        response = users_client.get_user_by_id(invalid_id)

        # JSONPlaceholder poate răspunde cu {} și 200 la unele endpointuri.
        # Aici putem adapta ulterior la comportamentul real observat.
        assert response.status_code in (200, 404), (
            f"Pentru user invalid {invalid_id}, am primit {response.status_code}"
        )


@pytest.mark.users
def test_get_an_invalid_user(users_client, test_data):
    invalid_id = test_data["invalid_user_ids"][0]
    response = users_client.get_invalid_user(invalid_id)
    assert response.status_code == 404, f"For invalid user {invalid_id}, got {response.status_code}"


# Check in this test case the custom timeout
# set for 0.1 seconds
@pytest.mark.timeout(0.1)
@pytest.mark.users
def test_get_a_specific_user_and_check_the_email(users_client, test_data):
    # sleep(5)
    response = users_client.get_user_by_id(test_data["sample_user_ids"][1])
    assert response.status_code == 200, f"Status is not 200"
    data = response.json()
    user_email = data["email"]
    assert_valid_email(user_email)



