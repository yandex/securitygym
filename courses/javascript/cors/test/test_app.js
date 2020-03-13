var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');
var assert = require('chai').assert;

const validRegex = /(^https:\/\/service\.yandex\.(ru|by|ua|kz|com|com\.tr|az)$)|(^https:\/\/(www\.)?ya\.(ru)$)|(^https:\/\/(www\.)?yandex\.(ru|by|ua|kz|com|com\.tr)$)/;
 
describe('app root', function() {

    it('Functional test', function(done) {
        let randomId = Math.random().toString(36).substring(8)+'.com';
        request(app)
            .post('/')
            .send({userId:randomId})
            .expect(200)
            .expect(function(res) {
                res.text.should.to.include('card_number');
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                corsOriginHeader.should.not.to.equal('');
                corsOriginHeader.should.not.to.equal(null);
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

    it('Testing referrer fix', function(done) {
        let randomDomain = 'https://' + Math.random().toString(36).substring(8)+'.com';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Referer', randomDomain)
            .expect(200)
            .expect(function(res) {
                res.text.should.to.include('card_number');
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                // console.log(corsOriginHeader);
                corsOriginHeader.should.not.to.equal('*');
                corsOriginHeader.should.not.to.contain(randomDomain);
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Referer header could be used for bypass');
                    throw err;
                } else {
                    console.log('Referer test passed');
                }
                done();
            });
    });

    it('Testing origin fix', function(done) {
        let randomDomain = 'https://' + Math.random().toString(36).substring(8)+'.io';
        // console.log(randomDomain);
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Origin', randomDomain)
            .expect(200)
            .expect(function(res) {
                res.text.should.to.include('card_number');
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                console.log(corsOriginHeader);
                corsOriginHeader.should.not.to.equal('*');
                corsOriginHeader.should.not.to.contain(randomDomain);
            })
            .end(function(err, res) {
                if (err) {
                    console.log('There is no validation for Origin header');
                    throw err;
                } else {
                    console.log('Origin test passed');
                }
                done();
            });
    });

    it('Generic fix test', function(done) {
        let randomDomain = 'https://' + Math.random().toString(36).substring(8)+'.dev';
        let uncontrollableTld = 'https://evil.yandex.dev';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Origin', uncontrollableTld)
            .set('Referer', uncontrollableTld)
            .expect(200)
            .expect(function(res) {
                res.text.should.to.include('card_number');
                //console.log(res.text);
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                // console.log(corsOriginHeader);
                // corsOriginHeader.should.not.to.equal('*');
                // corsOriginHeader.should.not.to.contain(randomDomain);
                // corsOriginHeader.should.not.to.contain(uncontrollableTld);
                assert(validRegex.test(corsOriginHeader), 'Allowed origin doesnt match for regex');
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Origin header could be used for bypass');
                    throw err;
                } else {
                    console.log('Origin test passed');
                }
                done();
            });
    });
});