var express = require('express');
var router = express.Router();
var _ = require('lodash');
var path = require('path');
var Multer = require('multer');
var request = require('request');
var CXRStorage = require('../helpers/CXRStorage');


var storage = CXRStorage();

// mutter
var fileFilter = function(req, file, cb) {
	var allowedMimes = ['image/jpeg', 'image/pjpeg', 'image/png', 'image/gif'];

	if (_.includes(allowedMimes, file.mimetype)) {
		cb(null, true);
	} else {
		cb(new Error('Invalid file type. Only jpg, png and gif image files are allowed.'));
	}
};

var mutter = Multer({
  storage: storage,
  limits: {
    files: 1,
    fileSize: 5 * 1024 * 1024 // no larger than 5mb
  },
  fileFilter: fileFilter
})

var default_body = {
	image_name: '',
}

/* GET home page. */
router.get('/', function(req, res, next) {
//   res.render('index', { title: 'Chest X-ray', cxr_field: 'cxr'});
	res.render('index', {cxr_field: 'cxr', body: default_body})
});

router.post('/upload', mutter.single('cxr'), function(req, res, next) {
	var file = req.file.filename;

	options = {
		uri: 'http://127.0.0.1:5002/cxr',
		method: 'POST',
		json: {
			image_name: file
		}
	}


	request(options, (err, result, body) => {
		if (err) { return console.log(err); }
		res.render('index', {cxr_field: 'cxr', body: body})
	})

});


module.exports = router;
