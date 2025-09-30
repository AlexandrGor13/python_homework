from datetime import datetime
import socket
import sys
import threading
import os

import pytz

import parse


HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = './www' #root folder for static files

def handle_request(client_socket):
    try:        
        request = client_socket.recv(1024)
        request_data = parse.parse_request(request.decode())          
        
        method = request_data.get("method")
        if method in ['GET', 'HEAD']:
            # create response and sendit back
            response = generate_response(request_data)            
        else:
            response = b'HTTP/1.1 405 Method Not Allowed'
        client_socket.sendall(response)
            
    finally:
        client_socket.close()
        

def generate_response(request_data):
    method = request_data.get("method")
    path = DOCUMENT_ROOT + request_data.get("path")
    headers = request_data.get("headers")
    index = 'index.html'
    response = b'HTTP/1.1 200 OK\r\n'
    try:
        if not os.path.exists(path):
            raise FileExistsError('File not found')
        if os.path.isdir(path):
            path += index if path[-1] == '/' else '/' + index
        _, ext = os.path.splitext(path)
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.swf']:
            with open(path, 'rb') as f:
                file = f.read()
        else:
            with open(path, 'r', encoding='utf-8') as f:
                file = f.read()
                file = file.encode()
        ext_dict = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "text/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".gif": "image/gif",
            ".jpeg": "image/jpeg",
            ".swf": "application/x-shockwave-flash",
        }
        response_headers_dict = {
            'Date': datetime.now(pytz.timezone("Europe/Moscow")).strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': 'MyWebServer',
            'Content-Length': len(file),
            'Content-Type': ext_dict.get(ext),
            'Connection': 'close'
        }
        response_headers = ''
        for key, value in response_headers_dict.items():
            response_headers += f'{key}: {value}\r\n'
        response_headers += '\r\n'
        response += response_headers.encode()
        if method == 'GET':
            response += file
    except FileExistsError:
        response = b'HTTP/1.1 404 Not Found\r\n'
    except IOError:
        response = b'HTTP/1.1 403 Forbidden\r\n'
    return response
    

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))      
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    if '-r' in sys.argv:
        DOCUMENT_ROOT = sys.argv[sys.argv.index('-r')+1]
    start_server()


#testing
#sh ab -n 1000 -c 10 http://localhost:8080/index.html

#wrk -t12 -c400 -d30s http://localhost:8080/index.html

# Running 30s test @ http://localhost:8080/index.html
#   12 threads and 400 connections
#   Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency     8.25ms   62.00ms   1.67s    98.21%
#     Req/Sec   276.71    293.35     1.66k    84.25%
#   55126 requests in 30.10s, 9.15MB read
#   Socket errors: connect 0, read 55127, write 0, timeout 26
# Requests/sec:   1831.53
# Transfer/sec:    311.22KB
