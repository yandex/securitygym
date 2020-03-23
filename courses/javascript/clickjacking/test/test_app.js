var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');

describe('app root', function() {
    it('Functional test', function(done) {
        request(app)
            .get('/payform')
            .expect(200)
            .end(function(err, res) {
                if (err) {
                    console.log('Functional tests failed');
                    throw err;
                } else {
                    console.log('Functional tests success');
                }
                done();
            });
    });

    it('testing Security', function(done) {
        request(app)
            .get('/payform')
            .expect(200)
            .expect(function(res){
                res.headers.should.to.have.property('x-frame-options');
                ['SAMEORIGIN', 'DENY'].should.to.include(res.headers['x-frame-options']);
            })
            .end(function(err, res){
                if (err) {
                    console.log('Security test failed: x-frame-options header is not properly set');
                    throw err;
                } else {
                    console.log('Security test success');
                }
                done();
            });
    });
});

