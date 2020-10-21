import ssl
import socket

from flask import Flask, request

app = Flask(__name__)


class InvalidArgsException(Exception):
    '''
    Custom exception class.
    '''


def get_args(request):
    '''
    Parses the specified arguments during a POST request. It verifies whether the remote
    host and port arguments were set, whether the request body contains content and whether
    SSL connections should be used.

    Paramaters:
        request             (request)               Incoming HTTP request

    Returns:
        remote              (list[string])          Remote host, port, content and ssl setting
    '''
    host = request.args.get('host')
    port = request.args.get('port', type=int)
    use_ssl = request.args.get('ssl', default=False)

    content = request.get_data()

    if host is None:
        raise InvalidArgsException("Error! GET parameter 'host' needs to be specified.\n")

    if port is None:
        raise InvalidArgsException("Error! GET parameter 'port' needs to be specified.\n")

    if content == b'':
        raise InvalidArgsException("No HTTP body found. Nothing to forward.\n")

    return [host, port, content, use_ssl]


def prepare_socket(use_ssl):
    '''
    Prepare the socket for the connection.

    Parameters:
        use_ssl             (boolean)               Decides whether to use ssl

    Returns:
        socket              (socket)                Socket object
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        s = ssl.wrap_socket(s, cert_reqs=ssl.CERT_NONE)

    s.settimeout(15)
    return s


@app.route('/')
def server_status():
    '''
    When just querying the root of the server, we return a static banner.

    Paramaters:
        None

    Returns:
        banner              (string)                Server banner
    '''
    return 'Proxy is ready!\n'


@app.route('/forward', methods=['GET', 'POST'])
def forward():
    '''
    Forward the POST body of a request to the specified remote host and return
    the result. The remote host, content and ssl option are all specified via
    URL paramaters.

    Paramaters:
        None

    Returns:
        content             (string)                Content received by the remote target
    '''

    try:
        host, port, content, use_ssl = get_args(request)

    except InvalidArgsException as e:
        return str(e)

    s = prepare_socket(use_ssl)
    target = (host, port)

    try:
        s.connect(target)
        s.sendall(content)

        master_data = b''
        while True:
            data = s.recv(1024)
            if len(data) <= 0:
                return master_data
            master_data += data

    except ConnectionRefusedError:
        return f"Target '{host}:{port}' refused the connection.\n"

    except socket.timeout:
        return f"Target '{host}:{port}' did not respond within 15 seconds.\n"

    except ConnectionResetError:
        return f"Target '{host}:{port}' resetted the connection.\n"

    except Exception as e:
        return "Unexpected exception: " + str(e) + "\n"
