import json
import logging
from datetime import datetime, timedelta
from flask import Flask, Response, request, send_file
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL  # 0, 10, 20, 30, 40, 50
from io import BytesIO
from pathlib import Path
from pypomes_core import (
    APP_PREFIX, DATETIME_FORMAT_INV, TEMP_FOLDER, DATETIME_FORMAT_COMPACT,
    env_get_str, env_get_path, datetime_parse, str_get_positional
)
from pypomes_http import http_get_parameters
from typing import Any, Final, Literal, TextIO

LOGGING_DEFAULT_STYLE: Final[str] = ("{asctime} {levelname:1.1} {thread:5d} "
                                     "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
LOGGING_ID: str | None = None
LOGGING_LEVEL: int | None = None
LOGGING_FORMAT: str | None = None
LOGGING_STYLE: str | None = None
LOGGING_FILE_PATH: str | None = None
LOGGING_FILE_MODE: str | None = None
PYPOMES_LOGGER: logging.Logger | None = None


def logging_startup(scheme: dict[str, Any] = None,
                    flask_app: Flask = None) -> None:
    """
    Start or re-start the log service.

    The parameters for starting the log can be found either as environment variables, or as
    attributes in *scheme*. Default values are used, if necessary.

    :param scheme: optional roll of log parameters and corresponding values
    :param flask_app: the *Flask* application object
    """
    scheme = scheme or {}

    # establish configuration attributes
    global LOGGING_ID
    LOGGING_ID = scheme.get("log-id",
                            env_get_str(key=f"{APP_PREFIX}_LOGGING_ID",
                                        def_value=f"{APP_PREFIX}"))
    global LOGGING_LEVEL
    # noinspection PyTypeChecker
    LOGGING_LEVEL = __get_logging_level(level=scheme.get("log-level",
                                                         env_get_str(key=f"{APP_PREFIX}_LOGGING_LEVEL",
                                                                     def_value="info").lower()))
    global LOGGING_FORMAT
    LOGGING_FORMAT= scheme.get("log-format",
                               env_get_str(key=f"{APP_PREFIX}_LOGGING_FORMAT",
                                           def_value=LOGGING_DEFAULT_STYLE))
    global LOGGING_STYLE
    LOGGING_STYLE = scheme.get("log-style",
                               env_get_str(key=f"{APP_PREFIX}_LOGGING_STYLE",
                                           def_value="{"))
    global LOGGING_FILE_PATH
    LOGGING_FILE_PATH = env_get_path(scheme.get("log-file-path",
                                                f"{APP_PREFIX}_LOGGING_FILE_PATH"),
                                     def_value=TEMP_FOLDER / f"{APP_PREFIX}.log")
    global LOGGING_FILE_MODE
    LOGGING_FILE_MODE = scheme.get("log-file-mode",
                                   env_get_str(key=f"{APP_PREFIX}_LOGGING_FILE_MODE",
                                               def_value="a"))
    global PYPOMES_LOGGER
    # is there a logger ?
    if PYPOMES_LOGGER:
        # yes, shut it down
        logging.shutdown()

    # start the logger
    PYPOMES_LOGGER = logging.getLogger(name=LOGGING_ID)

    # configure the logger
    # noinspection PyTypeChecker
    logging.basicConfig(filename=LOGGING_FILE_PATH,
                        filemode=LOGGING_FILE_MODE,
                        format=LOGGING_FORMAT,
                        datefmt=DATETIME_FORMAT_INV,
                        style=LOGGING_STYLE,
                        level=LOGGING_LEVEL)
    for _handler in logging.root.handlers:
        _handler.addFilter(filter=logging.Filter(LOGGING_ID))

    # establish the logging service endpoint
    if flask_app:
        flask_app.add_url_rule(rule="/logging",
                               endpoint="logging",
                               view_func=logging_service,
                               methods=["GET", "POST"])


def logging_get_entries(errors: list[str],
                        log_level: int = None,
                        log_from: datetime = None,
                        log_to: datetime = None) -> BytesIO:
    """
    Extract and return entries in the logging file *log_path*.

    It is expected for this logging file to be compliant with *PYPOMES_LOGGER*'s *LOGGING_DEFAULT_STYLE*.
    The extraction meets the criteria specified by *log_level*, and by the inclusive interval *[log_from, log_to]*.

    :param errors: incidental error messages
    :param log_level: the logging level (defaults to all levels)
    :param log_from: the initial timestamp (defaults to unspecified)
    :param log_to: the finaL timestamp (defaults to unspecified)
    :return: the logging entries meeting the specified criteria
    """
    # initialize the return variable
    result: BytesIO | None = None

    # verify whether inspecting the log entries is possible
    if LOGGING_STYLE != LOGGING_DEFAULT_STYLE and \
       (log_level or log_from or log_to):
        errors.append("It is not possible to apply level "
                      "or timestamp criteria to filter log entries")
    # errors ?
    if not errors:
        # no, proceed
        result = BytesIO()
        filepath: Path = Path(LOGGING_FILE_PATH)
        with (filepath.open() as f):
            line: str = f.readline()
            while line:
                items: list[str] = line.split(sep=None,
                                              maxsplit=3)
                # noinspection PyTypeChecker
                msg_level: int = CRITICAL if not log_level or len(items) < 2 \
                                 else __get_logging_level(level=items[2].lower())
                # 'not log_level' works for both values 'NOTSET' and 'None'
                if not log_level or msg_level >= log_level:
                    if len(items) > 1 and (log_from or log_to):
                        timestamp: datetime = datetime_parse(f"{items[0]} {items[1]}")
                        if not timestamp or \
                           ((not log_from or timestamp >= log_from) and
                            (not log_to or timestamp <= log_to)):
                            result.write(line.encode())
                    else:
                        result.write(line.encode())
                line = f.readline()

    return result


def logging_send_entries(scheme: dict[str, Any]) -> Response:
    """
    Retrieve from the log file, and send in response, the entries matching the criteria specified.

    These parameters, used to filter the records to be returned, are specified according to the pattern
    *attach=<[t,true,f,false]>&log-level=<notset|debug|info|warning|error|critical>&
    log-from-datetime=YYYYMMDDhhmmss&log-to-datetime=YYYYMMDDhhmmss&log-last-days=<n>&log-last-hours=<n>>*:
        - *log-attach*: whether browser should display or persist file (defaults to True - persist it)
        - *log-level*: the logging level of the entries (defaults to *notset*, meaning all levels:)
        - *log-from-datetime*: the start timestamp
        - log-to-datetime*: the finish timestamp
        - *log-last-days*: how many days before current date
        - *log-last-hours*: how may hours before current time

    :param scheme: the criteria for filtering the records to be returned
    :return: file containing the log entries requested on success, or incidental errors on fail
    """
    # declare the return variable
    result: Response

    # initialize the error messages list
    errors: list[str] = []

    # obtain the logging level
    log_level: int = str_get_positional(source=scheme.get("level", "N")[:1].upper(),
                                        list_origin=["N", "D", "I", "W", "E", "C"],
                                        list_dest=[0, 10, 20, 30, 40, 50])

    # obtain the initial and final timestamps
    log_from: datetime = datetime_parse(dt_str=scheme.get("from-datetime"))
    log_to: datetime = datetime_parse(dt_str=scheme.get("to-datetime"))

    # if 'from' and 'to' were not specified, try 'last-days' and 'last-hours'
    if not log_from and not log_to:
        last_days: str = scheme.get("last-days", "0")
        last_hours: str = scheme.get("last-hours", "0")
        offset_days: int = int(last_days) if last_days.isdigit() else 0
        offset_hours: int = int(last_hours) if last_hours.isdigit() else 0
        if offset_days or offset_hours:
            log_from = datetime.now() - timedelta(days=offset_days,
                                                  hours=offset_hours)
    # retrieve the log entries
    log_entries: BytesIO = logging_get_entries(errors=errors,
                                               log_level=log_level,
                                               log_from=log_from,
                                               log_to=log_to)
    # errors ?
    if not errors:
        # no, return the log entries requested
        base: str = "entries"
        if log_from:
           base += f"-from_{log_from.strftime(format=DATETIME_FORMAT_COMPACT)}"
        if log_to:
           base += f"-to_{log_to.strftime(format=DATETIME_FORMAT_COMPACT)}"
        log_file = f"log_{base}.log"
        param: str = scheme.get("attach", "true")
        attach: bool = not (isinstance(param, str) and param.lower() in ["0", "f", "false"])
        log_entries.seek(0)
        result = send_file(path_or_file=log_entries,
                           mimetype="text/plain",
                           as_attachment=attach,
                           download_name=log_file)
    else:
        # yes, report the failure
        result = Response(response=json.dumps(obj={"errors": errors}),
                          status=400,
                          mimetype="application/json")

    return result


def logging_log_msgs(msgs: str | list[str],
                     output_dev: TextIO = None,
                     log_level: int = ERROR,
                     logger: logging.Logger = PYPOMES_LOGGER) -> None:
    """
    Write all messages in *msgs* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msgs: the messages list
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param log_level: the logging level, defaults to 'error' (None for no logging)
    :param logger: the logger to use
    """
    # define the log writer
    log_writer: callable = None
    match log_level:
        case "debug":
            log_writer = logger.debug
        case "info":
            log_writer = logger.info
        case "warning":
            log_writer = logger.warning
        case "error":
            log_writer = logger.error
        case "critical":
            log_writer = logger.critical

    # traverse the messages list
    msg_list: list[str] = [msgs] if isinstance(msgs, str) else msgs
    for msg in msg_list:
        # has the log writer been defined ?
        if log_writer:
            # yes, log the message
            log_writer(msg)

        # write to output
        __write_to_output(msg=msg,
                          output_dev=output_dev)


def logging_log_debug(msg: str, output_dev: TextIO = None,
                      logger: logging.Logger = PYPOMES_LOGGER) -> None:
    """
    Write debug-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param logger: the logger to use
    """
    # log the message
    logger.debug(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_info(msg: str,
                     output_dev: TextIO = None,
                     logger: logging.Logger = PYPOMES_LOGGER) -> None:
    """
    Write info-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param logger: the logger to use
    """
    # log the message
    logger.info(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_warning(msg: str,
                        output_dev: TextIO = None,
                        logger: logging.Logger = PYPOMES_LOGGER) -> None:
    """
    Write warning-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param logger: the logger to use
    """
    # log the message
    logger.warning(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_error(msg: str,
                      output_dev: TextIO = None,
                      logger: logging.Logger = PYPOMES_LOGGER) -> None:
    """
    Write error-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param logger: the logger to use
    """
    # log the message
    logger.error(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_critical(msg: str,
                         output_dev: TextIO = None,
                         logger: logging.Logger = PYPOMES_LOGGER) -> None:
    """
    Write critical-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param logger: the logger to use
    """
    # log the message
    logger.critical(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)

# @app.route(rule="/logging",
#            methods=["GET", "POST"])
def logging_service() -> Response:
    """
    Entry pointy for configuring and retrieving the execution log of the system.

    The optional *GET* criteria, used to filter the records to be returned, are specified according
    to the pattern *attach=<[t,true,f,false]>&log-level=<notset|debug|info|warning|error|critical>&
    log-from-datetime=YYYYMMDDhhmmss&log-to-datetime=YYYYMMDDhhmmss&log-last-days=<n>&log-last-hours=<n>>*:
        - *log-attach*: whether browser should display or persist file (defaults to True - persist it)
        - *log-level*: the logging level of the entries (defaults to *notset*, meaning all levels)
        - *log-from-datetime*: the start timestamp
        - log-to-datetime*: the finish timestamp
        - *log-last-days*: how many days before current date
        - *log-last-hours*: how may hours before current time
    The *POST* query parameters are also optional, and are used for configuring a re-started logger:
        - log-id: the id of the logger
        - log-file-path: path for the log file
        - log-file-mode: the mode for log file opening (a- append, w- truncate)
        - log-format: the information and formats to be written to the log
        - log-level: the loggin level (*notse*, *debug*, *info*, *warning*, *error*, *critical*)
        - log-style: the style used for building the 'log-format' parameter

    :return: the requested log data, on 'GET', and the operation status, on 'POST'
    """
    # register the request
    req_query: str = request.query_string.decode()
    logging_log_info(f"Request {request.path}?{req_query}")

    # obtain the request parameters
    scheme: dict = http_get_parameters(request=request)

    # run the request
    result: Response
    if request.method == "GET":
        result = logging_send_entries(scheme=scheme)
    else:
        logging_startup(scheme=scheme)
        result = Response(status=200)

    # log the response
    logging_log_info(f"Response {request.path}?{req_query}: {result}")

    return result


def __get_logging_level(level: Literal["debug", "info", "warning", "error", "critical"]) -> int:
    """
    Translate the log severity string *level* into the logging's internal severity value.

    :param level: the string log severity
    :return: the internal logging severity value
    """
    result: int | None
    match level:
        case "debug":
            result = DEBUG          # 10
        case "info":
            result = INFO           # 20
        case "warning":
            result = WARNING        # 30
        case "error":
            result = ERROR          # 40
        case "critical":
            result = CRITICAL       # 50
        case _:
            result = NOTSET         # 0

    return result

def __write_to_output(msg: str,
                      output_dev: TextIO) -> None:

    # has the output device been defined ?
    if output_dev:
        # yes, write the message to it
        output_dev.write(msg)

        # is the output device 'stderr' ou 'stdout' ?
        if output_dev.name.startswith("<std"):
            # yes, skip to the next line
            output_dev.write("\n")
