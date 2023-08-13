import requests
from geopy.distance import geodesic
from ReadJSON import ReadJSON

class ServiceIP:
    def __init__(self):
        self.SERVERS_LIST = ReadJSON().read(filename='servers_list')
        self.SERVER_NAME = ReadJSON().read(filename='configs')[0]['server_name']
        self.SERVER_INFO = self.get_city_name_by_ip()

    def get_info_by_ip(self, ip: str) -> dict | str:
        try:
            return requests.get(url=f'http://ip-api.com/json/{ip}').json()
        except requests.exceptions.ConnectionError:
            return f'[!] Check your connection'

    def get_city_name_by_ip(self) -> dict[str, str, str, str]:
        for server in self.SERVERS_LIST:
            if server['server_name'] == self.SERVER_NAME:
                info_by_ip = self.get_info_by_ip(server['location_ip'])

                return {'server_name': self.SERVER_NAME, 'server_city': info_by_ip['city'], 'server_ip': server['location_ip'], 'server_url': server['server_url']}


    def get_coordinates_by_ip(self, ip: str) -> tuple:
        info_by_ip = self.get_info_by_ip(ip)

        return (info_by_ip['lat'], info_by_ip['lon'])

    def get_servers_coordinates(self) -> list[dict[str, tuple]]:
        ServersInfo = []

        for server in self.SERVERS_LIST:
            server_coordinates = self.get_coordinates_by_ip(server['location_ip']) #self.get_coordinates_by_ip(server['server_ip'])
            ServersInfo.append({'server_name': server['server_name'], 'server_coordinates': server_coordinates})

        return ServersInfo

    def get_nearest_server(self, client_ip: str) -> str:
        NearestServer = {'server_name': '', 'server_distance': 0.0}

        def write_server_data(ServerInfo: dict, server_distance: float):
            NearestServer['server_name'] = ServerInfo['server_name']
            NearestServer['server_distance'] = server_distance

        client_ip_coordinates = self.get_coordinates_by_ip(client_ip)

        for ServerInfo in self.get_servers_coordinates():
            server_distance = geodesic(ServerInfo['server_coordinates'], client_ip_coordinates).kilometers

            if NearestServer['server_distance'] == 0:
                write_server_data(ServerInfo, server_distance)

            if NearestServer['server_distance'] > server_distance:
                write_server_data(ServerInfo, server_distance)

        return NearestServer['server_name']