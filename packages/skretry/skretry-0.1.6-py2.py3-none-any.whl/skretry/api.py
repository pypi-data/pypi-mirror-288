import asyncio
from loguru import logger as lg
import random
import time
import traceback
from functools import partial

import inspect

from .compat import decorator

logging_logger = lg


def __retry_internal(
        f,
        exceptions=Exception,
        tries=-1,
        delay=0,
        max_delay=None,
        backoff=1,
        jitter=0,
        show_traceback=False,
        logger=logging_logger,
        fail_callback=None,
):
    _tries, _delay = tries, delay

    while _tries:
        try:
            return f()

        except exceptions as e:
            _tries -= 1

            if logger:
                _log_attempt(tries, show_traceback, logger, _tries, _delay, e, f.__name__)

            if not _tries:
                raise

            if fail_callback is not None:
                fail_callback(e)

            time.sleep(_delay)

            _delay = _new_delay(max_delay, backoff, jitter, _delay)


async def __retry_internal_async(
        f,
        exceptions=Exception,
        tries=-1,
        delay=0,
        max_delay=None,
        backoff=1,
        jitter=0,
        show_traceback=False,
        logger=logging_logger,
        fail_callback=None,
):
    _tries, _delay = tries, delay

    while _tries:
        try:
            return await f()

        except exceptions as e:
            _tries -= 1

            if logger:
                _log_attempt(tries, show_traceback, logger, _tries, _delay, e, f.__name__)

            if not _tries:
                raise

            if fail_callback is not None:
                await fail_callback(e)

            await asyncio.sleep(_delay)

            _delay = _new_delay(max_delay, backoff, jitter, _delay)


def _log_attempt(tries, show_traceback, logger, _tries, _delay, e, func_name):
    logger = logger.opt(depth=5).patch(
        lambda record: record.update(line=e.__traceback__.tb_next.tb_lineno, function=func_name))

    if _tries:
        if show_traceback:
            tb_str = "".join(traceback.format_exception(None, e, e.__traceback__))
            logger.error(tb_str)

        logger.error(
            f"{e}, attempt {tries - _tries}/{tries} failed - retrying in {_delay} seconds..."
        )

    elif tries > 1:
        logger.error(
            f"{e}, attempt {tries - _tries}/{tries} failed - giving up!"
        )


def _new_delay(max_delay, backoff, jitter, _delay):
    _delay *= backoff
    _delay += random.uniform(*jitter) if isinstance(jitter, tuple) else jitter

    if max_delay is not None:
        _delay = min(_delay, max_delay)

    return _delay


def _is_async(f):
    return asyncio.iscoroutinefunction(f) and not inspect.isgeneratorfunction(f)


def _get_internal_function(f):
    return __retry_internal_async if _is_async(f) else __retry_internal


def _check_params(f, show_traceback=False, logger=logging_logger, fail_callback=None):
    assert not show_traceback or logger is not None, "`show_traceback` needs `logger`"

    assert not fail_callback or (
            (_is_async(f) and _is_async(fail_callback))
            or (not _is_async(f) and not _is_async(fail_callback))
    ), "If the retried function is async, fail_callback needs to be async as well or vice versa"


def retry(
        exceptions=Exception,
        tries=-1,
        delay=0,
        max_delay=None,
        backoff=1,
        jitter=0,
        show_traceback=False,
        logger=logging_logger,
        fail_callback=None,
):
    """Returns a retry decorator.

    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts (in seconds). default: 0.
    :param max_delay: the maximum value of delay (in seconds). default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param show_traceback: if True, the traceback of the exception will be logged.
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param fail_callback: fail_callback(e) will be called on failed attempts.
    :returns: a retry decorator.
    """

    @decorator
    def retry_decorator(f, *fargs, **fkwargs):
        return retry_call(
            f,
            fargs,
            fkwargs,
            exceptions,
            tries,
            delay,
            max_delay,
            backoff,
            jitter,
            show_traceback,
            logger,
            fail_callback,
        )

    return retry_decorator


def retry_call(
        f,
        fargs=None,
        fkwargs=None,
        exceptions=Exception,
        tries=-1,
        delay=0,
        max_delay=None,
        backoff=1,
        jitter=0,
        show_traceback=False,
        logger=logging_logger,
        fail_callback=None,
):
    """
    Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts (in seconds). default: 0.
    :param max_delay: the maximum value of delay (in seconds). default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param show_traceback: if True, the traceback of the exception will be logged.
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param fail_callback: fail_callback(e) will be called on failed attempts.
    :returns: the result of the f function.
    """
    args = fargs or list()
    kwargs = fkwargs or dict()

    _check_params(f, show_traceback, logger, fail_callback)
    func = _get_internal_function(f)
    p = partial(f, *args, **kwargs)
    p.__name__ = f.__name__

    return func(
        p,
        exceptions,
        tries,
        delay,
        max_delay,
        backoff,
        jitter,
        show_traceback,
        logger,
        fail_callback,
    )
