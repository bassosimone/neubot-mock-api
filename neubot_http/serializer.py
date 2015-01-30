#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" HTTP serializer """

import logging
import os

def compose(first_line, headers, before, filep, after):
    """ Compose a generic HTTP message """

    logging.debug("> %s", first_line)
    yield first_line + b"\r\n"

    tot = 0
    if before:
        tot += len(before)
    if filep:
        filep.seek(0, os.SEEK_END)
        tot += filep.tell()
        filep.seek(0, os.SEEK_SET)
    if after:
        tot += len(after)
    headers["Content-Length"] = tot

    for name, value in headers.items():
        if value is not None:
            logging.debug("> %s: %s", name, value)
            yield b"%s: %s\r\n" % (name, value)
    yield b"\r\n"

    if before:
        yield before
    while filep:
        data = filep.read(65536)
        if not data:
            break
        yield data
    if after:
        yield after

def compose_response(code, reason, headers, body):
    """ Compose a generic HTTP message """
    return compose(b"HTTP/1.1 %s %s" % (code, reason),
                   headers, body, None, None)

def compose_filep(code, reason, headers, filep):
    """ Compose a generic HTTP message """
    return compose(b"HTTP/1.1 %s %s" % (code, reason),
                   headers, None, filep, None)

def compose_error(code, reason):
    """ Compose an HTTP error message """
    return compose_response(code, reason, {
        "Content-Type": "text/html",
    }, b"""\
        <HTML>
         <HEAD>
          <TITLE>%(code)s %(reason)s</TITLE>
         <HEAD>
         <BODY>
          <P>Error occurred: %(code)s %(reason)s</P>
         </BODY>
        </HTML>
        """ % locals())

def compose_headers(code, reason, headers):
    """ Compose headers of HTTP response """
    return compose_response(code, reason, headers, None)

def compose_redirect(target):
    """ Compose a redirect response """
    return compose_response("302", "Found", {
        "Location": target
    }, b"""\
        <HTML>
         <HEAD>
          <TITLE>Redirected to: %(target)s</TITLE>
         <HEAD>
         <BODY>
          <P>Redirected to: %(target)s</P>
         </BODY>
        </HTML>
        """ % locals())

def compose_chunk(chunk):
    """ Compose a body chunk """
    logging.debug("> %x", len(chunk))
    yield b"%x\r\n" % len(chunk)
    logging.debug("> {%d bytes}", len(chunk))
    yield chunk
    logging.debug(">")
    yield b"\r\n"
