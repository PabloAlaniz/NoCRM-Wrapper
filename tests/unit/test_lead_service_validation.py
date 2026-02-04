from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from nocrm_wrapper.models.lead import Lead
from nocrm_wrapper.services.lead_service import LeadService
from nocrm_wrapper.exceptions.nocrm_exceptions import NoCRMValidationError


def _service():
    # LeadService only needs a repository for type; validations are sync
    return LeadService(repository=MagicMock())


def test_validate_lead_requires_title_min_length():
    service = _service()
    lead = Lead(title="a", status="new")

    with pytest.raises(NoCRMValidationError):
        service._validate_lead(lead)


def test_validate_lead_rejects_negative_amount():
    service = _service()
    lead = Lead(title="Valid", status="new", amount=-1)

    with pytest.raises(NoCRMValidationError):
        service._validate_lead(lead)


def test_validate_lead_rejects_probability_out_of_range():
    service = _service()
    lead = Lead(title="Valid", status="new", probability=101)

    with pytest.raises(NoCRMValidationError):
        service._validate_lead(lead)


def test_validate_lead_rejects_expected_closing_date_in_past():
    service = _service()
    lead = Lead(
        title="Valid",
        status="new",
        expected_closing_date=datetime.now() - timedelta(days=1),
    )

    with pytest.raises(NoCRMValidationError):
        service._validate_lead(lead)
