import requests

from doipy.constants import DomainName
from doipy.exceptions import HandleValueNotFoundException

cached_data = {}


def get_connection(service: str) -> (str, str, int):
    """
    Get the serviceId, IP and port from the handle correponding to the service that should be connected to.
    """
    # get required handle values from the handle record
    url = f'https://hdl.handle.net/api/handles/{service}'
    # cache the service_id, ip and port of the requested service
    if service not in cached_data:
        r = requests.get(url)
        data = r.json()
        # find ip and port in the handle values
        ip = ''
        port = 0
        ip_found = False
        port_found = False
        for item in data['values']:
            if item['type'] == 'IP':
                ip = item['data']['value']
                ip_found = True
            if item['type'] == 'PORT':
                port = item['data']['value']
                port_found = True
            if ip_found and port_found:
                break
        if not ip_found:
            raise HandleValueNotFoundException('Could not find IP in the Service Handle')
        elif not port_found:
            raise HandleValueNotFoundException('Could not find Port in the Service Handle')
        else:
            cached_data[service] = {
                'service_id': service,
                'ip': ip,
                'port': port
            }
    return cached_data[service]['service_id'], cached_data[service]['ip'], int(cached_data[service]['port'])


def get_service_id(fdo_service_ref: str) -> str:
    # get the service information from the dtr
    url = f'{DomainName.TYPE_API_OBJECTS.value}/{fdo_service_ref}'
    service = requests.get(url).json()

    # get the service ID
    service_id = service['serviceId']
    return service_id
