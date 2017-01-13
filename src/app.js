var express = require('express');
var mime = require('mime');
var bodyParser = require('body-parser')
var app = express();

app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

/**
 * The only route
 * POST /log
 */
app.post('/log', function (req, res) {
  console.log(req.body);
  res.writeHead(200, {"Content-Type": "text/plain"});
  res.end("Message logged");
});

/**
 * Startup function.
 */
app.listen(6666, function () {
  console.log('metadata server is up on port 6666');
});
