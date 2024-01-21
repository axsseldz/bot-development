
COMMAND_PREFIX = '!'

def extract_company_names(allowed_companies_info: list[list[str]]) -> list[str]:
    """
    Extract company names from the given information.
    Returns a list of names.
    """

    companies = [company[0] for company in allowed_companies_info if company]
    companies_set = set(companies)

    return companies_set