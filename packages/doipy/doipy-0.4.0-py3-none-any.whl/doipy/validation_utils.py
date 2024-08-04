import requests
from jsonschema import validate

from doipy.constants import DomainName, ValidationSchemas
from doipy.exceptions import OperationNotSupportedException


def general_validation(user_input: dict):
    url = f'{DomainName.TYPE_API_SCHEMAS.value}/{ValidationSchemas.CREATE_FDO_DOIPY_INPUT.value}'
    validation_schema = requests.get(url).json()
    validate(instance=user_input, schema=validation_schema)


def get_specific_schema(user_input: dict):

    # get the service information from the dtr
    url = f'{DomainName.TYPE_API_OBJECTS.value}/{user_input["FDO_Service_Ref"]}'
    service = requests.get(url).json()

    # get all operations that can be performed on the given service
    operation_pids = service['implementsOperations']

    # find the correct create_FDO operation (which corresponds to the profile)
    found_operation = None
    for operation_pid in operation_pids:
        url = f'{DomainName.TYPE_REGISTRY_OBJECTS.value}/{operation_pid}'
        operation = requests.get(url).json()
        # condition that the correct FDO operation was found
        if (operation['operationCategory'] == 'Create_FDO' and operation['relatedFdoProfiles'][0]
                == user_input['FDO_Profile_Ref']):
            found_operation = operation
            break
    if not found_operation:
        raise OperationNotSupportedException('The service does not support Create_FDO for this profile.')

    # return input schema from the DTR for the chosen create_FDO operation
    input_pid = found_operation['inputs']
    url = f'{DomainName.TYPE_API_OBJECTS.value}/{input_pid}'
    validation_schema = requests.get(url).json()
    return validation_schema
