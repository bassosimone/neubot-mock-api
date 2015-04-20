#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

"""
 Neubot HTTP library.

 Example usage:

     import asyncore
     import json
     import neubot_http

     def simple(connection, request):
         ''' Handles /URL '''
         response = {
             "method": request.method,
             "url": request.url,
             "protocol": request.protocol,
             "headers": request.headers,
             "body": request.body_as_string()
         }
         connection.write(yield neubot_http.serializer.compose_response(
             "200", "Ok", {
                 "Content-Type": "application/json",
             }, json.dumps(response, indent=4)))

     def main():
         ''' Main function '''
         neubot_http.listen({
             "routes": {
                 "/simple": simple,
             }
         })
         asyncore.loop()
"""

from .core import listen
from . import serializer
