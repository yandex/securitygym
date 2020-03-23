const express = require('express');
const csrf = require('csurf');
const cookieParser = require('cookie-parser');
const app = express();

var csrfProtection = csrf({ cookie: true });
app.use(cookieParser());

app.get('/payform', csrfProtection, async (request, response) => {

    return response.send(`
    <form action='/pay' method='POST'>
        <input type='text' value='100' name='amount'/>
        <input type='submit' value='Send Payment'/>
        <input type="hidden" name="_csrf" value="${request.csrfToken()}" />
    </form>
    `);
});

app.post('/pay', csrfProtection, async (request, response) => {

    return response.send(`
    <b>Successful payment</b>
    `);
});

module.exports = app;
