import socket

HOST = '172.28.128.5'  # Standard loopback interface address (localhost)
PORT = 80        # Port to listen on (non-privileged ports are > 1023)


def get_url_from_data(request_data):
    return request_data.split()[1].decode("utf-8")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(0)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(4096)
        url = get_url_from_data(data)
        print(url)
