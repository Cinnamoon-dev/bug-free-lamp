import pytest
from fastapi.testclient import TestClient

from main import app

# Casos de teste
# ----------------------------------------------------
# Criar um tipo de usuario valido
# Criar um tipo de usuario com uma string vazia
# Criar um tipo de usuario com um nome ja existente
# ----------------------------------------------------
# Ver um tipo de usuário enviando um id inválido
# Ver um tipo de usuário enviando um id válido
# ----------------------------------------------------
# Editar um tipo de usuario sem mandar o corpo da requisição, ou com o corpo vazio
# Editar um tipo de usuario para um nome valido
# Editar um tipo de usuario para uma string vazia
# Editar um tipo de usuario para um nome ja existente
# Editar um tipo de usuário enviando id inválido
# ----------------------------------------------------
# Deletar um tipo de usuario que nao esta sendo usado
# Deletar um tipo de usuario que esta sendo usado
# Deletar um tipo de usuario que nao existe
# Deletar um tipo de usuário enviando id inválido
# ----------------------------------------------------


def create_user_type(name: str) -> str:
    """Retorna uma string do dict criado, usar em `client.method(content=STRING)`."""
    user_type = {"nome": name}

    return str(user_type).replace("'", '"')


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_create_valid_user_type(client):
    content = create_user_type("valid_user_type_name")
    response = client.post("/user/type", content=content)
    assert response.status_code == 200


def test_create_invalid_user_type(client):
    content = create_user_type("")
    response = client.post("/user/type", content=content)
    assert response.status_code == 422


def test_create_repeated_user_type(client):
    content = create_user_type("valid_user_type_name")
    response = client.post("/user/type", content=content)
    assert response.status_code == 400


def test_edit_valid_user_type(client):
    to_edit = create_user_type("valid_user_type_name_for_edit_1")
    new_value = create_user_type("valid_user_type_name_for_edit_2")

    existing_user_type_id = client.post("/user/type/", content=to_edit).json()["id"]
    print(existing_user_type_id)
    response = client.put(
        f"/user/type/edit/{existing_user_type_id}", content=new_value
    )
    assert response.status_code == 200


def test_edit_invalid_user_type(client):
    type_to_edit = create_user_type("type_to_edit")
    inserted_id = client.post("/user/type/", content=type_to_edit).json()["id"]

    content = create_user_type("")
    response = client.put(f"/user/type/{inserted_id}", content=content)
    assert response.status_code == 400


def test_edit_repeated_user_type(client):
    mocked_type = create_user_type("mocked_type")
    existing_type = create_user_type("existing_type")

    mocked_id = client.post("/user/type/", content=mocked_type).json()["id"]
    client.post("/user/type/", content=existing_type)

    response = client.put(f"/user/type/{mocked_id}", content=existing_type)
    assert response.status_code == 400

def test_delete_unused_user_type(client):
    mocked_type = create_user_type("type_to_delete")
    mocked_id = client.post("/user/type", content=mocked_type).json()["id"]

    response = client.delete(f"/user/type/{mocked_id}")
    assert response.status_code == 200
