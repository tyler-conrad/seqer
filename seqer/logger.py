"""
Logging functionality for classes and module level functions.
"""
from inspect import stack
from inspect import getmodule
from logging import DEBUG
from logging import INFO
from logging import WARNING
from logging import ERROR
from logging import CRITICAL

from twisted.python import log


# https://gist.github.com/techtonik/2151727
def _caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack_list = stack()
    start = 0 + skip
    if len(stack_list) < start + 1:
        return ''
    parentframe = stack_list[start][0]

    name = []
    module = getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)


def log_message(msg, kwargs, level):
    log.msg(_caller_name(skip=3)
            + ': '
            + msg.format(**kwargs),
            logLevel=level)


def debug(msg, **kwargs):
    log_message(msg, kwargs, DEBUG)


def info(msg, **kwargs):
    log_message(msg, kwargs, INFO)


def warn(msg, **kwargs):
    log_message(msg, kwargs, WARNING)


def error(msg, **kwargs):
    log_message(msg, kwargs, ERROR)


def critical(msg, **kwargs):
    log_message(msg, kwargs, CRITICAL)
