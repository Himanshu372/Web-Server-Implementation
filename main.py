import sys
from constants import HOST, PORT
from wsgi_server import WSGIServer

def maker_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Another argument required in the format of WSGI application "
             "object as module(djangoapp):application(local app)")
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = maker_server((HOST, PORT), application)
    print('WSGIServer: Serving HTTP on port {}'.format(PORT))
    httpd.serve_forever()