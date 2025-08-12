const express = require('express')
const router = require('./router/router')
const app = express()
const port = 3000

app.use('/', router)

app.listen(port, () => {
  console.log(`🚀 Agentic API server listening at http://localhost:${port}`)
  console.log(`📊 Welcome page: http://localhost:${port}/`)
})
