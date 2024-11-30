import typing as T
import logging

from mclib.core.callback.callback_manager.base import BaseCallbackManager

logger = logging.getLogger()


def invoke_callbacks(
    callback_name: str,
    callback_managers: T.List[BaseCallbackManager],
    *args,
    **kwargs,
) -> None:
    for callback_manager in callback_managers:
        if hasattr(callback_manager, callback_name):
            callback_func = getattr(callback_manager, callback_name)
            try:
                callback_func(
                    *args, **kwargs
                )
            except Exception as e:
                logger.exception(
                    f"Exception during Callback Function `{callback_name}` in Callback Manager `{repr(callback_manager)}`: {e}"
                )
        else:
            logger.warning(
                f"Callback Manager `{repr(callback_manager)}` does not implement Callback Function `{callback_name}`"
            )
