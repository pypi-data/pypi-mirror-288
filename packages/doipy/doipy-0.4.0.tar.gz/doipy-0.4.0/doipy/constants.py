from enum import Enum


class CordraOperation(Enum):
    GET_DESIGN = '20.DOIP/Op.GetDesign'
    GET_INIT_DATA = '20.DOIP/Op.GetInitData'


class DOIPOperation(Enum):
    HELLO = '0.DOIP/Op.Hello'
    CREATE = '0.DOIP/Op.Create'
    RETRIEVE = '0.DOIP/Op.Retrieve'
    UPDATE = '0.DOIP/Op.Update'
    DELETE = '0.DOIP/Op.Delete'
    SEARCH = '0.DOIP/Op.Search'
    LIST_OPERATION = '0.DOIP/Op.ListOperations'


class ResponseStatus(Enum):
    SUCCESS = '0.DOIP/Status.001'
    INVALID = '0.DOIP/Status.101'
    UNAUTHENTICATED = '0.DOIP/Status.102'
    UNAUTHORIZED = '0.DOIP/Status.103'
    UNKNOWN_DO = '0.DOIP/Status.104'
    DUPLICATED_PID = '0.DOIP/Status.105'
    UNKNOWN_OPERATION = '0.DOIP/Status.200'
    UNKNOWN_ERROR = '0.DOIP/Status.500'


class TypeIdentifier(Enum):
    FDO_PROFILE_REF = '21.T11969/bcc54a2a9ab5bf2a8f2c'
    FDO_TYPE_REF = '21.T11969/2bb5fec05c00bb89793e'
    FDO_RIGHTS_REF = '21.T11969/90fa2a1e224ae3e54139'
    FDO_GENRE_REF = '21.T11969/66d0e45fb2d2430ab967'
    FDO_DATA_REFS = '21.T11969/867134e94b3ec5afc6fe'
    FDO_MD_REFS = '21.T11969/a02253b264a9f2f1cf9a'


class ValidationSchemas(Enum):
    CREATE_FDO_DOIPY_INPUT = '21.T11969/6fe44ad5cba7c7c28c56'
    DATA_AND_METADATA = '21.T11969/27d8ca0c2585c0dafa39'


class DOType(Enum):
    DO = 'Document'
    FDO = 'FDO'


class DomainName(Enum):
    TYPE_API_SCHEMAS = 'https://typeapi.lab.pidconsortium.net/v1/types/schema'
    TYPE_API_OBJECTS = 'https://typeregistry.lab.pidconsortium.net/objects'
    TYPE_REGISTRY_OBJECTS = 'https://typeregistry.lab.pidconsortium.net/objects'


class Profile(Enum):
    CONFIG_TYPE_14 = '21.T11969/141bf451b18a79d0fe66'
