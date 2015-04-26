/*-
 * This file is part of Neubot <https://www.neubot.org/>.
 *
 * Neubot is free software. See AUTHORS and LICENSE for more
 * information on the copying conditions.
 */

//
// Integration test for /api/data
//

var http = require("http");

var getData = function(testName) {

    var options = {
        hostname: '127.0.0.1',
        port: 9774,
        path: '/api/2/data',
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

    var requestBody = {
        test: testName
    };

    request.end(JSON.stringify(requestBody));
};

getData("neubot_speedtest");
