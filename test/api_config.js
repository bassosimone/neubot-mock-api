/*-
 * This file is part of Neubot <https://www.neubot.org/>.
 *
 * Neubot is free software. See AUTHORS and LICENSE for more
 * information on the copying conditions.
 */

//
// Integration test for /api/runner
//

var http = require("http");

var changeConfig = function(requestBody) {

    var options = {
        hostname: '127.0.0.1',
        port: 9774,
        path: '/api/2/config',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    var request = http.request(options, function (response) {
        console.log('STATUS: ' + response.statusCode);
        console.log('HEADERS: ' + JSON.stringify(response.headers));
        response.setEncoding('utf8');
        response.on('data', function (chunk) {
            console.log('BODY: ' + chunk);
        });
    });

    request.end(JSON.stringify(requestBody));
};

changeConfig({
    enabled: 0
});
