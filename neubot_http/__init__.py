#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

"""
 Neubot HTTP library.

 Example usage:

     import neubot_http
     import json

     def simple(request):
         ''' Handles /URL '''
         response = {
             "method": request.method,
             "url": request.url,
             "protocol": request.protocol,
             "headers": request.headers,
             "body": request.body_as_string()
         }
         yield neubot_http.serializer.compose_response("200", "Ok", {
             "Content-Type": "application/json",
         }, json.dumps(response, indent=4))

     def main():
         ''' Main function '''
         neubot_http.serve({
             "routes": {
                 "/simple": simple,
             }
         })
"""

from .serve import serve
from .www_handler import WWWHandler
from . import serializer
