#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Requests router """

import json

from . import http

class Router(object):
    """ Backend class """

    def __init__(self, state_tracker, schedule):
        self.state_tracker = state_tracker
        self.schedule = schedule
        self.routes = {
            "/api": self.serve_api,
            "/api/": self.serve_api,
            "/api/2/config/labels": self.serve_api_config,
            "/api/2/data": self.serve_api_data,
            "/api/2/runner": self.not_implemented,
            "/api/debug": self.not_implemented,
            "/api/exit": self.serve_api_exit,
            "/api/index": self.not_implemented,
            "/api/log": self.serve_api_log,
            "/api/results": self.not_implemented,
            "/api/state": self.serve_api_state,
            "/api/version": self.serve_api_version,
        }

    def __iter__(self):
        return iter(self.routes)

    def __getitem__(self, key):
        return self.routes[key]

    @staticmethod
    def serve_api(connection, _):
        """ Manages /api/ URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(list(connection.server.routes.keys()))))

    def serve_api_config(self, connection, request):
        """ Manages /api/2/config URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps({})))

    def serve_api_data(self, connection, request):
        """ Manages /api/2/data URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps({})))

    @staticmethod
    def not_implemented(connection, _):
        """ Manages /api/debug URL """
        connection.write(http.writer.compose_error("501", "Not Implemented"))

    @staticmethod
    def serve_api_exit(*_):
        """ Manages /api/exit URL """
        raise KeyboardInterrupt

    def serve_api_log(self, connection, request):
        """ Manages /api/log URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps({})))

    def serve_api_state(self, connection, request):
        """ Manages /api/state URL """
        if "?" not in request.url or request.url.endswith("?t=0"):
            self._really_serve_api_state(connection, request)
        else:
            self.state_tracker.subscribe(self._really_serve_api_state,
                                         connection, request)

    def _really_serve_api_state(self, connection, _):
        """ Real /api/state URL handler """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.state_tracker.as_dict())))

    @staticmethod
    def serve_api_version(connection, _):
        """ Manages /api/version URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "text/plain",
        }, "0.5.0.0"))
