from csrf.vuln_app import create_app

if __name__ == '__main__':
    config = {"VULNERABLE": False}
    app = create_app(config)
    app.run(debug=True)