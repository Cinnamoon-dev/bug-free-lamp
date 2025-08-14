import pytest
from fastapi.testclient import TestClient

from main import app

# Casos de teste
# ----------------------------------------------------
# Criar um tipo de usuario valido
# Criar um tipo de usuario com uma string vazia
# Criar um tipo de usuario com um nome ja existente
# ----------------------------------------------------
# TODO
# Ver um tipo de usuário enviando um id cadastrado no banco
# TODO
# Ver um tipo de usuário enviando um id não cadastrado no banco
# ----------------------------------------------------
# Editar um tipo de usuario com o corpo da requisição vazio
# Editar um tipo de usuario com o corpo nulo
# Editar um tipo de usuario para um nome valido
# Editar um tipo de usuario para uma string vazia
# Editar um tipo de usuario para um nome ja existente
# ----------------------------------------------------
# Deletar um tipo de usuario que nao esta sendo usado
# TODO
# Deletar um tipo de usuario que esta sendo usado
# Deletar um tipo de usuario que nao existe
# ----------------------------------------------------


def create_user_type(name: str) -> dict[str, str]:
    """
    Helper function to generate a dictionary representing a user type payload for API requests.

    Args:
        name (str): The name of the user type.

    Returns:
        output (str): Dictionary with user type fields.
    """
    user_type = {"nome": name}
    return user_type

@pytest.fixture(scope="session")
def headers():
    return {"Content-Type": "application/json", "accept": "application/json"}

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_create_valid_user_type(client, headers):
    content = create_user_type("valid_user_type_name")
    response = client.post("/user/type", json=content, headers=headers)
    assert response.status_code == 200


def test_create_invalid_user_type(client, headers):
    content = create_user_type("")
    response = client.post("/user/type", json=content, headers=headers)
    assert response.status_code == 422


def test_create_repeated_user_type(client, headers):
    content = create_user_type("repeated_user_type")
    response = client.post("/user/type", json=content, headers=headers)
    response = client.post("/user/type", json=content, headers=headers)
    assert response.status_code == 400


def test_edit_valid_user_type(client, headers):
    to_edit = create_user_type("valid_user_type_name_for_edit_1")
    new_value = create_user_type("valid_user_type_name_for_edit_2")

    existing_user_type_id = client.post("/user/type/", json=to_edit, headers=headers).json()["id"]
    response = client.put(f"/user/type/{existing_user_type_id}", json=new_value, headers=headers)
    assert response.status_code == 200


def test_edit_invalid_user_type(client, headers):
    type_to_edit = create_user_type("type_to_edit")
    inserted_id = client.post("/user/type/", json=type_to_edit, headers=headers).json()["id"]

    content = create_user_type("")
    response = client.put(f"/user/type/{inserted_id}", json=content, headers=headers)
    assert response.status_code == 422


def test_edit_repeated_user_type(client, headers):
    mocked_type = create_user_type("mocked_type")
    existing_type = create_user_type("existing_type")

    mocked_id = client.post("/user/type/", json=mocked_type, headers=headers).json()["id"]
    client.post("/user/type/", json=existing_type, headers=headers)

    response = client.put(f"/user/type/{mocked_id}", json=existing_type, headers=headers)
    assert response.status_code == 400

def test_edit_user_type_with_empty_body(client, headers):
    existing_type = create_user_type("empty_body_test")
    existing_id = client.post("/user/type/", json=existing_type, headers=headers).json()["id"]

    response = client.put(f"/user/type/{existing_id}", json={}, headers=headers)
    assert response.status_code == 422

def test_edit_user_type_with_null_body(client, headers):
    existing_type = create_user_type("null_body_test")
    existing_id = client.post("/user/type/", json=existing_type, headers=headers).json()["id"]

    response = client.put(f"/user/type/{existing_id}", json=None, headers=headers)
    assert response.status_code == 422

def test_delete_unused_user_type(client, headers):
    mocked_type = create_user_type("type_to_delete")
    mocked_id = client.post("/user/type", json=mocked_type, headers=headers).json()["id"]

    response = client.delete(f"/user/type/{mocked_id}")
    assert response.status_code == 200

def test_delete_nonexistent_user_type(client, headers):
    mocked_type = create_user_type("nonexistent_user_type")
    mocked_id = client.post("/user/type", json=mocked_type, headers=headers).json()["id"]

    response = client.delete(f"/user/type/{mocked_id + 1999}")
    assert response.status_code == 200