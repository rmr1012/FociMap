var express = require('express');
var fs = require('fs');
var router = express.Router();

router.get('/:render', function(req, res, next) {
	res.render('index', { "render" : req.params.render });
});

router.post('/upload', function(req, res, next) {
	console.log("uploading " + req.body.id);
	let buf = Buffer.from(req.body.data, 'base64');
	let file = req.body.id + '_' + req.body.index + '.jpg'
	let path = './public/images/' + file;
	fs.writeFile(path, buf, function(err) {
		if (err) {
			console.log("failed to upload " + file);
			return res.end("failed");
		}
		let spawn = require('child_process').spawn;
		let pyproc = spawn('python3', ['./public/py/parallel.py', path]);
		pyproc.stderr.on('data', function(data) {
			console.log(data.toString());
			return res.end("failed");
		});
		pyproc.stdout.on('data', function(data) {
			console.log(data.toString('utf8'));
		});
		pyproc.stdout.on('end', function(data) {
			return res.end("success");
		});
	});
});

router.post('/url', function(req, res, next) {
	console.log(req.body);
	let spawn = require('child_process').spawn;
	let jsonfile = './public/json/' + req.body.id + '.json';
	let depthfile = './public/images' + req.body.id + '-depth.jpg'
	let data = JSON.stringify(req.body);
	fs.writeFile(jsonfile, data, function(err) {
		if (err) {
			console.log("failed to write " + jsonfile);
			return res.end("failed");
		}
		let pyproc = spawn('python3', ['./public/py/serial.py', "8032068921399739550", depthfile]);
		pyproc.stderr.on('data', function(data) {
			return res.end("failed");
		});
		pyproc.stdout.on('data', function(data) {
			console.log(data.toString('utf8'));
		});
		pyproc.stdout.on('end', function(data) {
			return res.end("success");
		});
	});
});

module.exports = router;
