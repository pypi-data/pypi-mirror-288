# Mypy; for the `|` operator purpose
# Remove this __future__ import once the oldest supported Python is 3.10
from __future__ import annotations

import contextlib
import logging

from . import exceptions, job_metadata_constants
from .bluequbit_client import BQClient
from .estimate_result import EstimateResult
from .job_result import JobResult

with contextlib.suppress(ImportError):
    from .qiskit_provider import BlueQubitProvider
from .version import __version__

__all__ = [
    "exceptions",
    "job_metadata_constants",
    "BQClient",
    "EstimateResult",
    "JobResult",
    "__version__",
    "BlueQubitProvider",
]

formatter = logging.Formatter(fmt="BQ-PYTHON-SDK - %(levelname)s - %(message)s")
# formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("bluequbit-python-sdk")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def init(api_token: str | None = None) -> BQClient:
    """Returns :class:`BQClient` instance for managing jobs on BlueQubit platform.

    :param api_token: API token of the user. If ``None``, the token will be looked
                      in the environment variable BLUEQUBIT_API_TOKEN.
    """
    return BQClient(api_token)
