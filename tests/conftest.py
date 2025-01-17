import pytest
import os
from dotenv import load_dotenv
from nocrm_wrapper.config import NoCRMConfig
from nocrm_wrapper.repositories import LeadRepository


@pytest.fixture(scope="session")
def config():
    load_dotenv()
    api_key = os.getenv("NOCRM_API_KEY")
    subdomain = os.getenv("NOCRM_SUBDOMAIN")
    user_id = os.getenv("NOCRM_USER_ID")

    if not all([api_key, subdomain, user_id]):
        pytest.skip("Faltan variables de entorno requeridas")

    return NoCRMConfig(api_key=api_key, subdomain=subdomain)


@pytest.fixture(scope="session")
def user_id():
    return int(os.getenv("NOCRM_USER_ID"))


@pytest.fixture
def lead_repository(config):
    return LeadRepository(config)