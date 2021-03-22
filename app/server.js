// server.js
const path = require("path");
const express = require("express");
const app = express();
// If an incoming request uses
// a protocol other than HTTPS,
// redirect that request to the
// same url but with HTTPS
const forceSSL = function () {
  return function (req, res, next) {
    if (req.headers["x-forwarded-proto"] !== "https") {
      return res.redirect(["https://", req.get("Host"), req.url].join(""));
    }
    next();
  };
};

// Instruct the app
// to use the forceSSL
// middleware
app.use(forceSSL());

// For all GET requests, send back index.html
// so that PathLocationStrategy can be used
app.use(express.static(path.join("dist")));

// Send the index.html whatever the request is.
app.get("*", (req, res) => {
  res.sendFile(path.resolve("dist", "app", "index.html"));
});

app.listen(process.env.PORT || 8080);
