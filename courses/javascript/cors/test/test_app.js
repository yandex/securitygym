var app = require('../app.js');
var request = require('supertest');
var assert = require('chai').assert;
var should = require('chai').should();

const validRegex = /(^https:\/\/service\.yandex\.(ru|by|ua|kz|com|com\.tr|az)$)|(^https:\/\/(www\.)?ya\.(ru)$)|(^https:\/\/(www\.)?yandex\.(ru|by|ua|kz|com|com\.tr)$)/;
 
describe('Application Tests', function() {
    let SECURITY_FAILED = false;
    it('Functional test', function(done) {
        let validDomain = 'https://service.yandex.ru';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Origin', validDomain)
            .expect(200)
            .expect(function(res) {
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                res.headers.should.exists;
                res.headers.should.to.have.property('access-control-allow-origin');
                corsOriginHeader.should.to.be.oneOf([validDomain, '*']);
                res.text.should.to.include('card_number');
                corsOriginHeader.should.not.to.equal('');
                corsOriginHeader.should.not.to.equal(null);
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Functional test failed for ' + validDomain);
                    throw err;
                } else {
                    console.log('Function tests success');
                }
                done();
            });
    });

    it('Testing origin fix', function(done) {
        if (SECURITY_FAILED) {
            this.skip();
        }
        let randomDomain = 'https://' + Math.random().toString(36).substring(8)+'.ru';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Origin', randomDomain)
            .expect(200)
            .expect(function(res) {
                res.headers.should.exists;
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                if (corsOriginHeader !== undefined) {
                    corsOriginHeader.should.not.to.equal('*');
                    corsOriginHeader.should.not.to.contain(randomDomain);
                }
            })
            .end(function(err, res) {
                if (err) {
                    console.log('There is no validation for Origin header with ' + randomDomain);
                    SECURITY_FAILED = true;
                    throw err;
                } else {
                    console.log('Origin test passed with ' + randomDomain);
                }
                done();
            });
    });

    it('Testing referrer fix', function(done) {
        if (SECURITY_FAILED) {
            this.skip();
        }
        let randomDomain = 'https://' + Math.random().toString(36).substring(8)+'.com';
        let referer = randomDomain + '/service.yandex.ru';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Referer', referer)
            .set('Origin', randomDomain)
            .expect(200)
            .expect(function(res) {
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                if (corsOriginHeader !== undefined) {
                    corsOriginHeader.should.not.to.equal('*');
                    corsOriginHeader.should.not.to.contain(randomDomain);
                }
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Referer header could be used for bypass with ' + referer);
                    SECURITY_FAILED = true;
                    throw err;
                } else {
                    console.log('Referer test passed with ' + referer);
                }
                done();
            });
    });

    it('TLD fix test', function(done) {
        if (SECURITY_FAILED) {
            this.skip();
        }
        let uncontrollableTld = 'https://service.yandex.dev';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Origin', uncontrollableTld)
            .expect(200)
            .expect(function(res) {
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                if (corsOriginHeader !== undefined) {
                    res.text.should.to.include('card_number');
                    assert(validRegex.test(corsOriginHeader), 'Allowed origin doesnt match for regex');
                }
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Origin header could be used for bypass with ' + uncontrollableTld);
                    SECURITY_FAILED = true;
                    throw err;
                } else {
                    console.log('Origin test passed with ' + uncontrollableTld);
                }
                done();
            });
    });

    it('Subdomain fix test', function(done) {
        if (SECURITY_FAILED) {
            this.skip();
        }
        let subdomain = 'https://service.yandex.ru.' + Math.random().toString(36).substring(8) + '.ru';
        let randomId = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({userId:randomId})
            .set('Origin', subdomain)
            .expect(200)
            .expect(function(res) {
                let corsOriginHeader = res.headers['access-control-allow-origin'];
                if (corsOriginHeader !== undefined) {
                    res.text.should.to.include('card_number');
                    assert(validRegex.test(corsOriginHeader), 'Allowed origin doesnt match for regex');
                }
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Origin header could be used for bypass with ' + subdomain);
                    SECURITY_FAILED = true;
                    throw err;
                } else {
                    console.log('Origin test passed with ' + subdomain);
                }
                done();
            });
    });
});