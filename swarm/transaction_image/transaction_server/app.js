var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var dotenv = require('dotenv');
dotenv.config();

var indexRouter = require('./routes/index');
var apiRouter = require('./routes/api');

var mongoose = require('mongoose');
mongoose.connect('mongodb://mongos0:27017/stocks', {useNewUrlParser: true}).
	catch(error => console.log(error));
var mongodb = mongoose.connection;
mongodb.on('connected', () => {
	console.log("Connected to mongodb");
});
mongodb.on('error', (err) => {
	console.log("Error connecting to mongo");
	console.log(err);
	console.log("Error connecting to mongo");
});
mongodb.on('disconnected', () => {
	console.log("Mongo connection disconnected");
});
process.on('SIGINT', () => {  
  mongodb.close(() => { 
    console.log('Mongoose default connection disconnected through app termination'); 
    process.exit(0); 
  }); 
});

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/api', apiRouter);

module.exports = app;
