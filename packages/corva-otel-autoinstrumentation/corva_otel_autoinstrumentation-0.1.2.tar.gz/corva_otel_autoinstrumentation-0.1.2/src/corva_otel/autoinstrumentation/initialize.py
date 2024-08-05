from os import environ, getcwd, pathsep
from os.path import abspath, dirname
import opentelemetry.instrumentation.auto_instrumentation

# This file makes it easy to integrate and initiate OTel SDK via code, similar to how it is done in other languages.
# This way:
#   - it works for different implementations of FaaS (AWS Lambda, OpenFaaS, whatever next ...)
#   - it is a concern of Code Owners not DevOps if and how the code is instrumented, so
#     no Docker / K8S / Command / Scripts need changing, everything works
#     from well-known env vars https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/
#   - it works for multi-workers / threads like `gunicorn`, `uvicorn` etc.
#     cases https://github.com/open-telemetry/opentelemetry-python/issues/3573#issuecomment-1962853105
#
# Sadly OpenTelemetry Python have deviated from all other implementations providing this `opentelemetry-instrument` app
# see https://opentelemetry.io/docs/languages/python/getting-started/#run-the-instrumented-app
# so we need our own implementation

# Optionally initialize OTel, by importing this file first
if environ.get('OTEL_SDK_DISABLED') != 'true':
    # Instrument packages through prefixed `PYTHONPATH` that includes instrumented packages first
    python_path = environ.get('PYTHONPATH')

    if not python_path:
        python_path = []

    else:
        python_path = python_path.split(pathsep)

    cwd_path = getcwd()

    # This is being added to support applications that are being run from their
    # own executable, like Django.
    # FIXME investigate if there is another way to achieve this
    if cwd_path not in python_path:
        python_path.insert(0, cwd_path)

    filedir_path = dirname(abspath(opentelemetry.instrumentation.auto_instrumentation.__file__))

    python_path = [path for path in python_path if path != filedir_path]

    python_path.insert(0, filedir_path)

    environ['PYTHONPATH'] = pathsep.join(python_path)

    # Setup Pymongo instrumentation if available
    # NOTE: Triggers warning `Attempting to instrument while already instrumented`, that is harmless in this case
    try:
        from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

        PymongoInstrumentor().instrument(capture_statement=True)
    except ImportError:
        PymongoInstrumentor = None

    # Initialize OTel components via ENV variables
    # (tracer provider, meter provider, logger provider, processors, exporters, etc.)
    from opentelemetry.instrumentation.auto_instrumentation import (  # noqa: F401 I001
        sitecustomize,
    )
