from RequestsUtilites import Utilites

class Console:
    def __init__(self):
        self.__Utilites = Utilites()
        self.__COMMANDS = [
            {'c1': 'Set country region as America'},
            {'c2': 'Set country region as Europe'},
            {'c3': 'Set country region as Asia'},
            {'commands': 'Print all commands'},
            {'exit': 'Exit program'},
        ]

    def __print_commands(self):
        for command in self.__COMMANDS:
            for key, value in command.items():
                print(f'{key} - {value}')
        print('')

    def run(self):
        while True:
            inp = input('Enter command or url: ')

            if inp == 'commands':
                self.__print_commands()
            elif inp == 'exit':
                return
            elif inp.split('/')[0] == 'http:' or inp.split('/')[0] == 'https:':
                URL = inp
                REGION = input('Enter region: ')

                filename = URL.split('/')[-1]
                action = URL.split('/')[-2]

                try:
                    if action == 'upload':
                        response = self.__Utilites.request_to_server(method='POST', url=URL, region=REGION, file={'file': self.__Utilites.read_file(filename)})
                        headers = response.headers

                        if headers['message'] == 'redirect':
                            response2 = self.__Utilites.request_to_server(method='POST', url=headers['url'], send_request_time=headers['send_request_time'], region=REGION, file={'file': self.__Utilites.read_file(filename)})
                            print(self.__Utilites.response_message_correction(response2.headers))
                            self.__Utilites.print_replications_messages(response2)
                        else:
                            print(self.__Utilites.response_message_correction(headers))
                            self.__Utilites.print_replications_messages(response)

                    elif action == 'download':
                        response = self.__Utilites.request_to_server(method='GET', url=URL, region=REGION)
                        headers = response.headers

                        if headers['message'] == 'redirect':
                            response2 = self.__Utilites.request_to_server(method='GET', url=headers['url'], send_request_time=headers['send_request_time'], region=REGION)
                            headers2 = response2.headers

                            with open(f'downloaded_files/{headers2["filename"]}', 'wb') as file:
                                file.write(response2.content)
                            print(self.__Utilites.response_message_correction(headers2))
                        else:
                            with open(f'downloaded_files/{headers["filename"]}', 'wb') as file:
                                file.write(response.content)

                            print(self.__Utilites.response_message_correction(headers))
                except Exception as e:
                    return f'Requests exception: {e}'