# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import json
from enum import IntEnum


# Field names and version constants used to communicate with the services.
PROTOCOL_VERSION = 5
BUILDINGS_FIELD = "buildings"
NAME_FIELD = "name"
ID_FIELD = "id"
FLOOR_PLANS_FIELD = "floor_plans"
IMAGE_ID_FIELD = "image_id"
AREAS_FIELD = "areas"
NETWORKS_FIELD = "networks"
NODES_FIELD = "nodes"
DATA_FIELD = "data"
SESSION_ID_FIELD = "session_id"
INFLUX_TOKEN_FIELD = "influx_token"
TYPE_FIELD = "type"
VERSION_FIELD = "version"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
IMAGE_BASE64_FIELD = "image_base64"


class MessageTypeEnum(IntEnum):
    """ Message type to send request to the metadata service. """

    LOGIN = 1
    GET_BUILDINGS = 1001
    GET_BUILDINGS_FLOOR_PLANS = 1011
    GET_FLOOR_PLAN_IMAGE_DATA = 1021
    GET_MAP_AREAS = 1031
    GET_NETWORKS = 1041


def get_login_message(username, password):
    """ Return a get login message to be sent to the metadata service. """
    data = {
        DATA_FIELD: {USERNAME_FIELD: username, PASSWORD_FIELD: password},
        TYPE_FIELD: MessageTypeEnum.LOGIN,
        VERSION_FIELD: PROTOCOL_VERSION,
    }

    return json.dumps(data)


def get_buildings_message(login_session_id):
    """ Return a get buildings message to be sent to the metadata service. """
    data = {
        DATA_FIELD: {},
        SESSION_ID_FIELD: login_session_id,
        TYPE_FIELD: MessageTypeEnum.GET_BUILDINGS,
        VERSION_FIELD: PROTOCOL_VERSION,
    }

    return json.dumps(data)


def get_buildings_floor_plans_message(login_session_id, building_id):
    """ Return a get building floor plans message to be sent to the metadata service. """
    data = {
        DATA_FIELD: {BUILDINGS_FIELD: [{ID_FIELD: building_id}]},
        SESSION_ID_FIELD: login_session_id,
        TYPE_FIELD: MessageTypeEnum.GET_BUILDINGS_FLOOR_PLANS,
        VERSION_FIELD: PROTOCOL_VERSION,
    }

    return json.dumps(data)


def get_floor_plan_image_data_message(login_session_id, image_id):
    """ Return a get floor plans image message to be sent to the metadata service. """
    data = {
        DATA_FIELD: {IMAGE_ID_FIELD: image_id},
        SESSION_ID_FIELD: login_session_id,
        TYPE_FIELD: MessageTypeEnum.GET_FLOOR_PLAN_IMAGE_DATA,
        VERSION_FIELD: PROTOCOL_VERSION,
    }

    return json.dumps(data)


def get_map_areas_message(login_session_id, floor_plan_id):
    """ Return a get map areas message to be sent to the metadata service. """
    data = {
        DATA_FIELD: {
            BUILDINGS_FIELD: [{FLOOR_PLANS_FIELD: [{ID_FIELD: floor_plan_id}]}]
        },
        SESSION_ID_FIELD: login_session_id,
        TYPE_FIELD: MessageTypeEnum.GET_MAP_AREAS,
        VERSION_FIELD: PROTOCOL_VERSION,
    }

    return json.dumps(data)


def get_rts_login_message(login_session_id: str):
    """ Return a get rts login message to be sent to the rts service. """
    data = {SESSION_ID_FIELD: login_session_id, VERSION_FIELD: PROTOCOL_VERSION}

    return json.dumps(data)
