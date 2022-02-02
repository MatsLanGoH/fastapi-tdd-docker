import json

import pytest  # noqa
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps(
            {"url": "https://foo.bar"},
        ),
    )

    assert response.status_code == HTTP_201_CREATED
    assert response.json()["url"] == "https://foo.bar"


def test_create_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", data=json.dumps({}))

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
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
    # arr
    response = test_app_with_db.post(
        "summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    # act
    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == HTTP_200_OK

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    # act
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db):
    # arr
    response1 = test_app_with_db.post(
        "summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id1 = response1.json()["id"]

    response2 = test_app_with_db.post(
        "summaries/", data=json.dumps({"url": "https://cuddly.bear"})
    )
    summary_id2 = response2.json()["id"]

    # act
    response = test_app_with_db.get("/summaries/")

    # assert
    # TODO: This test needs improvement - we should tear down / drop the table beforehand
    assert response.status_code == HTTP_200_OK
    response_list = response.json()
    assert (
        len(
            list(
                filter(
                    lambda d: d["id"] in [summary_id1, summary_id2],
                    response_list,
                )
            )
        )
        == 2
    )
