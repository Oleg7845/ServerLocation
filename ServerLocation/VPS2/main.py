import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.requests import Request
from fastapi.responses import Response
from ServiceIP import ServiceIP
from ReplicationFiles import Replication
from FileExists import Exists
from datetime import datetime
from time import time


app = FastAPI()
ServiceIP = ServiceIP()
Replication = Replication()
Exists = Exists()
SERVER_INFO = ServiceIP.SERVER_INFO


@app.post('/replication/{filename}') #Download file from the Server
async def replication_file(response: Response, request: Request, filename: str, file: UploadFile = File(...)):
    send_request_time = float(request.headers["send_request_time"])  # When client sent request

    try:
        with open(f'downloaded_files/{filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

            response.headers['message'] = f'{SERVER_INFO["server_name"]} ' \
                                          f'{SERVER_INFO["server_city"]} ' \
                                          f'{SERVER_INFO["server_ip"]}, ' \
                                          f'{round(time() - send_request_time, 2)} sec, ' \
                                          f'{datetime.now()}, ' \
                                          f'{SERVER_INFO["server_url"]}upload/{filename}'

            return 'Replication successfully!'

    except Exception as e:
        response.headers['message'] = f'Server exception: {e}'
        return 'Server exception...'


@app.post('/upload/{filename}') #Download file from the Server
async def upload_file(response: Response, request: Request, filename: str, file: UploadFile = File(...)):
    client_headers = request.headers  # request.client.host //Get Client IP-address
    nearest_server_name = ServiceIP.get_nearest_server(client_headers["client_host"]) # get nearest to client server
    send_request_time = float(client_headers["send_request_time"]) # When client sent request
    file_path = f'downloaded_files/{filename}'# Path to file by name

    try:
        if Exists.check(filename):
            if nearest_server_name == ServiceIP.SERVER_NAME:
                with open(file_path, 'wb') as buffer:
                    shutil.copyfileobj(file.file, buffer)

                    Replication.replicate(send_request_time, filename, ServiceIP)
                    replication_responses = Replication.RESPONSES_LIST

                    replications = []

                    for res in replication_responses:
                        msg = res.headers['message']
                        print(f'{ServiceIP.SERVER_NAME} -> ' + msg)
                        replications.append(f'{ServiceIP.SERVER_NAME} -> ' + msg)

                    response.headers['replications'] = str(replications)

                    response.headers['message'] = f'{SERVER_INFO["server_name"]} ' \
                                                  f'{SERVER_INFO["server_city"]} ' \
                                                  f'{SERVER_INFO["server_ip"]}, ' \
                                                  f'{round(time() - send_request_time, 2)} sec, ' \
                                                  f'{datetime.now()}, ' \
                                                  f'{SERVER_INFO["server_url"]}upload/{filename}'
                    return 'Uploading successfully!'
            else:
                for server in ServiceIP.SERVERS_LIST:
                    if server['server_name'] == nearest_server_name:
                        response.headers['message'] = 'redirect'
                        response.headers['url'] = f'{server["server_url"]}upload/{filename}'
                        response.headers['send_request_time'] = str(send_request_time)
                        return 'Redirection to other Server...'
        else:
            response.headers['message'] = f'Files "{filename}" already exists!'
            return 'Files already exists!'

    except Exception as e:
        response.headers['message'] = f'Server exception: {e}'
        return 'Server exception...'


@app.get('/download/{filename}') #Download file from the Server
def download_file(response: Response, request: Request, filename: str):
    client_headers = request.headers  # request.client.host //Get Client IP-address
    nearest_server_name = ServiceIP.get_nearest_server(client_headers["client_host"])  # get nearest to client server
    send_request_time = client_headers["send_request_time"] # When client sent request (type as <str>)

    try:
        file_path = f'downloaded_files/{filename}'
        if nearest_server_name == ServiceIP.SERVER_NAME:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as bytes:
                    file = bytes.read()

                    headers = {'message':
                                   f'{SERVER_INFO["server_name"]} '
                                   f'{SERVER_INFO["server_city"]} '
                                   f'{SERVER_INFO["server_ip"]}, '
                                   f'downloading_time'
                                   f'{datetime.now()}, '
                                   f'{SERVER_INFO["server_url"]}upload/{filename}',
                               'filename': filename,
                               'send_request_time': send_request_time}

                    return Response(content=file, media_type='image/jpg', headers=headers)
        else:
            for server in ServiceIP.SERVERS_LIST:
                if server['server_name'] == nearest_server_name:
                    response.headers['message'] = 'redirect'
                    response.headers['url'] = f'{server["server_url"]}download/{filename}'
                    response.headers['filename'] = filename
                    response.headers['send_request_time'] = send_request_time
                    return 'Redirection to other Server...'

    except Exception as e:
        response.headers['message'] = f'Server exception: {e}'
        return 'Server exception...'


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.2', port=8002, reload=True)
