"use strict";
var express = require('express');
var router = express.Router();

router.get('/:render', function(req, res, next) {
	res.render('index', { "render" : req.params.render });
});

router.post('/upload', function(req, res, next) {
	let buf = Buffer.from(req.body.data, 'base64');
	let file = req.body.id + '.jpg'
	let path = './public/images/' + file;
	fs.writeFile(path, buf, function(err) {
		if (err) {
			return res.send({ "status" : "failed" });
		}
		let spawn = require('child_process').spawn;
		let pyproc = spawn('python', ['./public/py/parallel.py', path]);
		pyproc.stderr.on('data', function(data) {
			return res.send({ "status" : "failed" });
		});
		pyproc.stdout.on('data', function(data) {
			console.log(data.toString('utf8'));
		});
		pyproc.stdout.on('end', function(data) {
			return res.send({ "status" : 200 });
		});
	});
});

router.post('/url', function(req, res, next) {
	let spawn = require('child_process').spawn;
	let jsonfile = './public/json/' + req.body.id + '.json';
	let depthfile = './public/images' + req.body.id + '-depth.jpg'
	fs.writeFile(jsonfile, req.body, function(err) {
		let pyproc = spawn('python', ['./public/py/serial.py', jsonfile, depthfile]);
		pyproc.stderr.on('data', function(data) {
			return res.send({ "status" : "failed" });
		});
		pyproc.stdout.on('data', function(data) {
			console.log(data.toString('utf8'));
		});
		pyproc.stdout.on('end', function(data) {
			return res.send({ "status" : 200 });
		});
	});
});

module.exports = router;
