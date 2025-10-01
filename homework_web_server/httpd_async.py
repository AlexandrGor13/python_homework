from datetime import datetime
import socket
import sys
import os
import asyncio

import aiofiles
import pytz

import parse

HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = './www'  # root folder for static files


async def handle_request(reader, writer):
    try:
        request = await reader.read(1024)
        request_data = parse.parse_request(request.decode())

        method = request_data.get("method")
        if method in ['GET', 'HEAD']:
            # create response and sendit back
            response = await generate_response(request_data)
        else:
            response = b'HTTP/1.1 405 Method Not Allowed'
        writer.write(response)
        await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def generate_response(request_data):
    method = request_data.get("method")
    path = DOCUMENT_ROOT + request_data.get("path")
    index = 'index.html'
    response = b'HTTP/1.1 200 OK\r\n'
    try:
        if not os.path.exists(path):
            raise FileExistsError('File not found')
        if os.path.isdir(path):
            path += index if path[-1] == '/' else '/' + index
        _, ext = os.path.splitext(path)
        async with aiofiles.open(path, 'rb') as f:
            file = await f.read()
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


async def start_server():
    server = await asyncio.start_server(handle_request, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f'Сервер запущен на {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    if '-r' in sys.argv:
        DOCUMENT_ROOT = sys.argv[sys.argv.index('-r') + 1]
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print('Сервер остановлен')

# testing
# sh ab -n 1000 -c 10 http://localhost:8080/index.html

# wrk -t12 -c400 -d30s http://localhost:8080/index.html
#
#
# Running 30s test @ http://localhost:8080/index.html
#   12 threads and 400 connections
#   Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency   172.15ms   23.71ms 540.38ms   79.63%
#     Req/Sec   184.42     58.83   333.00     68.30%
#   66083 requests in 30.02s, 16.89MB read
# Requests/sec:   2201.21
# Transfer/sec:    576.10KB
