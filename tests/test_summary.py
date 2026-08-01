def test_empty_data_object(post_summary):
    status, body = post_summary({"data": {}})

    assert status == 200
    assert body["summary"] == "No data was provided."


def test_single_attribute(post_summary):
    status, body = post_summary({"data": {"projects": 5}})

    assert status == 200
    assert body["summary"] == "There are 5 projects."


def test_two_attributes(post_summary):
    status, body = post_summary({"data": {"projects": 5, "workspaces": 2}})

    assert status == 200
    assert body["summary"] == "There are 5 projects and 2 workspaces."


def test_three_attributes_uses_comma_and_and(post_summary):
    status, body = post_summary({"data": {"projects": 5, "workspaces": 2, "teams": 1}})

    assert status == 200
    assert body["summary"] == "There are 5 projects, 2 workspaces and 1 teams."


def test_zero_counts_are_allowed(post_summary):
    status, body = post_summary({"data": {"projects": 0, "workspaces": 0}})

    assert status == 200
    assert body["summary"] == "There are 0 projects and 0 workspaces."


def test_preserves_attribute_insertion_order(post_summary):
    status, body = post_summary({"data": {"zebra": 1, "apple": 2}})

    assert status == 200
    assert body["summary"] == "There are 1 zebra and 2 apple."


def test_missing_data_key_returns_400(post_summary):
    status, body = post_summary({})

    assert status == 400
    assert body["error"] == "Invalid request"
    assert "non-negative integer counts" in body["message"]


def test_negative_count_returns_400(post_summary):
    status, body = post_summary({"data": {"projects": -1}})

    assert status == 400
    assert body["error"] == "Invalid request"


def test_string_value_returns_400(post_summary):
    status, body = post_summary({"data": {"projects": "five"}})

    assert status == 400
    assert body["error"] == "Invalid request"


def test_nested_object_value_returns_400(post_summary):
    status, body = post_summary({"data": {"projects": {"count": 5}}})

    assert status == 400
    assert body["error"] == "Invalid request"


def test_array_value_returns_400(post_summary):
    status, body = post_summary({"data": {"projects": [5]}})

    assert status == 400
    assert body["error"] == "Invalid request"


def test_data_must_be_an_object(post_summary):
    status, body = post_summary({"data": ["projects", 5]})

    assert status == 400
    assert body["error"] == "Invalid request"


def test_non_json_object_body_returns_400(post_summary):
    status, body = post_summary(["not", "an", "object"])

    assert status == 400
    assert body["error"] == "Invalid request"


def test_float_count_returns_400(post_summary):
    status, body = post_summary({"data": {"projects": 1.5}})

    assert status == 400
    assert body["error"] == "Invalid request"
