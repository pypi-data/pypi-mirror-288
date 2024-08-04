import json
import uuid
from pathlib import Path
from doip_sdk import send_request

from doipy.exceptions import InvalidRequestException
from doipy.constants import DOIPOperation, ResponseStatus, DOType
from doipy.models import Authentication
from doipy.request_and_response import decode_json_response


def hello(target_id: str, ip: str, port: int):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    # create request message
    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.HELLO.value
    }
    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def list_operations(target_id: str, ip: str, port: int, username: str = None, client_id: str = None,
                    password: str = None, token: str = None):
    """
    Implements 0.DOIP/Op.ListOperations: An operation to request the list of operations that can be invoked on the
    target DO.
    """
    # create request message
    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.LIST_OPERATION.value
    }
    # validate authentication credentials and build message with authentication credentials, if authentication
    # credentials are provided
    if username or client_id or password or token:
        authentication = Authentication.create_instance(username, client_id, password, token)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message
    # send request and read response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def create(target_id: str, ip: str, port: int, do_type: str = DOType.DO.value, do_name: str = 'Digital Object',
           bitsq: Path = None, metadata: dict = None, username: str = None, client_id: str = None, password: str = None,
           token: str = None):
    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.CREATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # create second message: DO of type document in Cordra for the file which is added
    message_2 = {
        'type': do_type,
        'attributes': {
            'content': {
                'id': '',
                'name': do_name
            }
        }
    }

    # add metadata to DO
    if metadata:
        message_2['attributes']['content'] = message_2['attributes']['content'] | metadata

    if bitsq:
        # add information on files to DO
        filename = bitsq.name
        my_uuid = str(uuid.uuid4())
        message_2['elements'] = [
            {
                'id': my_uuid,
                'type': 'text/plain',
                'attributes': {
                    'filename': filename
                }
            }
        ]
        data.append(message_2)

        # third message
        message_3 = {
            'id': my_uuid
        }
        data.append(message_3)

        # send content of files
        data.append(bitsq)

    else:
        data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)

    if response_decoded[0]['status'] == ResponseStatus.SUCCESS.value:
        return response_decoded
    raise InvalidRequestException(response)


# todo: update
"""
def update(service: str, client_id: str, password: str, do_type: str):
    # TODO fix message

    # get service settings
    target_id, ip, port = get_connection(service)

    with create_socket(ip, port) as ssl_sock:
        message = {
            'clientId': client_id,
            'targetId': target_id,
            'operationId': DOIPOperation.UPDATE.value,
            'authentication': {
                'password': password
            }
        }
        send_message(message, ssl_sock)
        string1 = f'https://cordra.testbed.pid.gwdg.de/objects/{target_id}?payload=file'
        string2 = f'https://cordra.testbed.pid.gwdg.de/objects/{target_id}'
        message = {
            'type': do_type,
            'attributes': {
                'content': {
                    'id': '',
                    'Payload': string1,
                    'Metadata': string2
                }
            }
        }
        send_message(message, ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response
"""


def retrieve(target_id: str, ip: str, port: int, file: str = None, username: str = None, client_id: str = None,
             password: str = None, token: str = None):
    """
    Implements 0.DOIP/Op.Retrieve: An operation to allow a client to get information about an (F)DO at a service.
    """
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.RETRIEVE.value
    }
    if file:
        message['attributes'] = {
            'element': file
        }
    if username or client_id or password or token:
        # validate authentication credentials and build message with authentication credentials
        authentication = Authentication.create_instance(username, client_id, password, token)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])

    # decode first segment
    first_segment_json = json.loads(response.content[0])

    # if response is success and a file is returned
    if first_segment_json['status'] == ResponseStatus.SUCCESS.value and file:

        # if a filename is given, use this file name
        filename = first_segment_json.get('attributes').get('filename')
        splits = filename.split('/')
        filename = splits[len(splits)-1]
        if filename:
            f = filename
        else:
            f = 'data'
        with open(f, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(response.content[1])
        return [first_segment_json]

    # if response is not success or no file is returned
    else:
        response_decoded = decode_json_response(response)
        return response_decoded


# delete
def delete(target_id: str, ip: str, port: int, username: str = None, client_id: str = None, password: str = None,
           token: str = None):
    """
    Implements 0.DOIP/Op.Delete: An operation to allow a client to delete an (F)DO at a service. This operation just
    deletes the referenced (F)DO but not any other (F)DOs which are referenced by the given (F)DO.
        """
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.DELETE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token)
    authentication_message = authentication.build_authentication_message()
    # concatenate messages
    message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def search(target_id: str, ip: str, port: int, query: str, username: str = None, client_id: str = None,
           password: str = None, token: str = None):
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.SEARCH.value,
        'attributes': {
            'query': query
        }
    }
    if username or client_id or password or token:
        # validate authentication credentials and build message with authentication credentials
        authentication = Authentication.create_instance(username, client_id, password, token)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded
