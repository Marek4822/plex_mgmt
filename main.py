from website import create_app
from waitress import serve
from website.env import host, local_address

app = create_app()
if __name__ == '__main__':
    serve(app, host=host, port=2137)
    # serve(app, host=local_address, port=2137)
    # app.run(host=local_address, debug=True, port=2137)
    