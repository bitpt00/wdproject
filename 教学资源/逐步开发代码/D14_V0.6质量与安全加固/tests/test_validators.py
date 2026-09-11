from validators import validate_approval_form, validate_booking_form


def test_booking_validator_returns_clean_data():
    data, errors = validate_booking_form(
        {
            "purpose": " 课程作品展示 ",
            "attendee_count": "20",
            "contact": " 13800000001 ",
        },
        capacity=40,
    )

    assert errors == []
    assert data["purpose"] == "课程作品展示"
    assert data["attendee_count_value"] == 20
    assert data["contact"] == "13800000001"


def test_booking_validator_collects_multiple_errors():
    _, errors = validate_booking_form(
        {"purpose": "短", "attendee_count": "not-a-number", "contact": "1"},
        capacity=40,
    )

    assert len(errors) == 3


def test_approval_validator_requires_rejection_reason():
    decision, comment, errors = validate_approval_form(
        {"decision": "reject", "comment": "无"}
    )

    assert decision == "reject"
    assert comment == "无"
    assert errors == ["驳回时请填写3至300个字的原因。"]


def test_approval_validator_accepts_approval_without_comment():
    decision, comment, errors = validate_approval_form(
        {"decision": "approve", "comment": ""}
    )

    assert decision == "approve"
    assert comment == ""
    assert errors == []
