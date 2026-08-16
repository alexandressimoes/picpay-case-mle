from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
import api_model_serving.app.main as main


client = TestClient(main.app)


def test_root_returns_hello_world() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_check_returns_healthy() -> None:
    response = client.get("/health-check/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_load_model_success() -> None:
    main.model_manager.load_model_async = AsyncMock(return_value=None)

    response = client.post("/load/", json={"model": "en_core_web_sm"})

    assert response.status_code == 200
    assert response.json()["model"] == "en_core_web_sm"
    assert "carregado com sucesso" in response.json()["message"]
    main.model_manager.load_model_async.assert_awaited_once_with("en_core_web_sm")


def test_load_model_empty_returns_400() -> None:
    response = client.post("/load/", json={"model": "   "})
    assert response.status_code == 400


def test_predict_success() -> None:
    expected = {
        "input": "Pix para Maria de 100 reais",
        "output": {"PERSON": "Maria", "MONEY": "100 reais"},
        "model_name": "pt_core_news_sm",
        "timestamp": "2026-08-16T12:00:00.000000Z",
    }
    main.model_manager.predict_async = AsyncMock(return_value=expected)

    response = client.post(
        "/predict/",
        json={"text": "Pix para Maria de 100 reais", "model": "pt_core_news_sm"},
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_predict_value_error_returns_400() -> None:
    main.model_manager.predict_async = AsyncMock(side_effect=ValueError("Nenhum modelo foi carregado ainda"))

    response = client.post("/predict/", json={"text": "teste"})

    assert response.status_code == 400
    assert "Nenhum modelo" in response.json()["detail"]


def test_list_predictions_success() -> None:
    expected = [
        {
            "input": "John transfer 20 dollars",
            "output": {"PERSON": "John", "MONEY": "20 dollars"},
            "model_name": "en_core_web_sm",
            "timestamp": "2026-08-16T12:00:00.000000Z",
        }
    ]
    main.model_manager.list_predictions_async = AsyncMock(return_value=expected)

    response = client.get("/list/")

    assert response.status_code == 200
    assert response.json() == {"predictions": expected}


def test_list_models_success() -> None:
    expected_registry = {
        "downloaded_models": ["en_core_web_sm", "pt_core_news_sm"],
        "last_used_model": "pt_core_news_sm",
    }
    main.model_manager.get_model_registry_async = AsyncMock(return_value=expected_registry)

    response = client.get("/list-models/")

    assert response.status_code == 200
    assert response.json() == expected_registry


def test_delete_model_success() -> None:
    main.model_manager.delete_model_async = AsyncMock(return_value=None)

    response = client.delete("/delete-model/", params={"model_version": "en_core_web_sm"})

    assert response.status_code == 200
    assert "deletado com sucesso" in response.json()["message"]


def test_delete_model_not_found_returns_404() -> None:
    main.model_manager.delete_model_async = AsyncMock(side_effect=ValueError("Modelo nao encontrado"))

    response = client.delete("/delete-model/", params={"model_version": "inexistente"})

    assert response.status_code == 404
