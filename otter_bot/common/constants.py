import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()

COMMAND_PREFIX = '!'
SUDO_CHANNEL_ID: int = int(os.environ["SUDO_CHANNEL_ID"])

def extract_company_names(allowed_companies_info: list[list[str]]) -> list[str]:
    """
    Extract company names from the given information.
    Returns a list of names.
    """

    companies = [company[0] for company in allowed_companies_info if company]
    companies_set = set(companies)

    return companies_set