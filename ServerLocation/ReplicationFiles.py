import requests
import threading
from ServiceIP import ServiceIP


class Replication:
    def __init__(self):
        self.RESPONSES_LIST = []

    def __get_file(self, filename: str):
        with open(f'downloaded_files/{filename}', 'rb') as file:
            return file.read()

    def __send_file(self, send_request_time: float, file: str, filename: str, server: dict):
        try:
            headers = {"send_request_time": str(send_request_time)}

            url = f'{server["server_url"]}replication/{filename}'
            response = requests.post(url=url, headers=headers, files={'file': file})
            self.RESPONSES_LIST.append(response)
        except Exception as e:
            return f'Requests exception: {e}'

    def replicate(self, send_request_time: float, filename: str, service_ip: ServiceIP):
        self.RESPONSES_LIST = []
        threads_list = []
        file = self.__get_file(filename)

        for server in service_ip.SERVERS_LIST:
            if server['server_name'] != service_ip.SERVER_NAME:
                thread = threading.Thread(target=self.__send_file, args=(send_request_time, file, filename, server), name=server['server_name'])
                threads_list.append(thread)
                thread.start()

        for i in threads_list:
            i.join()
