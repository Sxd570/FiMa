from functools import wraps
from typing import Any, Callable, TypeVar, cast

from utils.logger import Logger


F = TypeVar("F", bound=Callable[..., Any])


class LoggingMiddleware:
    """
    Logging middleware for MCP tools.

    This logs, to a file and stderr via the shared Logger:
    - user_id (when present in tool parameters)
    - tool name
    - request parameters
    - response payload
    """

    def __init__(self, logger_name: str = __name__):
        self._logger = Logger(logger_name)

    def wrap_tool(self, func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            tool_name = func.__name__
            user_id = kwargs.get("user_id")

            # Log request at info level
            self._logger.info(
                f"MCP tool request | tool={tool_name} | user_id={user_id} "
                f"| params={kwargs!r}"
            )

            try:
                result = func(*args, **kwargs)

                # Derive a loggable response payload
                try:
                    if hasattr(result, "model_dump"):
                        response_payload = result.model_dump()
                    elif hasattr(result, "dict"):
                        response_payload = result.dict()
                    else:
                        response_payload = repr(result)
                except Exception:
                    response_payload = repr(result)

                # Log response at debug level
                self._logger.debug(
                    f"MCP tool response | tool={tool_name} | user_id={user_id} "
                    f"| response={response_payload!r}"
                )

                return result
            except Exception as e:
                # Log errors while preserving stack trace for the caller
                self._logger.error(
                    f"MCP tool error | tool={tool_name} | user_id={user_id} "
                    f"| error={e!r} | params={kwargs!r}"
                )
                raise

        return cast(F, wrapper)

