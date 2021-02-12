const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const csv = require('csv-parser');
const fs = require('fs');

const userSchema = new Schema({
	Username: { type: String, required: true },
	Cash: { type: Number, default: 0.0 }
});

const User = mongoose.model('users', userSchema);


module.exports = {
	handle_req: function(req, res) {		
		if (!mongoose.connection.db) {
			// mongoose didn't have an initial connection so we need to try again
			mongoose.connect('mongodb://mongos0:27017/stocks', {useNewUrlParser: true}).
				catch(error => console.log(error));
		}
		
		var data = req.body;
		
		if (data.command.toLowerCase() == 'add') {
			var userid = data.userid;
			var amount = parseFloat(data.amount);
			User.findOne({ Username: userid }, (err, foundUser) => {
				if (err) {
					handle_mongo_error(err, data);
					res.send({
						success: false,
						message: "Error searching for that userid in MongoDB.",
						result: err
					});
				} else {
					let newUser = new User();
					newUser.Username = userid;
					if (foundUser) newUser = foundUser;
					newUser.Cash = newUser.Cash + amount;
					newUser.save().then(result => {
						res.send({
							success: true,
							message: "Successfully added $" + amount + " to " + userid + "'s account. " + newUser.Cash,
							result: result
						});
					});
				}
			});
		}
		
		/*
		if (1) {
			Part.find(req.body.args, (err, foundParts) => {
				if (err) {
					res.send({
						success: false,
						message: "Error while trying to find the part in MongoDB.",
						err
					})
				} else {
					//console.log("read:")
					//console.log(foundParts)
					res.send(foundParts)
				}
			})
		} else { // write
			if (req.body.args._id) {
				// if they provide an _id, then it's probably an update request
				Part.findOne({_id: req.body.args._id}, (err, foundPart) => {
					if (err) {
						console.log(err)
						console.log("error searching for part with provided _id")
						res.send({ success: false, err })
					} else {
						let newPart = new Part()
						if (foundPart) newPart = foundPart;
						for (key in req.body.args) {
							newPart[key] = req.body.args[key]
						}
						newPart.save().then(result => {
							//console.log("wrote:")
							//console.log(result)
							res.send({
								success: true,
								part: result
							})
						})
					}
				})
			} else {
				let newPart = new Part(req.body.args)
				newPart.save().then(result => {
					//console.log("wrote:")
					//console.log(result)
					res.send({
						success: true,
						part: result
					})
				})
			}
		}
		*/
	}
}