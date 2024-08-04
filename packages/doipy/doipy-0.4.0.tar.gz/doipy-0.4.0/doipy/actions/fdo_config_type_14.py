from doip_sdk import send_request

from doipy.actions.doip import create
from doipy.constants import DOType, TypeIdentifier, ResponseStatus, DOIPOperation
from doipy.dtr_utils import get_service_id, get_connection
from doipy.exceptions import InvalidRequestException
from doipy.models import FdoInput
from doipy.request_and_response import decode_json_response


def create_fdo_config_type_14(fdo_input: FdoInput):

    # get service ID, IP and port
    service_id = get_service_id(fdo_input.fdo_service_ref)
    service_id, ip, port = get_connection(service_id)

    # create first message
    message_1 = {
        'targetId': f'{service_id}',
        'operationId': DOIPOperation.CREATE.value,
    }

    # provide correct set of authentication credentials
    authentication_message = fdo_input.authentication.build_authentication_message()
    message_1 = message_1 | authentication_message

    # create second message
    message_2 = {
        # TODO: type should not be part of the DOIP message, but of the adaptor (?)
        'type': DOType.FDO.value,
        'attributes': {
            'content': {
                'id': '',
                'name': 'FAIR Digital Object',
                # FDO_Profile_Ref: mandatory
                TypeIdentifier.FDO_PROFILE_REF.value: fdo_input.fdo_profile_ref,
                # FDO_Type_Ref: mandatory
                TypeIdentifier.FDO_TYPE_REF.value: fdo_input.fdo_type_ref
            }
        }
    }
    # FDO_Rights_Ref: optional
    if fdo_input.fdo_rights_ref:
        message_2['attributes']['content'][TypeIdentifier.FDO_RIGHTS_REF.value] = fdo_input.fdo_rights_ref
    # FDO_Genre_Ref: optional
    if fdo_input.fdo_genre_ref:
        message_2['attributes']['content'][TypeIdentifier.FDO_GENRE_REF.value] = fdo_input.fdo_genre_ref

    # create the data and metadata DOs
    if fdo_input.data_and_metadata:
        data_refs = []
        metadata_refs = []
        for item in fdo_input.data_and_metadata:
            # create the data do
            if item.data_bitsq or item.data_values:
                response = create(service_id, ip, port, DOType.DO.value, 'Data-DO',
                                  item.data_bitsq, item.data_values, fdo_input.authentication.username,
                                  fdo_input.authentication.client_id, fdo_input.authentication.password,
                                  fdo_input.authentication.token)
                data_ref = response[0]['output']['id']
                data_refs.append(data_ref)
            # create the metadata do
            if item.metadata_bitsq or item.metadata_values:
                response = create(service_id, ip, port, DOType.DO.value, 'Metadata-DO',
                                  item.metadata_bitsq, item.metadata_values, fdo_input.authentication.username,
                                  fdo_input.authentication.client_id, fdo_input.authentication.password,
                                  fdo_input.authentication.token)
                metadata_ref = response[0]['output']['id']
                metadata_refs.append(metadata_ref)
        if data_refs:
            message_2['attributes']['content'][TypeIdentifier.FDO_DATA_REFS.value] = data_refs
        if metadata_refs:
            message_2['attributes']['content'][TypeIdentifier.FDO_MD_REFS.value] = metadata_refs

    # send request and read response
    data = [message_1, message_2]
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)

    if response_decoded[0]['status'] == ResponseStatus.SUCCESS.value:
        return response_decoded
    raise InvalidRequestException(response)
