import socket
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def server_status():
    return 'Proxy is ready!'


@app.route('/forward', methods=['GET', 'POST'])
def forward():

    host = request.args.get('host')
    port = request.args.get('port', type=int)
    content = request.get_data()

    if host is None:
        return "Error! GET parameter 'host' needs to be specified."

    if port is None:
        return "Error! GET parameter 'port' needs to be specified."

    if content == b'':
        return "No HTTP body found. Nothing to forward."

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.settimeout(10)
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

            return f"Error your target '{host}:{port}' refused the connection"
