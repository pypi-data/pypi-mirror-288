from __future__ import annotations

from typing import Optional

from opentelemetry import trace
from opentelemetry.trace import Span, Status, StatusCode
from opentelemetry.trace.propagation import get_current_span
from opentelemetry.util import types

# Use this "magick" name inherited
# from Uptrace https://github.com/uptrace/uptrace-js/blob/master/packages/uptrace-core/src/client.ts#L5
# this way probably Uptrace ignores the Span, but keeps the Exception and makes it prominent
DUMMY_SPAN_NAME = '__dummy__'


def record_exception(exception: BaseException | str,
                     attributes: Optional[types.Attributes] = None,
                     timestamp: Optional[int] = None,
                     escaped: bool = False,
                     span: Span = None) -> None:
    started_span = False
    if not span:
        span = get_current_span()

    if not span or not span.is_recording():
        span = trace.get_tracer('recordException').start_span(DUMMY_SPAN_NAME)
        started_span = True

    if isinstance(exception, BaseException):
        # exception object
        span.record_exception(
            exception=exception, attributes=attributes, timestamp=timestamp, escaped=escaped
        )
    else:
        # exception message as string
        _attributes = {
            'exception.type': 'str',
            'exception.message': str(exception),
            # TODO: Consider if capturing stacktrace is possible and reasonable here
            # "exception.stacktrace": stacktrace,
            'exception.escaped': str(escaped),
        }
        if attributes:
            _attributes.update(attributes)
        span.add_event(
            name='exception', attributes=_attributes, timestamp=timestamp
        )

    span.set_status(Status(StatusCode.ERROR))

    if started_span:
        span.end()
