var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');

describe('app root', function() {
    it('Functional test', function(done) {
        let url = Math.random().toString(36).substring(7) + '/'+ Math.random().toString(36).substring(7);

        request(app)
            .get('/redirect?url='+url)
            .expect(302)
            .expect(function(res) {
                res.headers.should.have.property('location', url)

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

    it('Security test', function(done) {
        let url = 'https://'+Math.random().toString(36).substring(7) + '/'+ Math.random().toString(36).substring(7);

        request(app)
            .get('/redirect?url='+url)
            .expect(function(res) {
                res.headers.should.not.have.property('location', url)

            })
            .end(function(err, res) {

                if (err) {
                    console.log('Security test failed');
                    throw err;
                } else {
                    console.log('Security tests success');
                }
                done();
            });
    });
});

