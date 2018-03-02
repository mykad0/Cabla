var express = require('express');
var mongoose = require('mongoose');

// Open connection to mongo DB
mongoose.connect("mongodb://admin:admin@localhost:27017/test");
var db = mongoose.connection; 
db.on('error', console.error.bind(console, 'Error while connecting to local database')); 
db.once('open', function (){
    console.log("Connected to local database " + db.name); 
}); 

var LifeEventSchema = new mongoose.Schema({
    place: String,
    date: Date,
    docs: Array,
    note: String
});

var CheckableInfoSchema = new mongoose.Schema({
    // anything
    levelOfCertainty: String // enum
});

var LifeEvent = mongoose.model('LifeEvent', LifeEventSchema);
var CheckableInfo = mongoose.model('CheckableInfo', CheckableInfoSchema);

var personSchema = new mongoose.Schema({
    uid: Number,
    name: String,
    firstName: String,
    firstNames: Array,
    gender: String, // enum
    parentRelationship: Number,
    birth: {
        type: Object,
        ref: 'LifeEvent'
    },
    death: {
        type: Object,
        ref: 'LifeEvent'
    },
    relationships: Number,
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now }
}, { id: false }, {_id: false});

personSchema.method('insert', function (doc, callback) {
  Object.assign(this, doc, { createdAt: new Date() });
  this.parent().save(callback);
});

personSchema.method('update', function (updates, callback) {
  Object.assign(this, updates, { updatedAt: new Date() });
  this.parent().save(callback);
});

var Person = mongoose.model('Persons', personSchema);

var personRouter = express.Router();

personRouter.route("/persons")
.get(function(req, res){
    console.log("GET request received");
    Person.find(function(err, persons){
        if (err) return next(err);
        res.json(persons);
    });
});

personRouter.route("/persons/:personId")
.get(function(req, res){
    console.log("GET request received");
    Person.find({uid: req.params.personId}).exec((err, person) => {
        if (err) return next(err);
        res.json(person);
    });
})
.put(function(req, res){
    console.log("PUT request received");
    Person.find({uid: req.params.personId}).update(req.body, (err, person) => {
        if (err) return next(err);
        res.json(person);
    });
})
.post(function(req, res){
    console.log("POST request received");
    var person = new Person(req.body);
    Person.save((err, person) => {
        if (err) return next(err);
        res.json(person);
    });
})
.delete(function(req, res){
    console.log("DELETE request received");
    Person.find({uid: personId}).remove(req.body, (err, person) => {
        if (err) return next(err);
        res.json("Person " + personId + " has been removed");
    });
});

var app = express();

var bodyParser = require("body-parser"); 
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(personRouter);

app.use((req, res, next) => {
    const err = new Error('This endpoint does not exists');
    err.status = 404;
    next(err);
});

app.use((err, req, res, next) => {
    res.status(err.status || 500);
    res.json({error: err.message});
});

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header(
        'Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Accept'
    );

    if (req.method === 'Options') {
        res.header('Access-Control-Allow-Methods', 'GET', 'PUT, POST, DELETE');
        return res.status(200).json({});
    }
});

app.listen(3000, () => console.log("Listening on port 3000 ..."));
