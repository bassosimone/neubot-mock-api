#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Requests router """

import cgi
import json

from . import http
from . import utils

class Router(object):
    """ Backend class """

    def __init__(self, config_db, data_db, log_db, net_tests_db,
                 runner, state_tracker):
        self.config_db = config_db
        self.data_db = data_db
        self.log_db = log_db
        self.net_tests_db = net_tests_db
        self.runner = runner
        self.state_tracker = state_tracker
        self.routes = {
            "/api": self.serve_api,
            "/api/": self.serve_api,
            "/api/config": self.serve_api_config,
            "/api/data": self.serve_api_data,
            "/api/debug": self.serve_api_debug,
            "/api/exit": self.serve_api_exit,
            "/api/index": self.serve_api_index,
            "/api/log": self.serve_api_log,
            #"/api/runner": self.serve_api_runner,
            "/api/state": self.serve_api_state,
            "/api/tests": self.serve_api_tests,
            "/api/version": self.serve_api_tests,
            "/": self.serve_rootdir,
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
        """ Manages /api/config URL """
        query = ""
        index = request.url.find("?")
        if index >= 0:
            query = request.url[index + 1:]
        params = cgi.parse_qs(query)
        if "labels" in params and int(params["labels"][0]):
            body_out = self.config_db.select(True)
        elif request.method == "POST":
            body_in = json.loads(request.body_as_string("utf-8"))
            self.config_db.update(body_in, True)
            body_out = {}
        else:
            body_out = self.config_db.select(False)
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(body_out)))

    def serve_api_data(self, connection, request):
        """ Manages /api/data URL """
        query = ""
        index = request.url.find("?")
        if index >= 0:
            query = request.url[index + 1:]
        test, since, until, offset, limit = "", 0, utils.timestamp(), 0, 128
        params = cgi.parse_qs(query)
        if "test" in params:
            test = str(params["test"][0])
        if "since" in params:
            since = int(params["since"][0])
        if "until" in params:
            until = int(params["until"][0])
        if "offset" in params:
            offset = int(params["offset"][0])
        if "limit" in params:
            limit = int(params["limit"][0])
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.data_db.select(test, since, until, offset, limit))))

    @staticmethod
    def serve_api_debug(connection, _):
        """ Manages /api/debug URL """
        connection.write(http.writer.compose_error("501", "Not Implemented"))

    @staticmethod
    def serve_api_exit(*_):
        """ Manages /api/exit URL """
        raise KeyboardInterrupt

    @staticmethod
    def serve_api_index(connection, _):
        """ Manages /api/index URL """
        connection.write(http.writer.compose_error("501", "Not Implemented"))

    def serve_api_log(self, connection, request):
        """ Manages /api/log URL """
        query = ""
        index = request.url.find("?")
        if index >= 0:
            query = request.url[index + 1:]
        since, until = 0, utils.timestamp()
        params = cgi.parse_qs(query)
        if "since" in params:
            since = int(params["since"][0])
        if "until" in params:
            until = int(params["until"][0])
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.log_db.select(since, until))))

#   def serve_api_runner(self, connection, request):
#       """ Manages /api/runner URL """
#       query = ""
#       index = request.url.find("?")
#       if index >= 0:
#           query = request.url[index + 1:]
#       streaming = 0
#       test = ""
#       params = cgi.parse_qs(query)
#       if "streaming" in params:
#           streaming = int(params["streaming"][0])
#       if "test" in params:
#           test = str(params["test"][0])
#       self.runner.run(connection, test, streaming)

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

    def serve_api_tests(self, connection, _):
        """ Manages /api/tests URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.net_tests_db.read_all())))

    @staticmethod
    def serve_api_version(connection, _):
        """ Manages /api/version URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "text/plain",
        }, "0.5.0.0"))

    def serve_rootdir(self, connection, _):
        """ Manages the / URL """
        body = []
        body.append("<html></html>")
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "text/html",
        }, "".join(body)))
