var express = require('express');
var router = express.Router();
const axios = require('axios');

function send_to_transaction(res, data) {
	axios.post('http://transaction_server:5000/', data).
		then((response) => {
			res.send({
				message: "Success.",
				data: response.data
			});
		}, (error) => {
			console.log(error);
			res.send({
				message: "error communicating between web_app and transaction server",
				error	
			});
	});
}

router.post('/command/', (req, res, next) => {
	/*
	Expected req.body:
	{
		command: 'add',
		userid: userid,
		amount: amount of cash to add to account (float)
	}
	
	{
		command: 'quote',
		userid: userid,
		stock: stock symbol
	}
	
	{
		command: 'buy',
		userid: userid,
		amount: number of stocks to purchase (integer)
	}
	*/
	send_to_transaction(res, req.body);
});

router.post('/test/', (req, res, next) => {
	axios.post('http://transaction_server:5000/', {
		body: 'hi'
	}).then((response) => {
		console.log(response.data);
		res.send(response.data);
	}, (error) => {
		console.log(error);
		res.send(error);
	});
});

router.post('/add/:userid/:amount/', (req, res, next) => {
	var data = {
		command: "add",
		userid: userid,
		amount: amount
	};
	
	send_to_transaction(res, data);
});

router.post('/quote/:userid/:stock/', (req, res, next) => {
	
});

router.post('/buy/:userid/:stock/:amount/', (req, res, next) => {
	
});

router.post('/commit_buy/:userid/', (req, res, next) => {
	
});

router.post('/cancel_buy/:userid/', (req, res, next) => {
	
});

router.post('/sell/:userid/:stock/:amount/', (req, res, next) => {
	
});

router.post('/commit_sell/:userid/', (req, res, next) => {
	
});

router.post('/cancel_sell/:userid/', (req, res, next) => {
	
});

router.post('/set_buy_amount/:userid/:stock/:amount/', (req, res, next) => {
	
});

router.post('/cancel_set_buy/:userid/:stock/', (req, res, next) => {
	
});

router.post('/set_buy_trigger/:userid/:stock/:amount/', (req, res, next) => {
	
});

router.post('/set_sell_amount/:userid/:stock/:amount/', (req, res, next) => {
	
});

router.post('/cancel_set_sell/:userid/:stock/', (req, res, next) => {
	
});

router.post('/set_sell_trigger/:userid/:stock/:amount/', (req, res, next) => {
	
});

router.post('/dumplog/:userid/', (req, res, next) => {
	
});

router.post('/dumplog/', (req, res, next) => {
	
});

router.post('/display_summary/:userid/', (req, res, next) => {
	
});


module.exports = router;
