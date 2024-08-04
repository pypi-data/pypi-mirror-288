import os
import typing
from typing import Optional

from openinference.semconv.resource import ResourceAttributes
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HttpSpanExporter,
)
from opentelemetry.sdk.trace import Resource, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)

if typing.TYPE_CHECKING:
    # avoid circular import
    from oli.tracing import OliTracing


def _create_resource(
    model_id: str,
    model_version: str,
    project_name: str,
) -> Resource:
    attributes = {}
    if model_id:
        attributes["model_id"] = model_id
    if model_version:
        attributes["model_version"] = model_version
    if project_name:
        attributes[ResourceAttributes.PROJECT_NAME] = project_name
    return Resource(attributes=attributes)


def _ensure_proper_url(url: str) -> str:
    # parse url and ensure the path is /v1/traces
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("URL must start with 'http://' or 'https://'")
    if not url.endswith("/v1/traces") and not url.endswith("/v1/traces/"):
        return url.rstrip("/") + "/v1/traces"
    return url


class TracingCollector:
    def __init__(
        self,
        tracing_client: "OliTracing",
        project_name: str,
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        log_to_console: bool = False,
        use_batch_processor: bool = True,
        use_global_tracer_provider: bool = True,
    ):
        if os.environ.get("OLI_TRACING_USE_GLOBAL_PROVIDER") is None:
            self.use_global_tracer_provider = use_global_tracer_provider
        else:
            self.use_global_tracer_provider = (
                os.environ.get("OLI_TRACING_USE_GLOBAL_PROVIDER").lower() == "true"
            )
        self.tracing_client: "OliTracing" = tracing_client
        self.project_name = project_name
        self.model_id = model_id
        self.model_version = model_version
        self.log_to_console = log_to_console
        self.use_batch_processor = use_batch_processor
        self._setup = False
        self._tracer_provider = None

    def setup(self):
        if not isinstance(self.use_batch_processor, bool):
            raise TypeError("use_batch_processor must be of type bool")
        provider = TracerProvider(
            resource=_create_resource(
                self.model_id,
                self.model_version,
                self.project_name,
            )
        )
        processor = (
            BatchSpanProcessor if self.use_batch_processor else SimpleSpanProcessor
        )
        exporter = HttpSpanExporter
        ep = _ensure_proper_url(self.tracing_client.tracing_endpoint_url)
        provider.add_span_processor(
            span_processor=processor(
                span_exporter=exporter(
                    endpoint=ep,
                    headers=self.tracing_client.auth_headers,
                ),
            )
        )
        if self.log_to_console:
            provider.add_span_processor(
                span_processor=processor(
                    span_exporter=ConsoleSpanExporter(),
                )
            )
        self._tracer_provider = provider
        if self.use_global_tracer_provider is True:
            trace.set_tracer_provider(tracer_provider=provider)
        self._setup = True

    @property
    def tracer_provider(self):
        return self._tracer_provider

    def enable_openai_tracing(self):
        if not self._setup:
            raise RuntimeError("Tracing must be setup before calling this function")
        from openinference.instrumentation.openai import OpenAIInstrumentor

        OpenAIInstrumentor().instrument(tracer_provider=self._tracer_provider)
        return self

    def enable_dspy_tracing(self):
        if not self._setup:
            raise RuntimeError("Tracing must be setup before calling this function")
        from openinference.instrumentation.dspy import DSPyInstrumentor

        DSPyInstrumentor().instrument(tracer_provider=self._tracer_provider)
        return self

    def enable_langchain_tracing(self):
        if not self._setup:
            raise RuntimeError("Tracing must be setup before calling this function")
        from openinference.instrumentation.langchain import LangChainInstrumentor

        LangChainInstrumentor().instrument(tracer_provider=self._tracer_provider)
        return self
