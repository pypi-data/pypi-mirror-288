from doip_sdk import send_request

from doipy.dtr_utils import get_connection
from doipy.constants import CordraOperation
from doipy.request_and_response import decode_json_response

# get service settings
target_id, ip, port = get_connection('21.T11966/service')


def get_design():
    message = {
        'targetId': f'{target_id}',
        'operationId': CordraOperation.GET_DESIGN.value
    }
    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def get_init_data():
    message = {
        'targetId': f'{target_id}',
        'operationId': CordraOperation.GET_INIT_DATA.value
    }
    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded
