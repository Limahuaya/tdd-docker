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
        data=json.dumps({
            "url": "https://foomodif.bar", 
            "summary": "updated!!"
        })
    )
    assert response.status_code == 200
    assert response.json() == {'url': 'https://foomodif.bar', 'summary': 'updated!!', 'id': summary_id}


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999999999/", 
        data=json.dumps({"url": "https://foomodif.bar", "summary": "updated!!"})
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
        data='''{
            "url": "https://foomodif.bar", 
            "summar": "updat
        }'''
    )
   
    assert response.status_code == 422
    assert response.json() == {
        "detail":[
            {
                "loc":[
                    "body",
                    74
                ],
                "msg":"Invalid control character at: line 3 column 29 (char 74)",
                "type":"value_error.jsondecode",
                "ctx":{
                    "msg":"Invalid control character at",
                    "doc":"{\n            \"url\": \"https://foomodif.bar\", \n            \"summar\": \"updat\n        }",
                    "pos":74,
                    "lineno":3,
                    "colno":29
                }
            }
        ]
    }


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/${summary_id}/", 
        data=json.dumps({
            "url": "no-url",
            "summar": "otr!!!",
        })
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail":[
            {
                "loc":[
                    "path",
                    "id"
                ],
                "msg":"value is not a valid integer",
                "type":"type_error.integer"
            },
            {
                "loc":[
                    "body",
                    "url"
                ],
                "msg":"Ingrese una url valida.",
                "type":"value_error"
            },
            {
                "loc":[
                    "body",
                    "summary"
                ],
                "msg":"field required",
                "type":"value_error.missing"
            }
        ]
    }