"""Console script for test."""

import logging

import click
import click_output_formatter
import hwinf_ci_logging
from error_value import Error
from opentelemetry.instrumentation.nv_click import ClickInstrumentor

# Auto-instrument OTEL tracing
if not ClickInstrumentor().is_instrumented_by_opentelemetry:
    ClickInstrumentor().instrument()


@click.group()
@click_output_formatter.json_option()
@hwinf_ci_logging.standard_logging
@click.version_option()
def cli(json: bool) -> None:
    """General description goes here."""
    pass


cli.result_callback()(click_output_formatter.output_result_formatter)


@cli.command()
@click_output_formatter.add_formatter(lambda x: repr(x))
def fail() -> Error:
    """This command is an error."""
    logging.debug("This is an error")
    return Error("This is an error")


@cli.command()
@click_output_formatter.add_formatter(lambda x: repr(x))
def pass1() -> dict:
    """This command is a passing command."""
    logging.debug("This is a passing command")
    return {"exit_code": 0, "message": "test"}
