# project/tests/test_summaries.py

import json

# import pytest


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]
    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_summaries(test_app_with_db):
    response = test_app_with_db.get("/summaries/")
    response_dict = response.json()
    assert response.status_code == 200
    assert len(response_dict) >= 0


def test_remove_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": summary_id, "url": "https://foo.bar"}


def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": "https://foomodif.bar", "summary": "updated!!"}),
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": "https://foomodif.bar",
        "summary": "updated!!",
        "id": summary_id,
    }


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999999999/",
        data=json.dumps({"url": "https://foomodif.bar", "summary": "updated!!"}),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/${summary_id}/",
        data="""{
            "url": "https://foomodif.bar",
            "summar": "updat
        }""",
    )
    result = response.json()
    assert response.status_code == 422
    assert (
        result["detail"][0]["msg"]
        == "Invalid control character at: line 3 column 29 (char 73)"
    )
    assert result["detail"][0]["type"] == "value_error.jsondecode"


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/${summary_id}/",
        data=json.dumps(
            {
                "url": "no-url",
                "summar": "otr!!!",
            }
        ),
    )

    response_data = response.json()
    assert response.status_code == 422
    assert response_data["detail"][1]["loc"][1] == "url"
    assert response_data["detail"][1]["msg"] == "Ingrese una url valida."
    assert response_data["detail"][2]["loc"][1] == "summary"
    assert response_data["detail"][2]["msg"] == "field required"


def test_update_summary_invalid_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/0/",
        data=json.dumps(
            {
                "url": "https://look.bar",
                "summary": "otr!!!",
            }
        ),
    )
    response_value = response.json()
    assert response.status_code == 422
    assert response_value["detail"][0]["loc"][1] == "id"
    assert response_value["detail"][0]["msg"] == "ensure this value is greater than 0"
    assert response_value["detail"][0]["type"] == "value_error.number.not_gt"


def test_read_summary_invalid_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/0/")
    response_value = response.json()
    assert response.status_code == 422
    assert response_value["detail"][0]["loc"][1] == "id"
    assert response_value["detail"][0]["msg"] == "ensure this value is greater than 0"
    assert response_value["detail"][0]["type"] == "value_error.number.not_gt"


def test_delete_summary_invalid_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/0/")
    response_value = response.json()
    assert response.status_code == 422
    assert response_value["detail"][0]["loc"][1] == "id"
    assert response_value["detail"][0]["msg"] == "ensure this value is greater than 0"
    assert response_value["detail"][0]["type"] == "value_error.number.not_gt"


def test_create_summary_invalid_url(test_app_with_db):
    response = test_app_with_db.post("/summaries/", data=json.dumps({"url": "no-url"}))
    response_value = response.json()
    assert response.status_code == 422
    assert response_value["detail"][0]["loc"][1] == "url"
    assert response_value["detail"][0]["msg"] == "Ingrese una url valida."
