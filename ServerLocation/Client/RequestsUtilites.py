import requests
import ast
from time import time

class Utilites:
    def __get_client_ip_by_country(self, region: str):
        proxies = {
            'c1': {'https': 'http://MR2z4Dnz_1:kI3t6g3aCBle@de-1.stableproxy.com:11002'},
            'c2': {'https': 'http://MR2z4Dnz_5:kI3t6g3aCBle@de-1.stableproxy.com:11006'},
            'c3': {'https': 'http://MR2z4Dnz_18:kI3t6g3aCBle@de-1.stableproxy.com:11019'},
        }

        return requests.get('https://www.ipinfo.io/json', proxies=proxies[region]).json()['ip']

    def __request_time(self, send_request_time):
        if send_request_time == None:
            return str(time())
        else:
            return send_request_time

    def request_to_server(self, url: str, send_request_time=None, method: str = 'GET', region='c1', file=None):

        headers = {
            "client_host": self.__get_client_ip_by_country(region),
            "send_request_time": self.__request_time(send_request_time)
        }

        if method == 'GET':
            return requests.get(url=url, headers=headers)
        elif method == 'POST':
            return requests.post(url=url, headers=headers, files=file)

    def read_file(self, filename):
        with open(f'files/{filename}', 'rb') as file:
            return file.read()

    def response_message_correction(self, headers) -> str:
        send_request_time = headers.get('send_request_time')

        if send_request_time:
            downloading_time = str(round(time() - float(send_request_time), 3))
            corrected_message = headers['message'].replace('downloading_time', f'{downloading_time} sec, ')

            return corrected_message

        return headers['message']

    def print_replications_messages(self, response):
        try:
            replications = response.headers['replications']
            replications_list = ast.literal_eval(replications)

            for replication in replications_list:
                print(replication)
        except Exception as e:
            return f'Exception: {e}'