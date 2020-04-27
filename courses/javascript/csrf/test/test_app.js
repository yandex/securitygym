var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');
var HTMLParser = require('node-html-parser');

describe('app root', function() {
    it('Functional test', function(done) {
        let message = Math.random().toString(36).substring(7);
        request(app)
            .get('/')
            .expect(200)
            .end(function(err, res) {
                let Cookies = res.headers['set-cookie'].pop().split(';')[0];

                var root = HTMLParser.parse(res.text);
                var csrfToken = '';
                root.querySelectorAll('input').forEach(input => {
                    if (input.getAttribute('name') === "_csrf") {
                        csrfToken = input.getAttribute('value');
                    }
                });

                request(app)
                    .post('/entry')
                    .type('form')
                    .set({cookie: Cookies})
                    .send({
                        _csrf: csrfToken,
                        message: message
                    })
                    .expect(200)
                    .expect(function(res){
                        res.text.should.include(message);
                    })
                    .end(function(err, res) {
                        if (err) {
                            console.log('Functional tests failed');
                            throw err;
                        } else {
                            console.log('Functional tests success');
                        }
                        done();
                    })
            });
    });

    it('testing Security', function(done) {
        let message = Math.random().toString(36).substring(7);
        request(app)
            .get('/')
            .expect(200)
            .end(function(err, res) {
                let Cookies = res.headers['set-cookie'].pop().split(';')[0];

                var root = HTMLParser.parse(res.text);
                var csrfToken = '';
                root.querySelectorAll('input').forEach(input => {
                    if (input.getAttribute('name') === "_csrf") {
                        csrfToken = input.getAttribute('value');
                    }
                });
                csrfToken = Math.random().toString(36).substring(csrfToken.length);

                request(app)
                    .post('/entry')
                    .type('form')
                    .set({cookie: Cookies})
                    .send({
                        _csrf: csrfToken,
                        message: message
                    })
                    .expect(function(res){
                        res.statusCode.should.not.equals(200);
                        res.text.should.not.include(message);
                    })
                    .end(function(err, res) {
                        if (err) {
                            console.log('Security tests failed');
                            throw err;
                        } else {
                            console.log('Security tests success');
                        }
                        done();
                    })
            });
    });
});

