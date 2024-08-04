from doipy.actions.fdo_config_type_14 import create_fdo_config_type_14
from doipy.constants import Profile
from doipy.exceptions import ProfileNotSupportedException
from doipy.models import FdoInput
from doipy.validation_utils import general_validation, get_specific_schema


def create_fdo(user_input: dict):

    # validate the user input against the general input schema
    general_validation(user_input)

    # get the schema which belongs to the inputs of the create operation for the chosen profile
    specific_schema = get_specific_schema(user_input)

    # validate the user input against the input schema for the specific profile and create an instance of FdoInput class
    fdo_input = FdoInput.parse(user_input, specific_schema)

    # get the profile from the FdoInput
    profile = fdo_input.fdo_profile_ref

    # choose the correct create_fdo operation
    if profile == Profile.CONFIG_TYPE_14.value:
        response = create_fdo_config_type_14(fdo_input)
    # check here for other profiles/configuration types
    else:
        raise ProfileNotSupportedException('Create_FDO is not supported by DOIPY for the chosen Profile.')

    # add more create_fdo operations for other configuration types
    return response
