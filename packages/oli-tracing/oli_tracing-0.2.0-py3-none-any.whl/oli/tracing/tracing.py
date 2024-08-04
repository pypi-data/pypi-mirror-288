import functools
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

# Global variable to track if a tracer is registered
_tracer_registered = False


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


def setup_oli_tracing(
    endpoint_url: str,
    project_name: str,
    client_id: str,
    client_secret: str,
    model_id: Optional[str] = None,
    model_version: Optional[str] = None,
    log_to_console: bool = False,
    use_batch_processor: bool = True,
) -> None:
    """
    Sets up a `TracerProvider` with the corresponding `Resource` and with
    multiple, if appropriate, `SimpleSpanProcessor`s.
    Each `SimpleSpanProcessor` (one per endpoint) is provided with an `OTLPSpanExporter`
    pointing to the corresponding endpoint.

    Parameters:
    -----------
        environment(str): The environment to send traces to. It can be either "dev" or "prod".
        project_name(str): This is Phoenix specific. A project is a collection of
            traces that are related to a single application or service. You can have
            multiple projects, each with multiple traces.
        client_id(str): This is Oli specific. The client ID is necessary for
            authentication when sending traces to Oli Hosted Phoenix Server.
        client_secret(str): This is Oli specific. The client secret is necessary for
            authentication when sending traces to Oli Hosted Phoenix Server.
        model_id(str, optional): This is Arize specific. The model ID is a unique name
            to identify your model in the Arize platform. Defaults to None.
        model_version(str, optional): This is Arize specific. The model version is
            used to group a subset of data, given the same model ID,
            to compare and track changes. Defaults to None.
        log_to_console(bool, optional): Enable this option while developing so the
            spans are printed in the console. Defaults to False.
        use_batch_processor(bool, optional): Enable this option to use
            `BatchSpanProcessor` instead of the default `SimpleSpanProcessor`.
            Defaults to False.

    Returns:
    --------
        None
    """
    global _tracer_registered
    if _tracer_registered:
        return
    if not isinstance(use_batch_processor, bool):
        raise TypeError("use_batch_processor must be of type bool")
    provider = TracerProvider(
        resource=_create_resource(
            model_id,
            model_version,
            project_name,
        )
    )
    processor = BatchSpanProcessor if use_batch_processor else SimpleSpanProcessor
    exporter = HttpSpanExporter
    ep = _ensure_proper_url(endpoint_url)
    provider.add_span_processor(
        span_processor=processor(
            span_exporter=exporter(
                endpoint=ep,
                headers={
                    "CF-Access-Client-Id": client_id,
                    "CF-Access-Client-Secret": client_secret,
                },
            ),
        )
    )
    if log_to_console:
        provider.add_span_processor(
            span_processor=processor(
                span_exporter=ConsoleSpanExporter(),
            )
        )
    trace.set_tracer_provider(tracer_provider=provider)
    _tracer_registered = True


def tracer_exists(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _tracer_registered:
            raise RuntimeError("Tracer must be registered before calling this function")
        return func(*args, **kwargs)

    return wrapper


@tracer_exists
def enable_openai_tracing():
    from openinference.instrumentation.openai import OpenAIInstrumentor

    OpenAIInstrumentor().instrument()


@tracer_exists
def enable_dspy_tracing():
    from openinference.instrumentation.dspy import DSPyInstrumentor

    DSPyInstrumentor().instrument()


@tracer_exists
def enable_langchain_tracing():
    from openinference.instrumentation.langchain import LangChainInstrumentor

    LangChainInstrumentor().instrument()
