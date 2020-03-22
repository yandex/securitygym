const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.urlencoded({
    extended: true
}));

app.get('/', (req, res) => {
    res.send(`
      <form action="/entry" method="POST">
        <div>
          <label for="message">Enter a message</label>
          <input id="message" name="message" type="text" />
        </div>
        <input type="submit" value="Submit" />
      </form>
    `);
  });

  app.post('/entry', (req, res) => {
    res.send(`Message received: ${req.body.message}`);
  });

module.exports = app;
