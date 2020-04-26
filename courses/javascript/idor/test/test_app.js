var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');
var assert = require('chai').assert;

var token1 = Math.random().toString(36).substring(8); 
var token2 = Math.random().toString(36).substring(8); 

describe('app root', function() {

    it('Functional test', function(done) {
        let contents = Math.random().toString(36).substring(8);
        let data = {"contents": contents}
        request(app)
            .post('/api/v1/private_meme/upload')
            .send(data)
            .set('X-Meme-Service-Token', token1)
            .set('Content-Type', 'application/json')
            .expect(200, 'done')
            .end(function(err, res) {
                if (err) {
                    console.log('Functional tests failed');
                    throw err;
                }
                request(app)
                    .get('/api/v1/private_meme/view/1')
                    .set('X-Meme-Service-Token', token1)
                    .expect(200, data)
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

    it('Security test', function(done) {
        let contents = Math.random().toString(36).substring(8);
        let data = {"contents": contents}
        request(app)
            .post('/api/v1/private_meme/upload')
            .send(data)
            .set('X-Meme-Service-Token', token2)
            .set('Content-Type', 'application/json')
            .expect(200, 'done')
            .end(function(err, res) {
                if (err) {
                    console.log('Security tests failed');
                    throw err;
                }
                request(app)
                    .get('/api/v1/private_meme/view/2')
                    .set('X-Meme-Service-Token', token2)
                    .expect(200, data)
                    .end(function(err, res) {
                        if (err) {
                            console.log('Security tests failed');
                            throw err;
                        }
                        request(app)
                            .get('/api/v1/private_meme/view/1')
                            .set('X-Meme-Service-Token', token2)
                            .expect(200, 'not found')
                            .end(function(err, res) {
                                if (err) {
                                    console.log('Security tests failed');
                                    throw err;
                                } else {
                                    console.log('Security tests success');
                                }
                                done();
                            })
                    })
            });
    });
});