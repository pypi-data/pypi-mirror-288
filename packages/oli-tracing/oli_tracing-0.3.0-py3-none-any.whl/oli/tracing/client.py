import os
from urllib.parse import urlparse, urlunparse


def _clean_url(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("URL must start with 'http://' or 'https://'")
    # remove any path in the url
    parsed_url = urlparse(url)
    cleaned_url = (
        urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", "")) + "/"
    )
    return cleaned_url


def setup_oli_tracing_client(
    endpoint_url: str,
    client_id: str,
    client_secret: str,
) -> None:
    endpoint_url = _clean_url(endpoint_url)
    auth_headers = {
        "CF-Access-Client-Id": client_id,
        "CF-Access-Client-Secret": client_secret,
    }
    os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = endpoint_url
    os.environ["PHOENIX_CLIENT_HEADERS"] = ",".join(
        f"{k}={v}" for k, v in auth_headers.items()
    )
