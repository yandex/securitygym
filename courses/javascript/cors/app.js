const express = require('express');
const url = require('url');
const app = express();

app.use(express.json());

function generateCardNumber() {
    var numberArray = []
    const seed = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 
  
    for (var i = 0; i < 12; i++) {
      const item = seed[Math.floor(Math.random() * seed.length)]
      numberArray.push(item)
    }
  
    return "1337-"+numberArray.join('');
}

function generateResponseData(userId) {
    let generatedData = generateCardNumber();
    if (userId == null) {
        return {};    
    }
    return {'userId': userId, 'card_number': generatedData};
}

app.post('/', async (request, response) => {
    let userId = request.body.userId;
    let responseData = generateResponseData(userId);

    clientUrl = request.headers['referer'] || request.headers['origin'];
    if (clientUrl) {
        const urlObj = url.parse(clientUrl);
        const domain = `${urlObj.protocol}//${urlObj.host}`;
        response.header('Access-Control-Allow-Origin', domain);
        request.requestUrl = clientUrl;
    } else {
        response.header('Access-Control-Allow-Origin', '*');
    }
    response.header(
        'Access-Control-Allow-Headers',
        'Origin,Content-Type,Accept,X-HTTP-Method-Override,X-Requested-With'
    );
    response.header('Access-Control-Allow-Credentials', 'true');
    return response.send(responseData);
})

module.exports = app;
