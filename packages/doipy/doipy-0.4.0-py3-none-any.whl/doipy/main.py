import json
from pathlib import Path
from typing import Annotated
import typer
from jsonschema.exceptions import ValidationError

from doipy import get_connection, hello, list_operations, create, retrieve, delete, search, create_fdo, get_design, \
    get_init_data
from doipy.constants import ResponseStatus, DOType
from doipy.exceptions import AuthenticationException, InvalidRequestException, ProfileNotSupportedException, \
    HandleValueNotFoundException, OperationNotSupportedException
from doipy.request_and_response import print_json_response

app = typer.Typer()


@app.command(name='hello')
def hello_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                  ip: Annotated[str, typer.Argument(help='the IP address identifying the data service')],
                  port: Annotated[int, typer.Argument(help='the DOIP port of the data service')]):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    response = hello(target_id, ip, port)
    print_json_response(response)


@app.command(name='list_operations')
def list_operations_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                            ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                            port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                            username: Annotated[
                                str, typer.Option(help='the username of the user at the data service')] = None,
                            client_id: Annotated[
                                str, typer.Option(help='the clientId of the user at the data service')] = None,
                            password: Annotated[
                                str, typer.Option(help='the password of the user at the data service')] = None,
                            token: Annotated[str, typer.Option(help='a token at the data service')] = None):
    """
    Implements 0.DOIP/Op.ListOperations: An operation to request the list of operations that can be invoked on the
    target DO.
    """
    try:
        response = list_operations(target_id, ip, port, username, client_id, password, token)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()

    print_json_response(response)


@app.command(name='create')
def create_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                   ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                   port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                   do_type: Annotated[
                       str, typer.Option(help='name of the DO to be generated at the data service')] = DOType.DO.value,
                   do_name: Annotated[
                       str, typer.Option(help='name of the DO to be generated at data service')] = 'Digital Object',
                   bitsq: Annotated[
                       Path, typer.Option(
                           help='Path to a file which comprises the data bit-sequence of the DO to be generated')]
                   = None,
                   metadata: Annotated[
                       Path, typer.Option(
                           help='Path to a JSON file which comprises the data bit-sequence of the DO to be generated')]
                   = None,
                   username: Annotated[
                       str, typer.Option(help='the username of the user at the data service')] = None,
                   client_id: Annotated[
                       str, typer.Option(help='the clientId of the user at the data service')] = None,
                   password: Annotated[
                       str, typer.Option(help='the password of the user at the data service')] = None,
                   token: Annotated[str, typer.Option(help='a token at the data service')] = None):
    """
    Implements 0.DOIP/Op.Create: An operation to create a digital object (containing at most one data bit-sequence)
    within the DOIP service. The target of a creation operation is the DOIP service itself.
    """
    # get the metadata and write them into a dictionary
    metadata_dict = None
    if metadata:
        try:
            with open(metadata, 'r') as f:
                metadata_dict = json.load(f)
        except json.JSONDecodeError as error_message:
            print("Invalid JSON syntax:", error_message)
            raise typer.Exit()
        except Exception as error_message:
            print(error_message)
            raise typer.Exit()

    try:
        response = create(target_id, ip, port, do_type, do_name, bitsq, metadata_dict, username, client_id, password,
                          token)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()
    # in case that the DOIP response status is not success, raise an exception and terminate the program
    except InvalidRequestException as error:
        details = error.args[0][0]
        print(f'{details["status"]} {ResponseStatus(details["status"]).name}')
        print(details['output']['message'])
        raise typer.Exit()

    print_json_response(response)


@app.command(name='retrieve')
def retrieve_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying an (F)do')],
                     ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                     port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                     file: Annotated[str, typer.Option(help='If the bit-sequence should be returned, this is the id of '
                                                            'the file in the DOIP service')] = None,
                     username: Annotated[
                         str, typer.Option(help='the username of the user at the data service')] = None,
                     client_id: Annotated[
                         str, typer.Option(help='the clientId of the user at the data service')] = None,
                     password: Annotated[
                         str, typer.Option(help='the password of the user at the data service')] = None,
                     token: Annotated[str, typer.Option(help='a token at the data service')] = None):
    """
    Implements 0.DOIP/Op.Retrieve: An operation to allow a client to get information about an (F)DO at a service.
    """
    try:
        response = retrieve(target_id, ip, port, file, username, client_id, password, token)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()

    print_json_response(response)


@app.command(name='delete')
def delete_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying an (F)do')],
                   ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                   port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                   username: Annotated[
                       str, typer.Option(help='the username of the user at the data service')] = None,
                   client_id: Annotated[
                       str, typer.Option(help='the clientId of the user at the data service')] = None,
                   password: Annotated[
                       str, typer.Option(help='the password of the user at the data service')] = None,
                   token: Annotated[str, typer.Option(help='a token at the data service')] = None):
    """
    Implements 0.DOIP/Op.Delete: An operation to allow a client to delete an (F)DO at a service. This operation just
    deletes the referenced (F)DO but not any other (F)DOs which are referenced by the given (F)DO.
    """
    try:
        response = delete(target_id, ip, port, username, client_id, password, token)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()

    print_json_response(response)


@app.command(name='search')
def search_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying an (F)do')],
                   ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                   port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                   query: Annotated[
                       str, typer.Argument(help='The search query to be performed, in a textual representation')],
                   username: Annotated[
                       str, typer.Option(help='the username of the user at the data service')] = None,
                   client_id: Annotated[
                       str, typer.Option(help='the clientId of the user at the data service')] = None,
                   password: Annotated[
                       str, typer.Option(help='the password of the user at the data service')] = None,
                   token: Annotated[str, typer.Option(help='a token at the data service')] = None):
    """Implements 0.DOIP/Op.Search"""
    try:
        response = search(target_id, ip, port, query, username, client_id, password, token)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()

    print_json_response(response)


@app.command(name='create_fdo')
def create_fdo_command(
        input_file: Annotated[Path, typer.Argument(help='A file containing a JSON which follows a specific '
                                                        'JSON schema. The file contains data bit-sequences, '
                                                        'metadata bit-sequences and the metadata that should '
                                                        'be written into the corresponding PID records.')]):
    """
    Create a FAIR Digital Object (FDO).
    """
    # read the user input
    try:
        with open(input_file, 'r') as f:
            user_input = json.load(f)
    except json.JSONDecodeError as error_message:
        print("Invalid JSON syntax:", error_message)
        raise typer.Exit()
    except Exception as error_message:
        print(error_message)
        raise typer.Exit()

    # Create the FDO
    try:
        response = create_fdo(user_input)
    except ValidationError as error:
        print(str(error))
        raise typer.Exit()
    except OperationNotSupportedException as error:
        print(str(error))
        raise typer.Exit()
    # in case that authentication fails, raise an exception
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()
    # in case the chosen profile is not supported, raise an exception
    except ProfileNotSupportedException as error:
        print(str(error))
        raise typer.Exit()
    # in case that the DOIP response is not success, raise an exception and terminate the program
    except InvalidRequestException as error:
        details = error.args[0][0]
        print(f'{details["status"]} {ResponseStatus(details["status"]).name}')
        print(details['output']['message'])
        raise typer.Exit()

    print_json_response(response)


@app.command(name='get_connection')
def get_connection_command(service: Annotated[str, typer.Argument(help='the PID identifying a data service')]):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    try:
        service_id, ip, port = get_connection(service)
        print(f'Service ID: {service_id}')
        print(f'IP: {ip}')
        print(f'Port: {port}')
    except HandleValueNotFoundException as error:
        print(error)


@app.command(name='get_design')
def get_design_command():
    """Implements 20.DOIP/Op.GetDesign (see https://www.cordra.org)"""
    response = get_design()
    print_json_response(response)


@app.command(name='get_init_data')
def get_init_data_command():
    """Implements 20.DOIP/Op.GetInitData (see https://www.cordra.org)"""
    response = get_init_data()
    print_json_response(response)
