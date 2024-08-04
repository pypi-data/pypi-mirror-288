import os
from typing import Optional
from urllib.parse import urlparse, urlunparse, urljoin

from requests import Session

from oli.tracing.tracing import TracingCollector


def _clean_url(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("URL must start with 'http://' or 'https://'")
    # remove any path in the url
    parsed_url = urlparse(url)
    cleaned_url = (
        urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", "")) + "/"
    )
    return cleaned_url


def ensure_value(value: Optional[str], env_var: str) -> str:
    if value:
        return value
    if not (env_value := os.getenv(env_var)):
        raise ValueError(
            f"Environment variable {env_var} is not set and no value provided."
        )
    return env_value


class OliTracing:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        endpoint_url = ensure_value(endpoint_url, "OLI_TRACING_ENDPOINT_URL")
        client_id = ensure_value(client_id, "OLI_TRACING_CLIENT_ID")
        client_secret = ensure_value(client_secret, "OLI_TRACING_CLIENT_SECRET")
        self.endpoint_url = _clean_url(endpoint_url)
        self._client_id = client_id
        self._client_secret = client_secret
        self._setup_client()
        self._session = Session()
        self._session.headers.update(self.auth_headers)

    @property
    def auth_headers(self):
        return {
            "CF-Access-Client-Id": self._client_id,
            "CF-Access-Client-Secret": self._client_secret,
        }

    @property
    def tracing_endpoint_url(self):
        return urljoin(self.endpoint_url, "/v1/traces")

    def is_available(self):
        health_url = urljoin(self.endpoint_url, "/arize_phoenix_version")
        response = self._session.get(health_url)
        if response.status_code == 200:
            print(f"Connected to Active Tracing Server; Version: {response.text}")
            return True
        return False

    def _setup_client(self):
        os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = self.endpoint_url
        os.environ["PHOENIX_CLIENT_HEADERS"] = ",".join(
            f"{k}={v}" for k, v in self.auth_headers.items()
        )

    def setup_collector(
        self,
        project_name: Optional[str] = None,
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        log_to_console: bool = False,
        use_batch_processor: bool = True,
    ) -> TracingCollector:
        project_name = ensure_value(project_name, "OLI_TRACING_PROJECT_NAME")
        collector = TracingCollector(
            tracing_client=self,
            project_name=project_name,
            model_id=model_id,
            model_version=model_version,
            log_to_console=log_to_console,
            use_batch_processor=use_batch_processor,
        )
        collector.setup()
        return collector
