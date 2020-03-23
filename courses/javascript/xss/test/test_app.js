var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');

describe('app root', function() {
    it('Functional test', function(done) {
        let name = Math.random().toString(36).substring(7);
        request(app)
            .post('/hello')
            .type('form')
            .send({username:name})
            .expect(200)
            .expect(function(res) {
                res.text.should.to.include(`{"username":"${name}"}`);
                res.text.should.to.include("Hello, "+name);
                res.text.should.to.include(`<input type="text" name="username" value="${name}"`);
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Functional test failed');
                    throw err;
                } else {
                    console.log('Function tests success');
                }
                done();
            });
    });

    it('testing XSS', function(done) {
        let tag = '<'+Math.random().toString(36).substring(3)+'>';
        let name = Math.random().toString(36).substring(7);
        let quote_str = Math.random().toString(36).substring(2)+'"'+Math.random().toString(36).substring(2);
        request(app)
            .post('/hello')
            .type('form')
            .send({username:tag+name+quote_str})
            .expect(function(res) {
                res.text.should.not.to.include(tag);
                res.text.should.not.to.include(quote_str);
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Security test failed: XSS exists');
                    throw err;
                } else {
                    console.log('Security test success: XSS pathed');
                }
                done();
            });
    });
});

