const express = require('express');
const app = express();


app.get('/redirect', async (request, response) => {
    const url = request.query.url;
    return response.redirect(url);
})

module.exports = app;
