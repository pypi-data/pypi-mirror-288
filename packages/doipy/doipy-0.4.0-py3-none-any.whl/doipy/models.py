import json
import requests
from jsonschema import validate
from pydantic import BaseModel
from pathlib import Path

from doipy.constants import DomainName, ValidationSchemas
from doipy.exceptions import AuthenticationException


class Authentication(BaseModel):
    # optional
    username: str = None
    client_id: str = None
    password: str = None
    token: str = None

    @classmethod
    def create_instance(cls, username: str = None, client_id: str = None, password: str = None,
                        token: str = None) -> 'Authentication':
        # TODO: can the validation process be formulated as part of the DTR? -> ask Hans
        if not username and not client_id and not token:
            raise AuthenticationException('Provide token, username or client_id')

        # build the Authentication object
        authentication = cls()
        if token:
            authentication.token = token
        elif client_id:
            if password:
                authentication.client_id = client_id
                authentication.password = password
            else:
                raise AuthenticationException('Provide password')
        else:
            if password:
                authentication.username = username
                authentication.password = password
            else:
                raise AuthenticationException('Provide password')
        return authentication

    def build_authentication_message(self) -> dict:
        # create the message
        authentication_message = {}
        if self.token:
            authentication_message['authentication'] = {
                'token': self.token
            }
        elif self.client_id:
            authentication_message['clientId'] = self.client_id
            authentication_message['authentication'] = {
                'password': self.password
            }
        else:
            authentication_message['authentication'] = {
                'username': self.username,
                'password': self.password
            }
        return authentication_message


class DataAndMetadata(BaseModel):
    # optional
    data_bitsq: Path = None
    data_values: dict = None
    metadata_bitsq: Path = None
    metadata_values: dict = None

    @classmethod
    def parse(cls, user_input: dict) -> 'DataAndMetadata':
        # validate the input against the JSON input schema
        url = f'{DomainName.TYPE_API_SCHEMAS.value}/{ValidationSchemas.DATA_AND_METADATA.value}'
        input_schema = requests.get(url).json()

        validate(instance=user_input, schema=input_schema)

        do_input = cls()

        if 'data_bitsq' in user_input:
            data_bitsq = Path(user_input['data_bitsq'])
            do_input.data_bitsq = data_bitsq

        if 'metadata_bitsq' in user_input:
            metadata_bitsq = Path(user_input['metadata_bitsq'])
            do_input.metadata_bitsq = metadata_bitsq

        if 'data_values' in user_input:
            with open(user_input['data_values']) as f:
                data_values = json.load(f)
                do_input.data_values = data_values

        if 'metadata_values' in user_input:
            with open(user_input['metadata_values']) as f:
                metadata_values = json.load(f)
                do_input.metadata_values = metadata_values

        return do_input


class FdoInput(BaseModel):
    # mandatory
    fdo_service_ref: str
    fdo_profile_ref: str
    authentication: Authentication
    fdo_type_ref: str
    # optional
    fdo_rights_ref: str = None
    fdo_genre_ref: str = None
    data_and_metadata: list[DataAndMetadata] = None

    @classmethod
    def parse(cls, user_input: dict, input_schema: dict) -> 'FdoInput':

        # validate the input against the JSON input schema
        validate(instance=user_input, schema=input_schema)

        # construct the authentication object
        auth = Authentication.create_instance(user_input['FDO_Authentication'].get('username'),
                                              user_input['FDO_Authentication'].get('client_id'),
                                              user_input['FDO_Authentication'].get('password'),
                                              user_input['FDO_Authentication'].get('token'))

        # construct the fdo_input object with the mandatory references
        fdo_input = cls(fdo_service_ref=user_input['FDO_Service_Ref'], fdo_profile_ref=user_input['FDO_Profile_Ref'],
                        fdo_type_ref=user_input['FDO_Type_Ref'], authentication=auth)

        # define the optional references
        if 'FDO_Rights_Ref' in user_input:
            fdo_input.fdo_rights_ref = user_input['FDO_Rights_Ref']
        if 'FDO_Genre_Ref' in user_input:
            fdo_input.fdo_genre_ref = user_input['FDO_Genre_Ref']

        # define the data and metadata arrays which will be used to create the DOs
        if user_input['FDO_Data_and_Metadata']:
            fdo_input.data_and_metadata = []
            for item in user_input['FDO_Data_and_Metadata']:
                if item:
                    # create the structure for the data DO and for the metadata DO
                    do = DataAndMetadata.parse(item)
                    fdo_input.data_and_metadata.append(do)

        return fdo_input
