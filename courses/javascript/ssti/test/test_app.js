var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');

describe('app root', function() {
    it('should return Hello World!', function(done) {
        request(app)
            .get('/')
            .expect(200)
            .expect(function(res) {
                console.log('SUCCESS Hello World!');
                res.text.should.equal('Hello World!');
            })
            .end(function(err, res) {
                if (err) throw err;
                done();
            });
    });
});

