import logging

import packaging.version
import requests

logger = logging.getLogger("bluequbit-python-sdk")


def check_version(version):
    local_version = packaging.version.parse(version)
    if local_version.is_prerelease:
        logger.warning(
            "Beta version %s of BlueQubit Python SDK is being used.", version
        )
    req = requests.get("https://pypi.python.org/pypi/bluequbit/json", timeout=2.0)
    if not req.ok:
        return

    # find max version on PyPI
    releases = req.json().get("releases", [])
    pip_version = packaging.version.parse("0")
    for release in releases:
        ver = packaging.version.parse(release)
        if not ver.is_prerelease or local_version.is_prerelease:
            pip_version = max(pip_version, ver)

    message = (
        "There is a %s of BlueQubit Python SDK available on PyPI. We"
        " recommend upgrading. Run 'pip install --upgrade bluequbit' to upgrade"
        " from your version %s to %s."
    )
    if pip_version.major > local_version.major:
        logger.warning(message, "major upgrade", local_version, pip_version)
    elif pip_version > local_version:
        logger.info(message, "newer version", local_version, pip_version)
