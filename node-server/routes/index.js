var express = require('express');
var fs = require('fs');
var router = express.Router();

router.get('/:id', function(req, res, next) {
	res.render('index', { "id" : req.params.id });
});

router.post('/upload', function(req, res, next) {
	let buf = Buffer.from(req.body.data, 'base64');
	let file = req.body.id + '_' + req.body.index + '.jpg'
	let path = './public/images/' + file;
	console.log("[UPLOAD] " + file);
	fs.writeFile(path, buf, function(err) {
		if (err) {
			console.log("[UPLOAD FAILURE] " + file);
			console.log(err);
			res.status(500);
			return res.end();
		}
		let spawn = require('child_process').spawn;
		let pyproc = spawn('python3', ['./public/py/parallel.py', path]);
		pyproc.stderr.on('data', function(data) {
			console.log("[PYTHON ERROR] " + file);
			console.log(data.toString('utf8'));
			res.status(500);
			return res.end();
		});
		pyproc.stdout.on('data', function(data) {
			console.log(data.toString('utf8'));
		});
		pyproc.stdout.on('end', function(data) {
			res.status(200);
			return res.end();
		});
	});
});

router.post('/url', function(req, res, next) {
	let spawn = require('child_process').spawn;
	let jsonfile = './public/json/' + req.body.id + '.json';
	let depthfile = './public/images/' + req.body.id + '-depth.png'
	let data = JSON.stringify(req.body);
	console.log("[WRITE] " + jsonfile);
	fs.writeFile(jsonfile, data, function(err) {
		if (err) {
			console.log("[WRITE FAILURE] " + jsonfile);
			res.status(500);
			return res.end();
		}
		let pyproc = spawn('python3', ['./public/py/serial.py', req.body.id, depthfile]);
		pyproc.stderr.on('data', function(data) {
			console.log("[PYTHON ERROR] " + depthfile);
			console.log(data.toString('utf-8'));
			res.status(500);
			return res.end();
		});
		pyproc.stdout.on('data', function(data) {
			console.log(data.toString('utf8'));
		});
		pyproc.stdout.on('end', function(data) {
			res.status(200);
			return res.end();
		});
	});
});

module.exports = router;
