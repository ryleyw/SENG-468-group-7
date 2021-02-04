var express = require('express');
var router = express.Router();


const dbMongo = require('../dbMongo');

router.post('/test/', (req, res, next) => {
	console.log("received message:");
	console.log(req.body);
	res.send({body: "reply!"});
});

router.post('/command/', (req, res, next) => {
	var data = req.body;
	if (data.command.toLowerCase() == "add") {
		dbMongo.handle_req(req, res);
	} else {
		res.send({
			success: false,
			message: "Command not recognized."
		});
	}
});

/*
router.post('/write/:db/csv/:count/', (req, res, next) => {
	// api trigger to write roughly count rows into the database
	var count = parseInt(req.params.count);
	var new_req = {
		body: {
			mode: "csvWrite",
			count: count
		}
	};
	if (isNaN(count)) {
		res.send({
			success: false,
			err: "Incorrect count field. Must be integer.\n/:write/:db/csv/:count/"
		});
	} else if (req.params.db == "mongo") {
		dbMongo.handle_req(new_req, res);
	} else if (res.params.db == "sql") {
		dbSQL.handle_req(new_req, res);
	} else {
		res.send({
			success: false,
			err: "Incorrect db field. Must be 'mongo' or 'sql'.\n/:write/:db/csv/:count/"
		});
	}
})
router.post('/:mode/:db/part/', (req, res, next) => {
	var new_req = {
		body: {
			mode: req.params.mode,
			args: req.body
		}
	};
	console.log(req.body);
	if (req.params.mode != "read" && req.params.mode != "write") {
		res.send({
			success: false,
			err: "Incorrect mode field. Must be 'read', or 'write'.\n/:mode/:db/part/"
		});
	} else if (req.params.db == "mongo") {
		dbMongo.handle_req(new_req, res);
	} else if (req.params.db == "sql") {
		dbSQL.handle_req(new_req, res);
	} else {
		res.send({
			success: false,
			err: "Incorrect db field. Must be 'mongo', or 'sql'.\n/api/:mode/:db/part/"
		});
	}
})
router.post('/:mode/:db/boat/', (req, res, next) => {
	var new_req = {
		body: {
			mode: req.params.mode,
			args: req.body
		}
	};
	if (req.params.mode != "read" && req.params.mode != "write") {
		res.send({
			success: false,
			err: "Incorrect mode field. Must be 'read', or 'write'.\n/api/:mode/:db/boatPart/"
		});
	} else if (req.params.db == "mongo") {
		dbMongo.handle_req(new_req, res);
	} else if (req.params.db == "sql") {
		dbSQL.handle_req(new_req, res);
	} else {
		res.send({
			success: false,
			err: "Incorrect db field. Must be 'mongo', or 'sql'.\n/api/:mode/:db/boatPart/"
		});
	}
})
router.post('/:mode/:db/boatPart/', (req, res, next) => {
	var new_req = {
		body: {
			mode: req.params.mode,
			args: req.body
		}
	};
	if (req.params.mode != "read" && req.params.mode != "write") {
		res.send({
			success: false,
			err: "Incorrect mode field. Must be 'read', or 'write'.\n/api/:mode/:db/boatPart/"
		});
	} else if (req.params.db == "mongo") {
		dbMongo.handle_req(new_req, res);
	} else if (req.params.db == "sql") {
		dbSQL.handle_req(new_req, res);
	} else {
		res.send({
			success: false,
			err: "Incorrect db field. Must be 'mongo', or 'sql'.\n/api/:mode/:db/boatPart/"
		});
	}
})

*/
module.exports = router;
