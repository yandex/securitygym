from app import create_app

if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', debug=True)
