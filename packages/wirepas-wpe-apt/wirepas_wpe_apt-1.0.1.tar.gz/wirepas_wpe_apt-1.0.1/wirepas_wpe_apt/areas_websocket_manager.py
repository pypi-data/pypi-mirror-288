# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import json
import logging
import os
import ssl
import threading
import time
import websocket
from enum import IntEnum

from wirepas_wpe_apt import common_functions as cf
from wirepas_wpe_apt import wpe_proto
from wirepas_wpe_apt import wnt_proto
from wirepas_wpe_apt.areas_manager_utils import *
from wirepas_wpe_apt.constants import *
from wirepas_wpe_apt.element import Area, FloorPlan, Node


SLEEP_WAITING_IN_S = 0.1


class ErrorCodeResult(IntEnum):
    """ Websocket services result codes enumerate. """
    OK = 1
    GENERIC_ERROR = 2
    INVALID_CREDENTIALS = 3
    WRONG_PROTOCOL_VERSION = 4
    RIGHTS_ISSUE = 5
    INVALID_USER_ID = 6
    USER_ALREADY_CREATED = 7
    INVALID_RECEIVED_MESSAGE = 8
    INVALID_SESSION_ID = 9


class AreaWebsocketManager:

    def __init__(
        self,
        configuration_file,
        metadata_file,
        map_identifiers=None,
        query_anchors: bool = False,
        network_id=None,
        timeout_s=None,
        tls_secured=True,
    ):
        """ Initiate a AreaWebsocketManager that get data from the different backend services via websockets.

        Args:
            configuration_file (str): Configuration file containing the needed credentials.
            metadata_file (str): File where to store collected data.
            map_identifiers (list): Default to None.
                Filter of map identifier containing the nodes to be queried.
                If set to None, the map queried to include all anchors data.
            query_anchors (bool): Default to False.
                Boolean asserting that the anchors data need to be queried to the rts.
            network_id (int): Network id to filter the anchors if those are queried.
                Default to None not to filter on network id.
            timeout_s (int): Max timeout in seconds to run the AreaWebsocketManager and retrieve the data.
                Default to None to run for infinite time.
            tls_secured (bool): Default to True. Websockets connect to wss:// urls if enable else to ws://.
        """
        self.configuration_file = configuration_file
        configuration_data = cf.get_data_json(configuration_file)
        self.metadata_file = metadata_file
        self.map_identifiers = map_identifiers
        self.query_anchors = query_anchors
        self.network_id = network_id
        self.timeout_s = timeout_s
        self.tls_secured = tls_secured

        try:
            self.wnt_hostname = configuration_data["wnt_hostname"]
            self.wnt_username = configuration_data["wnt_username"]
            self.wnt_password = configuration_data["wnt_password"]
            self.ws_auth_port = configuration_data.get("ws_auth_port", 8813)
            self.ws_metadata_port = configuration_data.get("ws_metadata_port", 8812)
            self.ws_rts_port = configuration_data.get("ws_rts_port", 8811)
        except KeyError as error:
            raise KeyError("The configuration file should contain all the values "
                           "needed for the data collector to work properly. "
                           "Check the README.md for more information!") from error

        self.influx_token = None  # Influx v2 token to connect to the WNT4.4+
        self.is_ws_auth_end_event = threading.Event()
        self.is_ws_metadata_end_event = threading.Event()
        self.count_building = float("inf")
        self.floor_plans_dict = {}  # map between buildings and their floors
        self.areas_dict = {}  # map between floors and their areas
        self.floor_images_dict = {}  # map image identifiers with their data
        self.floor_plans_responses = 0
        self.areas_responses = 0
        self.image_reception_waiting = False
        self.current_image_id = 0
        self.login_session_id = None

        if self.tls_secured:
            ws_url_scheme = "wss"
        else:
            ws_url_scheme = "ws"

        self.ws_authentication = websocket.WebSocketApp(
            ws_url_scheme + "://" + self.wnt_hostname + ":" + str(self.ws_auth_port),
            on_open=self.ws_auth_on_open,
            on_message=self.ws_auth_on_message,
            on_error=self.ws_auth_on_error)

        self.ws_metadata = websocket.WebSocketApp(
            ws_url_scheme + "://" + self.wnt_hostname + ":" + str(self.ws_metadata_port),
            on_open=self.ws_metadata_on_open,
            on_message=self.ws_metadata_on_message,
            on_error=self.ws_metadata_on_error)

        self.is_ws_rts_end_event = threading.Event()
        self.is_ws_rts_end_event.set()

        if self.query_anchors:
            # RTS related attributes
            self.rts_anchor_protos = []
            self.rts_lock = threading.Lock()
            self._anchor_data = []

            self.nb_rts_services = 1  # Total number of RTS services
            self.nb_rts_services_started = 0  # Number of RTS services that are started
            self.ws_rts = websocket.WebSocketApp(
                ws_url_scheme + "://" + self.wnt_hostname + ":" + str(self.ws_rts_port),
                on_open=self.ws_rts_on_open,
                on_message=self.ws_rts_on_message,
                on_error=self.ws_rts_on_error)

    def get_influx_token(self):
        """
        Return the token that is used to connect to the Influx v2 database on WNT4.4+.
        Connection must be establish with the authentication service with `connect` method before.
        """
        return self.influx_token

    def connect(self):
        """ Connect to the authentication service. """
        thread = threading.Thread(target=self.run, args=(self.ws_authentication,), daemon=True)
        thread.start()
        self.is_ws_auth_end_event.wait(timeout=self.timeout_s)
        if not self.is_connected():
            raise ConnectionError("An error occured when trying to connect to the authentication service.")

    def is_connected(self):
        """ Return whether the object is connected to the services. """
        return self.ws_authentication.sock is not None and self.ws_authentication.sock.connected

    def close_websockets(self):
        """ Close websockets that aren't closed yet."""
        self.close_ws_auth()
        self.close_ws_metadata()
        self.close_ws_rts()

    def ws_auth_on_open(self, ws_object):
        """ Callback to be used when the authentication websocket has been opened. """
        login_message = get_login_message(self.wnt_username, self.wnt_password)
        logging.info("Sending login request to the authentication service")
        logging.debug(login_message)
        self.ws_authentication.send(login_message)

    def ws_auth_on_error(self, ws_object, error):
        """ Callback to be used when an authentication socket error occurs. """
        logging.error("An error occured when connecting to authentication service: %s",
                      error)
        self.close_websockets()

    def ws_auth_on_message(self, ws_object, message):
        """ Callback to be used when a new authentication message arrives. """
        logging.info("An authentication service message has been received: %s", message)
        session_obj = json.loads(message)
        logging.debug(session_obj)
        message_type = session_obj[TYPE_FIELD]

        if message_type == MessageTypeEnum.LOGIN:
            if session_obj["result"] != ErrorCodeResult.OK:
                logging.error("An error has been received by the authentication service: %s",
                              ErrorCodeResult(session_obj["result"]))
                self.close_websockets()
                return

            self.login_session_id = session_obj[DATA_FIELD][SESSION_ID_FIELD]
            self.influx_token = session_obj[DATA_FIELD].get(INFLUX_TOKEN_FIELD, None)
            self.is_ws_auth_end_event.set()

    def ws_metadata_on_message(self, ws_object, message):
        """ Callback to be used when a new metadata message arrives.
        It also updates the class object depending on the type of the
        received message.
        """
        logging.info("A metadata message has been received.")
        logging.debug(message)

        session_obj = json.loads(message)
        message_type = session_obj[TYPE_FIELD]

        if session_obj["result"] != ErrorCodeResult.OK:
            logging.error("An error has been received by the metadata service: %s",
                          ErrorCodeResult(session_obj["result"]))
            return

        if message_type == MessageTypeEnum.GET_BUILDINGS:
            self.count_building = len(session_obj[DATA_FIELD][BUILDINGS_FIELD])
            for building in session_obj[DATA_FIELD][BUILDINGS_FIELD]:
                self.floor_plans_dict[building[ID_FIELD]] = None

        elif message_type == MessageTypeEnum.GET_BUILDINGS_FLOOR_PLANS:
            building_id = session_obj[DATA_FIELD][BUILDINGS_FIELD][0][ID_FIELD]
            floor_plans = session_obj[DATA_FIELD][BUILDINGS_FIELD][0][FLOOR_PLANS_FIELD]
            interested_floors = [floor_plan for floor_plan in floor_plans
                                 if not self.map_identifiers
                                     or floor_plan[ID_FIELD] in self.map_identifiers]

            self.floor_plans_dict[building_id] = interested_floors
            self.floor_plans_responses += 1

        elif message_type == MessageTypeEnum.GET_MAP_AREAS:
            for floor_plan in session_obj[DATA_FIELD][BUILDINGS_FIELD][0][FLOOR_PLANS_FIELD]:
                self.areas_dict[floor_plan[ID_FIELD]] = floor_plan[AREAS_FIELD]
            self.areas_responses += 1

        elif message_type == MessageTypeEnum.GET_FLOOR_PLAN_IMAGE_DATA:
            self.floor_images_dict[self.current_image_id] = session_obj[DATA_FIELD][IMAGE_BASE64_FIELD]
            self.image_reception_waiting = False

    def ws_metadata_on_error(self, ws_object, error):
        """ Callback to be used when a metadata socket error occurs. """
        logging.error("An error occured during the query of data from WNT metadata: %s",
                      error)

    def ws_metadata_on_open(self, ws_object):
        """ Callback to be used when the metadata websocket has been opened. """
        thread = threading.Thread(target=self.query_data, daemon=True)
        thread.start()

    def query_data(self):
        """ Query metadata server to get buildings then floor plans then
        associated areas and the images of the floor plans if they exist.
        For each block of query, the function waits that the class object
        get updated before continuing.
        """
        get_buildings_msg = get_buildings_message(self.login_session_id)
        logging.info("Send a get buildings request to the metadata service.")
        logging.debug(json.dumps(get_buildings_msg, indent=4))
        self.ws_metadata.send(get_buildings_msg)
        while len(self.floor_plans_dict) != self.count_building:
            time.sleep(SLEEP_WAITING_IN_S)

        for building_id in self.floor_plans_dict:
            get_floor_plan_msg = get_buildings_floor_plans_message(self.login_session_id, building_id)
            logging.info("Send a get buildings floor plan request to the metadata service.")
            logging.debug(json.dumps(get_floor_plan_msg, indent=4))
            self.ws_metadata.send(get_floor_plan_msg)

        while len(self.floor_plans_dict) != self.floor_plans_responses:
            time.sleep(SLEEP_WAITING_IN_S)

        for floor_plans in self.floor_plans_dict.values():
            for floor_plan in floor_plans:
                get_map_areas_msg = get_map_areas_message(self.login_session_id, floor_plan[ID_FIELD])
                logging.info("Send a get map areas request to the metadata service.")
                logging.debug(json.dumps(get_map_areas_msg, indent=4))
                self.ws_metadata.send(get_map_areas_msg)

        while len(self.areas_dict) != self.areas_responses:
            time.sleep(SLEEP_WAITING_IN_S)

        for floor_plans in self.floor_plans_dict.values():
            for floor_plan in floor_plans:
                if IMAGE_ID_FIELD and floor_plan[IMAGE_ID_FIELD] is not None:
                    self.current_image_id = floor_plan[IMAGE_ID_FIELD]
                    self.image_reception_waiting = True

                    get_floor_plan_image_data_msg = get_floor_plan_image_data_message(self.login_session_id, self.current_image_id)
                    logging.info("Send a get floor plan image request to the metadata service.")
                    logging.debug(json.dumps(get_floor_plan_image_data_msg, indent=4))
                    self.ws_metadata.send(get_floor_plan_image_data_msg)

                    while self.image_reception_waiting:
                        time.sleep(SLEEP_WAITING_IN_S)

        self.close_ws_metadata()

    def close_ws_auth(self):
        """ Close the websocket connected to the authentication service. """
        if self.is_connected():
            logging.info("Close authentication service websocket!")
            self.ws_authentication.close()

        self.is_ws_auth_end_event.set()

    def close_ws_metadata(self):
        """ Close the websocket connected to the metadata service. """
        if self.ws_metadata.sock and self.ws_metadata.sock.connected:
            logging.info("Close metadata service websocket!")
            self.ws_metadata.close()

        self.is_ws_metadata_end_event.set()

    def close_ws_rts(self):
        """ Close the websocket connected to the rts service. """
        if self.query_anchors and self.ws_rts.sock and self.ws_rts.sock.connected:
            logging.info("Close rts service websocket!")
            self.ws_rts.close()

        self.is_ws_rts_end_event.set()

    def get_areas_json(self):
        """ Transform self.areas_dict into a more standard format:
        {'area_id': area} with area a dictionary of an area.

        Returns (dict): A standardized dictionary representing areas.
        """
        dictionary = {}
        for floor_plan_id, areas in self.areas_dict.items():
            for area in areas:
                # Set the WNT proto field names
                area['polygon_points'] = area.get("llas", None)
                area['floor_plan_id'] = floor_plan_id

                # Conversion of the dictionary to a internal standard format
                wnt_proto_obj = cf.parse_influxdata(area, wnt_proto.internal_pb2.Area, pseudo_name=None)
                dictionary[area[ID_FIELD]] = Area.from_wnt_proto(wnt_proto_obj).to_dict()

        return dictionary

    def get_floor_plans_json(self):
        """ Transform self.floor_plans_dict into a more standard format:
        {'floor_plan_id': floor_plan} with floor_plan a dictionary of a floor.

        Returns (dict): A standardized dictionary representing floors.
        """
        floors_dict = {}
        for floor_plans in self.floor_plans_dict.values():
            for floor_plan in floor_plans:
                floor_plan["image"] = self.floor_images_dict[floor_plan["image_id"]]
                floors_dict[floor_plan[ID_FIELD]] = FloorPlan.from_dict(floor_plan).to_dict()

        return floors_dict

    def generate_file(self):
        """ Generate a json file with all areas, their colors,
        floor plans and their images in it under this shape:
        {
            "areas": (list(dict))  # {'id_area': area} area in a dict format.
            "floor_plans": (dict)  # {'id_floor': floor_plan} floor_plan in a dict format.
        }
        """
        if not self.floor_images_dict or not self.get_floor_plans_json():
            raise ValueError("No floor plan has been received from the metadata service")

        data_dict = {
            AREAS_FIELD: self.get_areas_json(),
            FLOOR_PLANS_FIELD: self.get_floor_plans_json()
        }

        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, "w") as data_file:
            json.dump(data_dict, data_file, indent=4)

    # RTS methods
    def ws_rts_on_error(self, ws_object, error):
        """ Callback to be used when an anchor metadata socket error occurs.

        Args:
            error (str): error message.
        """
        logging.error("An error occured during the query of data from RTS: %s", error)

    def ws_rts_on_open(self, ws_object):
        """ Callback to be used when the RTS websocket has been opened."""
        thread = threading.Thread(target=self.connect_to_rts, daemon=True)
        thread.start()

    def connect_to_rts(self):
        """ Connect to the RTS service. """
        rts_login_message = get_rts_login_message(self.login_session_id)
        logging.info("Sending login request to the RTS service")
        logging.debug(rts_login_message)
        self.ws_rts.send(rts_login_message)

    def ws_rts_on_message(self, ws_object, message):
        """ Callback to be used when receiving a message from the rts service. """
        logging.debug("RTS message is received: %s", message)
        if not isinstance(message, bytes):
            return

        message_proto = wnt_proto.MessageCollection()
        try:
            message_proto.ParseFromString(message)
        except Exception as e:
            logging.error("An error occured when parsing a rts message: %s", e)
            return

        logging.debug(message_proto)
        with self.rts_lock:
            for msg_proto in message_proto.message_collection:
                if msg_proto.HasField("positioning_status_data"):
                    self.parse_positioning_status_data(msg_proto)
                elif msg_proto.HasField("rtsituation_metadata"):
                    self.parse_rtsituation_metadata(msg_proto)
                elif msg_proto.HasField("node_metadata"):
                    self.parse_anchor_proto(msg_proto)
                else:
                    logging.debug("A message collection has been received by rts service but not parsed "
                                  "as a node/positioning status/rtsituation metadata.")

    def parse_positioning_status_data(self, anchor_proto):
        """ Return True if the positioning status has been started. """
        if anchor_proto.positioning_status_data is not None \
                and anchor_proto.positioning_status_data.code == wpe_proto.Status.CODE.STARTED:
            logging.info("The positioning is starting, it means the configuration has been received!")
            self.nb_rts_services_started += 1

            if self.nb_rts_services == self.nb_rts_services_started:
                self.close_ws_rts()

            return True

        return False

    def parse_anchor_proto(self, anchor_proto):
        """ Parse an anchor node metadata proto message. """
        self.rts_anchor_protos.append(anchor_proto)

    def parse_rtsituation_metadata(self, rtsituation_metadata_proto):
        """ Parse a RTSituationMetadata proto message. """
        if rtsituation_metadata_proto.rtsituation_metadata.HasField("cluster_size"):
            self.nb_rts_services = rtsituation_metadata_proto.rtsituation_metadata.cluster_size

    def get_anchor_data(self) -> list:
        """ Parse anchor node data protobuf and return them in a wpe json format. """
        data = []
        if not self.query_anchors:
            logging.warning('get_anchor_data method was called but the object did not query anchors!')
            return data

        if not self._anchor_data:
            with self.rts_lock:
                for anchor_proto in self.rts_anchor_protos:
                    try:
                        node = Node.from_wnt_proto(anchor_proto)
                        if not node.is_anchor or (self.network_id and node.network_id != self.network_id):
                            continue

                        data.append(node.to_dict())
                    except:
                        logging.exception("An anchor data could not be parsed!")
                self._anchor_data = data

        logging.info("%d anchors have been found!", len(self._anchor_data))
        return self._anchor_data

    @staticmethod
    def run(ws):
        """ Make a websocket running.

        Args:
            ws: Websocket to run.
        """
        ws.run_forever(
            sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False},
            ping_interval=10
        )

    def run_manager(self):
        """
        Make the AreaWebsocketManager query for data and store those in a metadata file.
        If the connection has not been established yet,
        the connection and disconnection are included.
        """
        # Boolean to do the connection and disconnection if it is not established yet
        do_connect = not self.login_session_id
        if do_connect:
            self.connect()

        if self.query_anchors:
            self.is_ws_rts_end_event.clear()
            rts_thread = threading.Thread(target=self.run, args=(self.ws_rts,), daemon=True)
            rts_thread.start()

        self.is_ws_metadata_end_event.clear()
        metadata_thread = threading.Thread(target=self.run, args=(self.ws_metadata,), daemon=True)
        metadata_thread.start()

        cf.wait_for_events(events=[self.is_ws_rts_end_event,
                                   self.is_ws_metadata_end_event],
                           timeout_s=self.timeout_s)

        if do_connect:
            self.close_websockets()

        # Generates output file
        self.generate_file()
