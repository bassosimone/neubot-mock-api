#!/usr/bin/env python

#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Example serving files in the current directory """

import cgi
import logging
import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))

import neubot_http

class PrettyWWWHandler(neubot_http.WWWHandler):
    """ Pretty WWW handler """

    @staticmethod
    def guess_mimetype(path):
        return "text/plain", None

    def serve_directory(self, request, path):
        yield neubot_http.serializer.compose_headers("200", "Ok", {
            "Content-Type": "text/html",
            "Transfer-Encoding": "chunked",
        })
        yield neubot_http.serializer.compose_chunk("<HTML><BODY>\n")
        for name in os.listdir(path):
            fullpath = os.sep.join([path, name])
            if os.path.isdir(fullpath):
                name += "/"
            elif not os.path.isfile(fullpath):
                continue
            quot = cgi.escape(name)
            chunk = "  <DIV><A HREF='%(name)s'>%(quot)s</A></DIV>\n" % locals()
            yield neubot_http.serializer.compose_chunk(chunk)
        yield neubot_http.serializer.compose_chunk("</BODY></HTML>\n")
        yield neubot_http.serializer.compose_last_chunk()

    def serve_filep(self, request, path, filep):
        yield neubot_http.serializer.compose_headers("200", "Ok", {
            "Content-Type": "text/html",
            "Transfer-Encoding": "chunked",
        })
        yield neubot_http.serializer.compose_chunk("<HTML><BODY>\n")
        yield neubot_http.serializer.compose_chunk("<HR><PRE>")
        yield neubot_http.serializer.compose_chunk(cgi.escape(filep.read()))
        yield neubot_http.serializer.compose_chunk("</PRE><HR>")
        yield neubot_http.serializer.compose_chunk("</BODY></HTML>\n")
        yield neubot_http.serializer.compose_last_chunk()

def main():
    """ Main function """
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    neubot_http.serve({
        "www_handler": PrettyWWWHandler,
        "rootdir": ".",
    })

if __name__ == "__main__":
    main()
