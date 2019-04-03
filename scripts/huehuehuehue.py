import socket
import json

HOST = '172.28.128.5'  # Standard loopback interface address (localhost)
PORT = 80  # Port to listen on (non-privileged ports are > 1023)


def handle_post_request(request_data):
    return 0


def handle_get_request(request_data):
    if get_url_from_data(request_data) == "/api/":
        return json.dumps(
            {
                "object": {
                    "Mart": {
                        "isHomo": True,
                        "RelationWith": "Max"
                    },
                    "Max": {
                        "isHomo": True,
                        "RelationWith": "Mart"
                    }
                }
            }
        )


def get_url_from_data(request_data):
    return request_data.split()[1].decode("utf-8")


def get_request_type(request_data):
    return request_data.split()[0].decode("utf-8")


def handle_request(request_data):
    request_type = get_request_type(request_data)

    if request_type == "POST":
        return handle_get_request(request_data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(0)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(4096)
        conn.send(bytes('HTTP/1.0 200 OK\r\n', 'utf-8'))
        conn.send(bytes('Access-Control-Allow-Origin: *', 'utf-8'))
        conn.send(bytes('\r\n\r\n', 'utf-8'))
        conn.send(bytes(handle_request(data), 'utf-8'))
        conn.close()
        s.close()
