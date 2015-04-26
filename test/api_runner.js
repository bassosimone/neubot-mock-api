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

var startTest = function(testName, domain) {

    var options = {
        hostname: '127.0.0.1',
        port: 9774,
        path: '/api/runner',
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
        test: testName,
        params: {
            '$domain': domain
        }
    };

    request.end(JSON.stringify(requestBody));
};

startTest("mtr", "8.8.8.8");
//startTest("traceroute", "8.8.8.8");
