import io
import socket
import sys
import datetime

class WSGIServer(object):
    """
    Simple implementation for WSGI server
    """

    address_family = socket.AF_INET6
    socket_type = socket.SOCK_STREAM
    queue_size = 5

    def __init__(self, server_address):
        # Creating a listening socket
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)
        # Setting up socket options
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind host and port
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(self.queue_size)
        # Host and portname
        host, port = self.listen_socket.getsockname()[:2]
        self.host = socket.getfqdn(host)
        self.port = port


    def set_app(self, application):
        """
        Attach application to server
        :param application:
        :return:
        """
        self.application = application

    def serve_forever(self):
        """
        Serving HTTP by server continuously
        :return:
        """
        listen_socket = self.listen_socket
        while True:
            self.client_connection, client_address = listen_socket.accept()
            # Handle a request per client and close the close, looping over and wait for another client
            self.handle_one_request()

    def handle_one_request(self):
        """

        :return:
        """
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode('utf-8')
        # Printing request data
        print(''.join('{}\n'.format(line) for line in request_data.splitlines()))
        # Parsing request
        self.parse_request(request_data)
        # Setting up env variables
        env = self.get_environ()
        # Getting a result back from application callable which will be part of response body
        result = self.application(env, self.start_response())
        # Construct a response which includes response body, header, env
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        # Break down the request line into components
        self.request_data, self.path, self.request_version = request_line.split()

    def get_environ(self):
        env = {}
        # Required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # Required CGI variables
        env['REQUEST_METHOD'] = self.request_method  # GET
        env['PATH_INFO'] = self.path  # /hello
        env['SERVER_NAME'] = self.server_name  # localhost
        env['SERVER_PORT'] = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', datetime.datetime.today().__str__()),
            ('Server', 'WSGIServer 0.2')
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {} \r\n'.format(status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            response_bytes = response.encode()
            self.client_connection.sendall(response_bytes)
        finally:
            self.client_connection.close()




