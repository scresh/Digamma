var express = require('express');
var app = express();

const sqlite3 = require('sqlite3').verbose();

let dbTor = new sqlite3.Database('./db/insideTor.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the insideTor database.');
});

let dbIoT = new sqlite3.Database('./db/insideIoT.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the insideIoT database.');
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

    req.query.key = req.query.key.split(" ");

    let sql = "select count(*) AS count from (select count(distinct Words.word) from Words "+
        "inner join Pairs on Words.id = Pairs.word_id "+
        "inner join Pages on Pairs.page_id = Pages.id "+
        "inner join Sentences on Sentences.id = Pairs.sentence_id "+
        "where Words.word IN ('" + req.query.key.join("','") + "') "+
        "group by Pages.url) ;";

    console.log(sql);

    // Print the records as JSON
    dbTor.all(sql, function(err, rows) {
        res.send(JSON.stringify(rows));
        console.log(rows);
    });
});

app.get('/api/search', function(req, res){
    let pagesPerPage = req.query.ppage == undefined ? 40 : req.query.ppage;
    let page = req.query.page == undefined ? 0 : req.query.page;
    let start = page * pagesPerPage;

    req.query.key = req.query.key.split(" ");

    let sql = "select count(distinct Words.word) AS count, Pages.url AS url, Sentences.sentence AS sentence, Pages.title AS title from Words "+
        "inner join Pairs on Words.id = Pairs.word_id "+
        "inner join Pages on Pairs.page_id = Pages.id "+
        "inner join Sentences on Sentences.id = Pairs.sentence_id "+
        "where Words.word IN ('" + req.query.key.join("','") + "') "+
        "group by Pages.url "+
        "order by count(distinct Words.word) DESC "+
        "LIMIT "+ pagesPerPage + " OFFSET " + start +" ;";

    console.log(sql);

    // Print the records as JSON
    dbTor.all(sql, function(err, rows) {
        res.send(JSON.stringify(rows));
    });
});

app.listen(9112);