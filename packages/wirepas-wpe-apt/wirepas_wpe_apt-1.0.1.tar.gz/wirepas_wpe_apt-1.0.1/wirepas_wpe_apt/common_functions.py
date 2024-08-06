"""
Functions that are used to manipulate data files,
conversion of json Influxdb format to protobuf messages,
searching in the data file the good network and nodes,
but also manipulates metadata and converting a network in a dictionary format
to a ConfigurationData protobuf.
"""

# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import json
import math
from google.protobuf import json_format
import logging
from time import time

from wirepas_wpe_apt import wnt_proto
from wirepas_wpe_apt import wpe_proto
from wirepas_wpe_apt.constants import *
from wirepas_wpe_apt.element import Area, FloorPlan, Measurement, Node


def get_data_json(file_name):
    """ Extracts the data from a json file and returns the json associated.

    Args:
        file_name: The name of the json file with stored data.

    Return (str): The data into a dictionary shape.
    """
    logging.info("Get data from %s", file_name)
    try:
        with open(file_name) as file:
            data = json.loads(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            f"{file_name} file has not been found, please check the logs for unexpected errors "
            "or README.md or documentation if you have doubt on the execution of the script") from None
    except json.decoder.JSONDecodeError:
        raise ValueError(
            f"{file_name} file has been found, but it can't be parsed by json. "
            "Please refer to the README.md or documentation for the format of its content.") from None

    return data


def parse_elements_file(file_name):
    """ Extracts the data from a json file and parse the content as Element objects.

    Args:
        file_name: The name of the json file with stored data.

    Return (str): The data into a dictionary shape.
    """
    json_content = get_data_json(file_name)
    if NODES_FIELD in json_content:
        json_content[NODES_FIELD] = [Node.from_dict(node) for node in json_content[NODES_FIELD]]

    if MEASUREMENTS_FIELD in json_content:
        json_content[MEASUREMENTS_FIELD] = [Measurement.from_dict(mes) for mes in json_content[MEASUREMENTS_FIELD]]

    if AREAS_FIELD in json_content:
        json_content[AREAS_FIELD] = {uid: Area.from_dict(area) for uid, area in json_content[AREAS_FIELD].items()}

    if FLOOR_PLANS_FIELD in json_content:
        json_content[FLOOR_PLANS_FIELD] = {uid: FloorPlan.from_dict(floor) for uid, floor in json_content[FLOOR_PLANS_FIELD].items()}

    return json_content


def parse_influxdata(json_data, proto_type=wnt_proto.Message,
                     pseudo_name="Message_{}"):
    """ Parse a flat influx json as a protobuf object.

    Notes: The output is constructed so that it has the same name of fields
    as the wnt proto objects it corresponds to.
    Thus it can be parse to the proto with the following command:

    json_format.ParseDict(output_data)

    Example of input: {
            'Message_2': 10,
            'Message_7': 1,
            'Message_73_1': 45,
            'Message_73_10': '[aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee]',
            'Message_73_2': 5,
            'Message_73_23': False,
            'Message_73_3': 0,
            'Message_73_31': 0,
            'Message_73_50': 'Tag name',
            'Message_73_51': 'Some description'
        }

    Example of output: {
        'network_id': 10,
        'source_address': 1,
        'node_metadata': {
            'latitude': 45,
            'longitude': 5,
            'altitude': 0,
            'map_uuid': '[aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee]',
            'is_virtual': False,
            'rssi_offset': 0,
            'name': 'Tag name',
            'description': 'Some description'
        }
    }

    Args:
        json_data (dict): Influx data as a flat dictionary.
        proto_type: Default to wnt_proto.Message.
            Protobuf object type to convert the influx data to.
        pseudo_name (str): Default to "Message_{}", pseudo name to map influx fields
            with real proto fields names. If set to None, no mapping is done and
            proto fields must correspond to the name of the fields in the data.
    """
    def map_influx_fields_to_proto(json_data, proto_descriptor, pseudo_name):
        proto_data = {}

        for field in proto_descriptor.fields:
            if pseudo_name:
                data_field_name = pseudo_name.format(field.number)
                child_pseudo_name = pseudo_name.format(field.number) + "_{}"
            else:
                data_field_name = field.name.lower()
                child_pseudo_name = pseudo_name

            if data_field_name in json_data and json_data[data_field_name] not in [None, ""]:
                value = json_data[data_field_name]
                if isinstance(value, str) and value[0] == "[" and value[-1] == "]":
                    if "=" in value:
                        value = stringlist_to_json_objects(value, field.message_type, child_pseudo_name)
                    else:
                        value = stringlist_to_list(value)

                proto_data[field.name] = value
            elif field.message_type:
                # Parse the children fields description.
                data_children = map_influx_fields_to_proto(json_data, field.message_type, pseudo_name=child_pseudo_name)
                if data_children:
                    proto_data[field.name] = data_children

        return proto_data

    # Clean the data, as many NaN can be added to influx data
    cleaned_data = {key: value for (key, value) in json_data.items()
                    if not (isinstance(value, float) and math.isnan(value))}

    proto_data = map_influx_fields_to_proto(cleaned_data, proto_type.DESCRIPTOR, pseudo_name)
    return json_format.ParseDict(proto_data, proto_type())


def stringlist_to_json_objects(string, object_descriptor, pseudo_name):
    """ Transform a string of list of protobuf objects to a list of objects json.

    Args:
        string (str): String representation of a list of protobuf objects.
        object_descriptor: Protobuf object descriptor.
        pseudo_name (str): Pseudo name to map influx fields with real proto fields names.
            If set to None, no mapping is done and
            proto fields must correspond to the name of the fields in the data.
    """
    string = string.strip("[]")
    objects = []
    current_values = {}
    current_index = -1

    for attribute in string.split(","):
        key, value = attribute.split("=")[0:2]
        index = int(key.split("_")[-1])
        if index <= current_index:
            proto_object = parse_influxdata(current_values, object_descriptor._concrete_class, pseudo_name)
            objects.append(json_format.MessageToDict(proto_object))
            current_values = {}

        current_values[key] = value
        current_index = index

    proto_object = parse_influxdata(current_values, object_descriptor._concrete_class, pseudo_name)
    objects.append(json_format.MessageToDict(proto_object))
    return objects


def stringlist_to_list(string: str) -> list:
    """ Transform a string representation of a list to a list of string:

    Example:
        Input: '[1df9211c-aee1-3bb8-1cd0-0c0da6f973f2]'
        Output: ['1df9211c-aee1-3bb8-1cd0-0c0da6f973f2']
    """
    if isinstance(string, list):
        return string

    string = string.strip(" '[]")
    list_value = string.split(',')
    return list_value


def search_node(network, node_address):
    """ Finds the nodes json with the good node address in a network.

    Args:
        network (dict): Network containing the node we are searching for.
        node_address (Any): Address of the node to search in the network.

    Return (list(Any)): A list of nodes in wpe_proto.Node or standard json
                        format with the good node address.
    """
    list_nodes = []
    for node in network[NODES_FIELD]:
        if isinstance(node, Node) and node.address == int(node_address):
            list_nodes.append(node)
        elif isinstance(node, dict) and int(node["address"]) == int(node_address):
            list_nodes.append(node)

    return list_nodes


def network_to_configurationdata(network):
    """
    Takes a network containing Element objects of Nodes (anchors) and Areas
    and returns the associated protobuf wpe_proto.ConfigurationData.
    """
    configuration = wpe_proto.ConfigurationData()
    configuration.network = int(network[NETWORK_FIELD])
    if NODES_FIELD in network:
        configuration.nodes.extend([node.to_wpe_proto() for node in network[NODES_FIELD]])

    if AREAS_FIELD in network:
        configuration.areas.extend([area.to_wpe_proto() for area in network[AREAS_FIELD].values()])

    return configuration


def wait_for_events(events: list, timeout_s=None) -> bool:
    """ Wait for all events of a list to be set. """
    start = time()
    for event in events:
        time_spent = time() - start
        if timeout_s:
            event.wait(timeout_s - time_spent)
        else:
            event.wait()

    return False not in [event.is_set() for event in events]
