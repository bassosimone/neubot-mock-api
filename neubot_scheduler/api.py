#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot scheduler API """

import cgi
import json

from . import backend
from . import http

class StateManager(object):
    """ State manager """

    def __init__(self):
        self.pending = []

    def serialize(self):
        """ Serialize state manager """
        return http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}")

    def comet_wait(self, connection):
        self.pending.append(connection)

    def comet_trigger(self):
        pending = self.pending
        self.pending = []
        for connection in pending:
            try:
                connection.write(self.serialize())
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                logging.warning("unhandled exception", exc_info=1)

STATE_MANAGER = StateManager()

def state_manager():
    """ Get singleton instance """
    return STATE_MANAGER

def api_(connection, _):
    """ Implements /api/ API """
    connection.write(http.writer.compose_response("200", "Ok", {
        "Content-Type": "application/json",
    }, json.dumps(list(connection.server.routes.keys()))))

def api_config(connection, request):
    """ Implements /api/config API """

    query = ""
    index = request.url.find("?")
    if index >= 0:
        query = request.url[index + 1:]

    labels = 0
    dictionary = cgi.parse_qs(query)
    if "labels" in dictionary:
        backend.get().get_config(connection, True)
    elif request.method == "POST":
        incoming = json.loads(request.body_as_string("utf-8"))
        backend.get().set_config(connection, incoming)
    else:
        backend.get().get_config(connection, False)

def api_data(connection, request):
    """ Implements /api/data API """

    query = ""
    index = request.url.find("?")
    if index >= 0:
        query = request.url[index + 1:]

    since, until, test = -1, -1, ""
    dictionary = cgi.parse_qs(query)
    if "test" in dictionary:
        test = str(dictionary["test"][0])
    if "since" in dictionary:
        since = int(dictionary["since"][0])
    if "until" in dictionary:
        until = int(dictionary["until"][0])

    backend.get().query_data(connection, test, since, until);

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

    query = ""
    index = request.url.find("?")
    if index >= 0:
        query = request.url[index + 1:]

    reverse, verbosity = 0, 0
    dictionary = cgi.parse_qs(query)
    if "reversed" in dictionary:
        reverse = str(dictionary["reversed"][0])
    if "verbosity" in dictionary:
        verbosity = int(dictionary["verbosity"][0])

    backend.get().query_logs(connection, reverse, verbosity)

def api_results(connection, request):
    """ Implements /api/results API """

    query = ""
    index = request.url.find("?")
    if index >= 0:
        query = request.url[index + 1:]

    test = ""
    dictionary = cgi.parse_qs(query)
    if "test" in dictionary:
        test = str(dictionary["test"][0])

    backend.get().query_tests(connection, test)

def api_state(connection, request):
    """ Implements /api/state API """
    if "?" not in request.url:
        connection.write(state_manager().serialize())
    elif request.url.endswith("?t=0"):
        connection.write(state_manager().serialize())
    else:
        state_manager().comet_wait(connection)

def api_version(connection, _):
    """ Implements /api/version API """
    connection.write(http.writer.compose_response("200", "Ok", {
        "Content-Type": "text/plain",
    }, "0.5.0.0"))
