#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Requests router """

import cgi
import json
import logging
import re

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
            "/api/2/config/labels": self.serve_api_2_config_labels,
            "/api/2/config": self.serve_api_2_config,
            "/api/2/data": self.serve_api_2_data,
            "/api/2/runner": self.serve_api_2_runner,
            "/api/debug": self.not_implemented,
            "/api/exit": self.serve_api_exit,
            "/api/index": self.not_implemented,
            "/api/log": self.serve_api_log,
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

    def serve_api_2_config_labels(self, connection, request):
        """ Manages /api/2/config/labels URL """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.config_db.select_labels())))

    def serve_api_2_config(self, connection, request):
        """ Manages /api/2/config URL """
        request_body = request.body_as_string("utf-8")
        if request_body:
            request_body = json.loads(request_body)
            self.config_db.update(request_body)
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.config_db.select())))

    def serve_api_2_data(self, connection, request):
        """ Manages /api/2/data URL """
        request_body = json.loads(request.body_as_string("utf-8"))
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(self.data_db.select(
            request_body["test"],
            request_body.get("since", 0),
            request_body.get("until", utils.timestamp()),
            request_body.get("offset", 0),
            request_body.get("limit", 128)))))

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

    def serve_api_2_runner(self, connection, request):
        """ Manages /api/2/runner URL """
        request_body = json.loads(request.body_as_string("utf-8"))
        test = request_body["test"]
        descr = self.net_tests_db.read_one(test)
        logging.debug("/api/runner: orig cmdline: %s", descr["command_line"])
        command_line = []
        for item in descr["command_line"]:
            if not item.startswith("$"):
                command_line.append(item)
                continue
            if item not in request_body["params"]:
                raise RuntimeError("No mapping for param")
            value = request_body["params"][item]
            if not re.match(descr["params"][item]["regexp"], value):
                raise RuntimeError("Invalid parameter")
            command_line.append(value)
        logging.debug("/api/runner: expanded cmdline: %s", command_line)
        self.runner.run(test, command_line)
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

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
