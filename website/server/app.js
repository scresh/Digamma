var express = require('express');
var app = express();

const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./db/insideTor.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the insideTor database.');
});

//dangerous solution - to change!
//set to test integration between Angular and Node in the same machine
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get('/', function(req, res){
    res.send('hello world');
});

app.get('/api/count', function(req, res){
    let sql = "SELECT COUNT(*) AS count " +
        "FROM Words " +
        "INNER JOIN Pairs on Words.id = Pairs.word_id " +
        "INNER JOIN Urls on Urls.id = Pairs.url_id " +
        "WHERE Words.word LIKE " + "'%" + req.query.key + "%';";

    console.log(sql);

    // Print the records as JSON
    db.all(sql, function(err, rows) {
        res.send(JSON.stringify(rows));
    });
});

app.get('/api/search', function(req, res){
    let pagesPerPage = req.query.ppage == undefined ? 40 : req.query.ppage;
    let page = req.query.page == undefined ? 0 : req.query.page;
    let start = page * pagesPerPage;
    let sql = "SELECT Words.word, Urls.url " +
        "FROM Words " +
        "INNER JOIN Pairs on Words.id = Pairs.word_id " +
        "INNER JOIN Urls on Urls.id = Pairs.url_id " +
        "WHERE Words.word LIKE " + "'%" + req.query.key + "%' " +
        "LIMIT " + pagesPerPage + " OFFSET " + start +" ;";

    console.log(sql);

    // Print the records as JSON
    db.all(sql, function(err, rows) {
        res.send(JSON.stringify(rows));
    });
});

app.listen(9112);