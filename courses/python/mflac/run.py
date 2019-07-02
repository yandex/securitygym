from mflac.vuln_app import create_app

if __name__ == '__main__':
    config = {"VULNERABLE": True}
    app = create_app(config)
    app.run(debug=True)