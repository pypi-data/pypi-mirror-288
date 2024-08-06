"""Patent API using patent-client library.

This wraps the USPTO and EPO patent APIs, and seems to be very powerful and
well-maintained.

Ideally, this could become our patent API of choice, but I've not yet fully grokked how
to use it optimally.
"""

import asyncio

from patent_client._async import Patent

from degel_python_utils.sys_utils.errors import ExternalApiError
from degel_python_utils.sys_utils.log_tools import setup_logger

logger = setup_logger(__name__)
# pylint: disable=logging-fstring-interpolation


MAX_RETRIES = 5
BACKOFF_FACTOR = 1.0


async def fetch_us_patent_grant_from_pclient(
    patent_number: str, log_prefix: str | None
) -> dict:
    """
    Fetch a granted US patent using the patent-client library.

    :param patent_number: The patent number to fetch.
    :param log_prefix: Request identifier, for clarity in log messages.
    :return: A dictionary containing the patent application details.
    :raises ExternalApiError: If the patent-client API request fails.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            patent = await Patent.objects.get(  # pylint: disable=no-member
                patent_number
            )
            return patent
        except Exception as err:  # pylint: disable=broad-except
            if retries < MAX_RETRIES - 1:
                backoff_time = BACKOFF_FACTOR * (2**retries)
                logger.warning(
                    f"Retrying {log_prefix} after {backoff_time}s due to error: {err}"
                )
                await asyncio.sleep(backoff_time)
                retries += 1
            else:
                logger.error(
                    f"Failed to fetch patent {patent_number} ({MAX_RETRIES} attempts)."
                )
                raise ExternalApiError(
                    "patent-client request failed on "
                    f"{log_prefix} after {MAX_RETRIES} attempts"
                ) from err
    # This line is unreachable, but added to satisfy mypy's requirement
    raise ExternalApiError(
        f"{log_prefix} Unhandled error fetching patent {patent_number}"
    )
