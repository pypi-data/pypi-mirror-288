from typing import Optional

import click
import requests
from semver import VersionInfo

from vgscli.text import bold, green

__version__ = ""
print("version", __version__)


# noinspection PyBroadException
def get_latest_version(**kwargs) -> Optional[VersionInfo]:
    try:
        response_json = requests.get(
            "https://pypi.org/pypi/vgs-cli/json", **kwargs
        ).json()
        print("latest version response", VersionInfo.parse(response_json["info"]["version"]))
        return VersionInfo.parse(response_json["info"]["version"])
    except Exception:
        return None


def check_for_updates() -> None:
    latest_version = get_latest_version(timeout=2)
    print("latest_version", latest_version)

    if latest_version and latest_version > __version__:
        message = f"CLI update available from {bold(green(__version__))} to {bold(green(str(latest_version)))}."
        print(message)
        click.echo(message, err=True)


def version():
    return __version__
