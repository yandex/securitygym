const express = require('express');
const doT = require('dot');
const app = express();

app.use(express.json());

var orders = [{'title': 'test_product_1', 'price': 20},
    {'title': 'test_product_2', 'price': 45}]

function generateBadge(username) {
    return `Hi, <b>${username}</b>`;
}

async function renderMail(username) {
    let text = `
    {{~it.orders :order:index}}
    <div>{{!order.title}} - {{=order.price}} rub.</div>
    {{~}}
    `;
    let render = doT.template(generateBadge(username) + "<div>" + text + "</div>");
    return render({'orders': orders});
}

app.post('/', async (request, response) => {
    let username = request.body.username;

    return response.send(await renderMail(username));
})

module.exports = app;
