var express = require("express"),
    app = express(),
    bodyParser = require('body-parser'),
    sqlite = require('sqlite3'),
    db = new sqlite.Database('test.db'),
    port = 4567;

app.get("/", function (req, res) {
  res.redirect("/index.html");
});

app.get('/get_words', function(req, res) {
  db.get("SELECT phrase_counts FROM music where artist_name=?", [req.query.artist], function(err, row) {
    // row.counts = row.counts.replace(/'/g, '"');
    // console.log(row.counts.indexOf("'"));
    // console.log(row.counts.indexOf("\'"));
    // console.log(row);
    if (!row) {
      res.send(null);
      return;
    }
    //lol fix later...
    db.get("SELECT phrase_counts FROM music where artist_name=?", [req.query.artist], function(err, row1) {
      res.send({phrases: row.phrase_counts, words: row1.phrase_counts});
    });
  });
  
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.static(__dirname));

console.log("Simple static server listening at http://localhost:" + port);
app.listen(port);
