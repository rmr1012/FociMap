var express = require('express');
var router = express.Router();

router.get('/:render', function(req, res, next) {
	res.render('index', { "render" : req.params.render });
});

module.exports = router;
