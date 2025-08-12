const express = require('express');
const { welcomeAPIMessage } = require('../controller/wellcome');

const router = express.Router();

router.get('/', welcomeAPIMessage);


module.exports = router;
