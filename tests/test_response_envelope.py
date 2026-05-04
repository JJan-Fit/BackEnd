from app.shared.response import ApiError, ApiResponse, fail, ok


def test_ok_wraps_data() -> None:
    response = ok({"id": 1})
    assert response.success is True
    assert response.data == {"id": 1}
    assert response.error is None


def test_ok_with_no_data() -> None:
    response = ok()
    assert response.success is True
    assert response.data is None
    assert response.error is None


def test_fail_wraps_error_with_detail() -> None:
    response = fail("BAD", "잘못됨", detail={"field": "name"})
    assert response.success is False
    assert response.data is None
    assert response.error == ApiError(code="BAD", message="잘못됨", detail={"field": "name"})


def test_serialization_keeps_envelope_keys() -> None:
    dumped = ok({"a": 1}).model_dump()
    assert dumped == {"success": True, "data": {"a": 1}, "error": None}


def test_failure_serialization() -> None:
    dumped = fail("X", "메시지").model_dump()
    assert dumped == {
        "success": False,
        "data": None,
        "error": {"code": "X", "message": "메시지", "detail": None},
    }


def test_generic_typing_does_not_explode() -> None:
    typed: ApiResponse[dict[str, int]] = ok({"n": 42})
    assert typed.data == {"n": 42}
