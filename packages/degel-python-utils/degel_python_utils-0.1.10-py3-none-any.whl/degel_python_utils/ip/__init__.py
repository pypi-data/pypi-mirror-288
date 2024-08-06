"""
Utilities for parsing and reading patent applications and grants.

Includes support for the USPTO and patent-client API, each of which has strengths
and weaknesses.
"""

import re


def parse_extended_patent_number(patent_number_string: str) -> dict[str, str | None]:
    """
    Parse an extended patent number string into its components.

    Args:
        patent_number_string (str): The extended patent number string to parse.

    Returns:
        dict: Contains parsed components: type_of_citation, country, number_type,
              application_number, and grant_number.
    """
    match = pattern.search(patent_number_string)

    if match:
        country_code = match.group(1)
        patent_number = match.group(2).replace("-", "").replace("/", "")
        kind_code = match.group(3)

        country = country_code[:2] if country_code else ""
        type_of_citation = "Patent"

        if kind_code:
            number_type = "Application" if kind_code[0] == "A" else "Grant"
        else:
            number_type = "Grant" if len(patent_number) <= 8 else "Application"
        if number_type == "Application" and not kind_code:
            kind_code = "A1"

        application_number = patent_number if number_type == "Application" else None
        grant_number = patent_number if number_type == "Grant" else None

    else:
        type_of_citation = "NPL"
        country = None
        number_type = None
        kind_code = None
        application_number = None
        grant_number = None

    return {
        "type_of_citation": type_of_citation,
        "country": country,
        "number_type": number_type,
        "kind_code": kind_code,
        "application_number": application_number,
        "grant_number": grant_number,
    }


# Define the regex pattern for parsing patent numbers
pattern = re.compile(
    r"""
    (?<!\w)            # Match starts at BOS or after non-alphanumeric
    ([A-Z]{1,3})?      # Optional country code
    [\s\-_]*           # Optional separator (whitespace, hyphen, or underscore)
    (\d{4}[-/]?\d{3,}) # Mandatory patent number; may have separator after year
    [\s\-_]*           # Optional separator (whitespace, hyphen, or underscore)
    ([AB]\d?(?![\w]))? # Optional code: 'A' or 'B', optionally followed by a digit
    """,
    re.VERBOSE,
)
