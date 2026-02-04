from datetime import datetime, timezone

from nocrm_wrapper.models.lead import Lead


def test_lead_from_dict_parses_dates_and_filters_unknown_fields():
    data = {
        "title": "Deal",
        "status": "new",
        "amount": 10.0,
        "expected_closing_date": "2026-02-01T10:00:00Z",
        "created_at": "2026-02-01T10:00:00Z",
        "updated_at": "2026-02-01T11:00:00Z",
        "unknown": "should-be-ignored",
    }

    lead = Lead.from_dict(data)

    assert lead.title == "Deal"
    assert lead.status == "new"
    assert lead.amount == 10.0

    # parsed as aware datetimes (Z -> +00:00)
    assert lead.expected_closing_date.tzinfo is not None
    assert lead.created_at.tzinfo is not None
    assert lead.updated_at.tzinfo is not None


def test_lead_to_dict_excludes_none_and_readonly_fields():
    lead = Lead(
        title="Deal",
        status="new",
        contact_name=None,
        id=123,
        created_at=datetime(2026, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 2, 1, 11, 0, 0, tzinfo=timezone.utc),
    )

    payload = lead.to_dict()

    assert payload == {"title": "Deal", "status": "new"}
