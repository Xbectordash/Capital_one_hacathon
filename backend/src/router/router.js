const express = require('express')
const { welcomeAPIMessage } = require('../controller/wellcome')
const { healthCheck, apiStatus } = require('../controller/healthController')

const router = express.Router()

// Welcome page
router.get('/', welcomeAPIMessage)

// Health check endpoints
router.get('/health', healthCheck)
router.get('/api/status', apiStatus)

module.exports = router
