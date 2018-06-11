var express = require('express');
var app = express();

const sqlite3 = require('sqlite3').verbose();

let dbTor = new sqlite3.Database('./db/insideTor.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error(err.message);
    } else {
        console.log('Connected to the insideTor database.');
    }
});


let dbIot = new sqlite3.Database('./db/insideIot.db', sqlite3.OPEN_READONLY, (err) => {
    if(err) {
        console.error(err.message);
    } else {
        console.log('Connected to the insideIoT database.');
}
})
;


//dangerous solution - to change!
//set to test integration between Angular and Node in the same machine
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get('/', function (req, res) {
    res.send('hello world');
});

app.get('/api/tor/count', function (req, res) {

    req.query.key = req.query.key.split(" ");

    let sql = "select count(*) AS count from (select count(distinct Words.word) from Words " +
        "inner join Pairs on Words.id = Pairs.word_id " +
        "inner join Pages on Pairs.page_id = Pages.id " +
        "inner join Sentences on Sentences.id = Pairs.sentence_id " +
        "where Words.word IN ('" + req.query.key.join("','") + "') " +
        "group by Pages.url) ;";

    console.log(sql);

    // Print the records as JSON
    dbTor.all(sql, function (err, rows) {
        res.send(JSON.stringify(rows));
        console.log(rows);
    });
});

app.get('/api/tor/search', function (req, res) {
    let pagesPerPage = req.query.ppage == undefined ? 40 : req.query.ppage;
    let page = req.query.page == undefined ? 0 : req.query.page;
    let start = page * pagesPerPage;

    req.query.key = req.query.key.split(" ");

    let sql = "select count(distinct Words.word) AS count, Pages.url AS url, Sentences.sentence AS sentence, Pages.title AS title, Pages.id AS idPage from Words " +
        "inner join Pairs on Words.id = Pairs.word_id " +
        "inner join Pages on Pairs.page_id = Pages.id " +
        "inner join Sentences on Sentences.id = Pairs.sentence_id " +
        "where Words.word IN ('" + req.query.key.join("','") + "') " +
        "group by Pages.url " +
        "order by count(distinct Words.word) DESC " +
        "LIMIT " + pagesPerPage + " OFFSET " + start + " ;";

    console.log(sql);

    // Print the records as JSON
    dbTor.all(sql, function (err, rows) {
        res.send(JSON.stringify(rows));
    });
});

app.get('/api/iot/count', function (req, res) {

    req.query.key = req.query.key.split(" ");

    /* this should be replaced with sql command to get count from iot database */
    let sql = "select count(*) AS count from Devices "+
        "where Devices.banner LIKE '" + req.query.key.join("' OR Devices.banner LIKE '%") + "%' ;";

    console.log(sql);

    /* dbTor change to dbIot */
    // Print the records as JSON 
    dbIot.all(sql, function (err, rows) {
        res.send(JSON.stringify(rows));
        console.log(rows);
    });
});

app.get('/api/iot/search', function (req, res) {
    let pagesPerPage = req.query.ppage == undefined ? 40 : req.query.ppage;
    let page = req.query.page == undefined ? 0 : req.query.page;
    let start = page * pagesPerPage;

    req.query.key = req.query.key.split(" ");

    /* this should be replaced with sql command to get count from iot database */
    let sql = "select Devices.ip as ip, Devices.port as port, Devices.banner as banner from Devices "+
        "where Devices.banner LIKE '" + req.query.key.join("' OR Devices.banner LIKE '%") + "%' " +
        "LIMIT " + pagesPerPage + " OFFSET " + start + " ;";

    console.log(sql);

    /* dbTor change to dbIot */
    // Print the records as JSON
    dbIot.all(sql, function (err, rows) {
        res.send(JSON.stringify(rows));
    });
});


app.listen(9112);

var http = require('http');
var url = require('url');

http.createServer(function (req, res) {
    var q = url.parse(req.url, true);
    var qdata = q.query;

    let sql = "SELECT Pages.html FROM Pages WHERE Pages.id = " + qdata.page + " ;";
    console.log(sql);

    dbTor.all(sql, function (err, rows) {
        console.log(rows);
        if (err) {
            res.writeHead(404, {'Content-Type': 'text/html'});
            return res.end("404 Not Found");
        }
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write(rows[0].html);
        return res.end();
    });
}).listen(9979); 