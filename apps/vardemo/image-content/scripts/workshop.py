#!/usr/bin/env python3
import socket
import time
import os
import datetime

server_status = 'Starting'

def main():
    # Define the port on which the server will listen
    port = int(os.getenv('PORT', 8080))
    requests_file = os.getenv('REQUESTS_FILE', '/data/requests.txt')
    startup_delay = int(os.getenv('STARTUP_DELAY', 5))
    envs = []
    cm_vars = []
    for name, value in os.environ.items():
        envs.append({'name': name, 'value': value})
        if name.startswith('CM_VAR_'):
            cm_vars.append({'name': name, 'value': value})

    # Sort the CM_VAR_ vars by name
    envs = sorted(envs, key=lambda x: x['name'])
    cm_vars = sorted(cm_vars, key=lambda x: x['name'])
    kill = False
    container_start_time = time.ctime()

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Get the hostname of the server
    host = socket.gethostname()

    # Bind the socket to the host and port
    server_socket.bind(("0.0.0.0", port))

    # Listen for incoming connections
    server_socket.listen(5)

    # Time delay to simulate a slow start
    log(f"Starting application with a delay of {startup_delay} seconds")
    
    # Start background timer to change server_status to running in main loop after the delay
    def set_server_status() -> None:
        time.sleep(startup_delay)
        global server_status
        server_status = 'Running'
        log("Server status changed to Running")
   
    import threading
    threading.Thread(target=set_server_status).start()

    log(f"Container is listening on port { port}")

    while True:
        # Establish connection with client
        client_socket, addr = server_socket.accept()

        # Connection received from client
        log("Got a connection from %s" % str(addr))

        # Data received from client
        data = process_incomming_data(client_socket.recv(1024))

        
            # if line.startswith('X-Forwarded-For: ') and not source_ip:
            #     source_ip = line.split(' ')[1]
            # if line.startswith('X-Real-IP: '):
            #     source_ip = line.split(' ')[1]

        source_ip = str(addr[0])
        source_port = str(addr[1])
        if 'X-Forwarded-For' in data['headers']:
            source_ip = data['headers']['X-Forwarded-For'].split(',')[0]
        if 'X-Real-IP' in data['headers']:
            source_ip = data['headers']['X-Real-IP']
        
        log(f"Received data from client:\n{data.decode('ascii')}\n")

        response, kill, unhealthy = generate_response(data, server_status, container_start_time, requests_file, host, port, source_ip, source_port, envs, cm_vars)

        if unhealthy:
            response['unhealthy_duration']
            response['body'] += f"\n!!! THIS CONTAINER IS UNHEALTHY for {response['unhealthy_duration']} seconds !!!\n"
            if server_status == 'Running':
                server_status = 'Unhealthy'
                log(f"Server status changed to Unhealthy for {response['unhealthy_duration']} seconds")
                thre

            else:
                log(f"Server status remains Unhealthy for {response['unhealthy_duration']} seconds")

        if kill:
            response['body'] += "\n!!! THIS CONTAINER WILL BE KILLED !!!\n"
        response_headers = {
            'Content-Type': 'text/text; encoding=utf8',
            'Content-Length': len(response['body']),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK' # this can be random

        # sending all this stuff
        response = f"{response_proto} {response_status} {response_status_text}\r\n"
        client_socket.sendall(response.encode())
        client_socket.sendall(response_headers_raw.encode())
        client_socket.sendall(b'\r\n') # to separate headers from body
        client_socket.send(response['body'].encode(encoding="utf-8"))

        # Close the connection
        client_socket.close()
        if kill:
            break
    log("Stopping application")
    server_socket.close()


def generate_response(data: dict, server_status: str, container_start_time: str, requests_file: str, host: str, port: int, source_ip: str, source_port: str, envs: dict, cm_vars: dict) -> tuple(str, bool, bool):
    kill = False
    unhealthy = False
    response = {
        'body': f"Server status: {server_status}\n",
        'unhealthy_duration': 0
    }
    
    if server_status != 'Running':


    if data['path'] == '/':
        response['body'] += "Welcome to the VarDemo app\n
        


    if server_status == 'Unhealthy':
        response['unhealthy_duration'] = int(time.time() - time.mktime(time.strptime(container_start_time)))
    response['body'] += f"Host: {host}\n"
    response['body'] += f"Port: {port}\n"
    response['body'] += f"Source IP: {source_ip}\n"
    response['body'] += f"Source Port: {source_port}\n"
    response['body'] += f"Method: {data['method']}\n"
    response['body'] += f"Path: {data['path']}\n"
    response['body'] += f"Headers:\n"
    for key, value in data['headers'].items():
        response['body'] += f"  {key}: {value}\n"
    response['body'] += f"Body: {data['body']}\n"
    response['body'] += f"Requests: {requests(requests_file)}\n"
    response['body'] += f"Environment variables:\n"
    for env in envs:
        response['body'] += f"  {env['name']}: {env['value']}\n"
    response['body'] += f"ConfigMap variables:\n"
    for cm_var in cm_vars:
        response['body'] += f"  {cm_var['name']}: {cm_var['value']}\n"

    if 'KILL' in data['path']:
        kill = True
    if 'UNHEALTHY' in data['path']:
        unhealthy = True
    return response, kill, unhealthy


def process_incomming_data(incomming) -> dict:
    data_lines = incomming.decode('ascii').split('\n')
    data = {
        'method': data_lines[0].split(' ')[0],
        'path': data_lines[0].split(' ')[1],
        'headers': {},
        'body': ''
    }
    for line in data_lines:
        if line == '':
            break
        if ':' in line:
            key, value = line.split(':', 1)
            data['headers'][key] = value

    if data['method'] == 'POST':
        data['body'] = data_lines[-1]
    return data


def requests(requests_file:str) -> int:
    if not os.path.exists(requests_file):
        with open(requests_file, 'w') as f:
            f.write('0')
    with open(requests_file, 'r') as f:
        requests = int(f.read())
    requests += 1
    with open(requests_file, 'w') as f:
        f.write(str(requests))
    return requests


def log(msg):
    print(f'{now()} {msg}')


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    main()

