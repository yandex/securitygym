var app = require('../app.js');
var should = require('chai').should();
var request = require('supertest');

describe('app root', function() {
    it('Functional test', function(done) {
        let name = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({username:name})
            .expect(200)
            .expect(function(res) {
                res.text.should.to.include('<b>'+name+'</b>');
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

    it('testing SSTI', function(done) {
        let a = Math.floor(Math.random() * 1000);
        let b = Math.floor(Math.random() * 1000);
        request(app)
            .post('/')
            .send({username:'{{='+a.toString()+'*'+b.toString()+'}}'})
            .expect(200)
            .expect(function(res) {
                res.text.should.not.to.include((a*b).toString());
            })
            .end(function(err, res) {
                if (err) {
                    console.log('Security test failed: SSTI exists');
                    throw err;
                } else {
                    console.log('Security test success: SSTI pathed');
                }
                done();
            });
    });

    it('testing XSS', function(done) {
        let tag = Math.random().toString(36).substring(3);
        let name = Math.random().toString(36).substring(7);
        request(app)
            .post('/')
            .send({username:'<'+tag+'>'+name})
            .expect(200)
            .expect(function(res) {
                res.text.should.not.to.include('<'+tag+'>');
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

