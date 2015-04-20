#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot scheduler API """

import json

from . import state_manager
from .. import http

def api_(connection, _):
    """ Implements /api/ API """
    connection.write(http.writer.compose_response("200", "Ok", {
        "Content-Type": "application/json",
    }, json.dumps(list(connection.server.routes.keys()))))

def api_config(connection, request):
    """ Implements /api/config API """
    raise NotImplementedError

def api_data(connection, request):
    """ Implements /api/data API """
    raise NotImplementedError

def api_debug(connection, _):
    """ Implements /api/debug API """
    connection.write(http.writer.compose_error("501", "Not Implemented"))

def api_exit(*_):
    """ Implements /api/exit API """
    raise KeyboardInterrupt

def api_index(connection, _):
    """ Implements /api/index API """
    connection.write(http.writer.compose_error("501", "Not Implemented"))

def api_log(connection, request):
    """ Implements /api/log API """
    raise NotImplementedError

def api_results(connection, request):
    """ Implements /api/results API """
    raise NotImplementedError

def api_state(connection, request):
    """ Implements /api/state API """
    if "?" not in request.url:
        connection.write(state_manager.get().serialize())
    elif request.url.endswith("?t=0"):
        connection.write(state_manager.get().serialize())
    else:
        state_manager.get().comet_wait(connection)

def api_version(connection, _):
    """ Implements /api/version API """
    connection.write(http.writer.compose_response("200", "Ok", {
        "Content-Type": "text/plain",
    }, "0.5.0.0"))
