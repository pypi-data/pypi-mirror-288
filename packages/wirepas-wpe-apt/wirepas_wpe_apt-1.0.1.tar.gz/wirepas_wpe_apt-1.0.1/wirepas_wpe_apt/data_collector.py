# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import argparse
import json
import logging
import os
import pandas as pd
import requests
import sys

from wirepas_wpe_apt.areas_websocket_manager import AreaWebsocketManager
from wirepas_wpe_apt import common_functions as cf
from wirepas_wpe_apt.constants import *
from wirepas_wpe_apt.element import *


class QueryComparisonCondition():
    """ Condition class to add condition in database queries. """
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

    def value_to_influx(self, value_to_str, version: int):
        """ Return the string representation of a value in influxql. """
        if self.type == float or self.type == int or self.type == bool:
            if value_to_str is None:
                return '0'
            return str(value_to_str)

        if self.type == str:
            return self.add_str_quotes(value_to_str, version)

    @staticmethod
    def add_str_quotes(value: str, version):
        """ Add string quote to a value. """
        if version == 1:
            if value:
                return "'" + value + "'"
            return "''"
        elif version == 2:
            if value:
                return '"' + value + '"'
            return '""'

    def to_influx(self) -> str:
        """ Return a influxql compatible string condition. """
        raise NotImplementedError


class IsEqual(QueryComparisonCondition):
    def to_influx(self):
        return f'{self.name} = {self.value_to_influx(self.value, 1)}'


class IsNotEqual(QueryComparisonCondition):
    def to_influx(self):
        return f'{self.name} != {self.value_to_influx(self.value, 1)}'


class DataCollector:
    def __init__(self, configuration, network_id, reference_network_id,
                 folder_path="wpeapt_data", node_list=None, time_start=None,
                 time_end=None, reference_area_names_file=None, limit=10000,
                 query_anchors_from_rts=False, timeout_s=60):
        """ Initiate the Data Collector.
        A tool to get data from a backend and to store those in files.

        Args:
            configuration (str): Configuration file containing the needed credentials.
            network_id (int): The network id for the measurements and configuration.
            reference_network_id (int): The network id for references of the nodes.
            folder_path: Default to "wpeapt_data". Path of the folder to store the collected data.
            node_list (list(int)): The list of nodes to get the values.
            time_start (str): Condition on the starting time.
            time_end (str): Condition on the ending time.
            reference_area_names_file (str): Name of a json file to maps the reference positions
                of tags to their respective areas. When getting an area from the WNT
                Those are not linked to any areas. This option allow to fix this issue
                by providing a mapping between the node id of the reference positions and their area names.

                Example of content for this file:
                {
                    "1": [
                        "Area name 1"
                    ],
                    "2": [
                        "Area name 1"
                    ],
                    "3": [
                        "Area name 2"
                    ]
                }

            limit (int): Default to 10000. Limit of the number of element taken on the query.
            query_anchors_from_rts (bool): True to query anchors from rts to get a static configuration
                else it will get the anchor data from the influx database.
            timeout_s (int): Default to 60. Timeout in seconds for each queries.
        """
        self.data_collector_configuration_file = configuration

        self.network_configuration_file = os.path.join(folder_path, "data", "network_configuration.json")
        self.reference_file = os.path.join(folder_path, "data", "reference.json")
        self.computed_locations_file = os.path.join(folder_path, "data", "computed_locations.json")
        self.metadata_file = os.path.join(folder_path, "data", "metadata.json")

        configuration_data = cf.get_data_json(configuration)
        try:
            self.influxdb_hostname = configuration_data["wnt_hostname"]
            self.influxdb_password = configuration_data["wnt_password"]
            self.influxdb_username = configuration_data["wnt_username"]
            self.influxdb_port = configuration_data.get("influxdb_port", 8886)
            self.influxdb_ssl = configuration_data.get("influxdb_ssl", True)
            self.influxdb_verify_ssl = configuration_data.get("influxdb_verify_ssl", True)
            self.influxdb_database = configuration_data.get("influxdb_database", "wirepas")
            self.anchors_dataset = configuration_data.get("anchors_dataset", "node_metadata")
            self.measurements_dataset = configuration_data.get("measurements_dataset", "location_measurement")
            self.references_dataset = configuration_data.get("references_dataset", "node_metadata")
            self.locations_dataset = configuration_data.get("locations_dataset", "location_update")
        except KeyError as error:
            raise KeyError("The configuration file should contain all the values "
                           "needed for the data collector to work properly. "
                           "Check the README.md for more information!") from error

        self.network_id = network_id
        self.reference_network_id = reference_network_id
        self.node_list = node_list
        self.time_start = time_start
        self.time_end = time_end
        self.limit = limit
        self.query_anchors_from_rts = query_anchors_from_rts
        self.timeout_s = timeout_s

        self.reference_area_names = None
        try:
            if reference_area_names_file:
                self.reference_area_names = {
                    int(nodeid, 0): area
                    for nodeid, area in cf.get_data_json(reference_area_names_file).items()
                }
        except ValueError as e:
            raise ValueError("reference_area_names file is incorrect, please use "
                             "`wirepas_apt_data_collector --help` command "
                             "to see its expected content.") from e

        self.areas_manager = AreaWebsocketManager(
            self.data_collector_configuration_file,
            self.metadata_file,
            query_anchors=self.query_anchors_from_rts,
            network_id=self.network_id,
            tls_secured=self.influxdb_ssl,
            timeout_s=self.timeout_s
        )
        self.influxdb_token = None

    def data_query(self, *args, limit=None, **kwargs):
        """ Send a http query to the Influx database
        according to the conditions put into parameters.
        A limit or time interval should be put to avoid the database
        to be overcharged by this query.

        Args:
            dataset (str): Influx dataset to search the data in.
            network_id (int): Network id.
            data_fields (list): Selection of the fields on the dataset.
                                Default to None to query all fields.
            additional_condition (str): Used to add other conditions if needed,
                                        it must be influxql compatible.
            node_list (list(int)): The list of nodes to get the values.
            time_end(str) : Condition on the ending time.
            time_start (str): Condition on the starting time.
            limit (int): Limit of the number of element taken on the query.

        Returns (Iterable): An iterable containing the results of the query.
        """
        http = "https" if self.influxdb_ssl else "http"
        url = f"{http}://{self.influxdb_hostname}:{self.influxdb_port}/query"
        influxql_query = self.generate_data_query(*args, limit=limit, **kwargs)
        logging.info("Sending the data request %s", influxql_query)

        try:
            if self.influxdb_token:
                headers = {
                    'Authorization': 'Token {}'.format(self.influxdb_token),
                }
                parameters = {
                    'epoch': 's',
                    'db': self.influxdb_database,
                    'q': influxql_query
                }
                response = requests.get(url, params=parameters, headers=headers, timeout=self.timeout_s)
            else:
                parameters = {
                    'u': self.influxdb_username,
                    'p': self.influxdb_password,
                    'epoch': 's',
                    'db': self.influxdb_database,
                    'q': influxql_query
                }
                response = requests.get(url, params=parameters, timeout=self.timeout_s)
        except requests.exceptions.ConnectTimeout:
            raise ConnectionError(f"A timeout occured when sending a data request to {url}!") from None

        # Get and convert results
        if str(response.status_code) != "200":
            logging.error("An error occured when sending the SQL request to the db, "
                          "error code: %d, reason: %s", response.status_code, response.reason)
            return []

        results = response.json()["results"][0]
        if "series" not in results:
            logging.warning("No element have been found in the response from the influx database!")
            return []

        # Parse the data inside the json response as a dataframe
        # to map the columns with the values.
        df = pd.DataFrame(results["series"][0]["values"],
                          columns=results["series"][0]["columns"])

        logging.info("%d elements have been found!", len(df))
        if limit == len(df):  # Raise a warning if the limit of the query is reached.
            logging.warning("The limit of %d elements per query has been reached!", limit)

        return df.to_dict(orient="records")

    def generate_data_query(self, dataset, network_id=None, data_fields=None,
                            additional_condition=None, node_list=None,
                            time_end=None, time_start=None, limit=None) -> str:
        """ Generate a influxQL request.

        Args:
            dataset (str): Influx dataset to search the data in.
            network_id (int): Network id.
            data_fields (list): Selection of the fields on the dataset.
                                Default to None to query all fields.
            additional_condition (str): Used to add other conditions if needed,
                                        it must be influxql_query compatible.
            node_list (list(int)): The list of nodes to get the values.
            time_end(str) : Condition on the ending time.
            time_start (str): Condition on the starting time.
            limit (int): Limit of the number of element taken on the query.
        """
        data_fields_to_query = "*"
        if data_fields is not None:
            data_fields_to_query = ",".join(data_fields)

        query_string = f"SELECT {data_fields_to_query} FROM \"{dataset}\""
        and_where: bool = False  # Boolean to know when to add WHERE and AND in the FROM condition
        where_string = " WHERE"

        def where_condition() -> str:
            nonlocal and_where
            if and_where:
                return " AND"
            else:
                and_where = True
                return where_string

        if additional_condition is not None:
            if isinstance(additional_condition, QueryComparisonCondition):
                query_string += where_condition() + " " + additional_condition.to_influx()
            elif isinstance(additional_condition, list):
                for condition in additional_condition:
                    query_string += where_condition() + " " + condition.to_influx()

        if network_id is not None:
            query_string += where_condition() + f" network_id='{network_id}'"

        if node_list is not None:
            query_string += where_condition() + " ("
            count = 0
            for nodeid in node_list:
                if count != 0:
                    query_string += " OR"

                count += 1
                query_string += f" nodeid = {nodeid}"

            query_string += ")"

        if time_start is not None:
            # Influxql differentiate time and string literals
            if "now()" in time_start:
                query_string += where_condition() + f" time > {time_start}"
            else:
                query_string += where_condition() + f" time > '{time_start}'"

        if time_end is not None:
            if "now()" in time_end:
                query_string += where_condition() + f" {time_end} > time"
            else:
                query_string += where_condition() + f" '{time_end}' > time"

        # to ensure that the data are ordered by time for erasing duplicated
        # informations for reference and anchor nodes.
        query_string += " ORDER BY time DESC"

        if limit is not None:
            query_string += f" LIMIT {limit}"

        return query_string

    def remove_duplicate_nodes(self, nodes):
        """ Suppress all duplicate node data of an iterable.

        Args:
            nodes: Node data iterable with potentially redundant nodes.

        Returns (list): Non duplicate nodes list.
        """
        logging.debug("Removing duplicate node ids!")
        used_node_ids = set()
        non_redundant_nodes = []
        for node in nodes:
            node_id = node["nodeid"]
            if node_id not in used_node_ids:
                used_node_ids.add(node_id)
                non_redundant_nodes.append(node)

        return non_redundant_nodes

    def query_anchors(self):
        """ Gets all the anchors related to a network with redundance
        and returns a generator containing the values needed to define these.

        Returns (iter): A generator containing the anchors in a network.
        """
        logging.info("Query anchors data!")
        anchors = self.data_query(
            dataset=self.anchors_dataset,
            network_id=self.network_id,
            additional_condition=[  # not to get anchor without coordinates
                IsEqual(INFLUX_POSITIONING_ROLE, INFLUX_ANCHOR_ROLE, int),
                IsNotEqual(INFLUX_LATITUDE, None, float),
                IsNotEqual(INFLUX_LONGITUDE, None, float),
            ],
            time_end=self.time_end
        )

        unique_anchors = self.remove_duplicate_nodes(anchors)
        if not unique_anchors:
            logging.warning("No anchors have been taken from the database")
        else:
            logging.info("%d different anchors have been found!", len(unique_anchors))

        return [Node.from_wnt_proto(cf.parse_influxdata(anchor)).to_dict()
                for anchor in unique_anchors]

    def query_measurements(self):
        """ Gets all the measurement data related to a network
        and returns a list containing the values needed to define these.

        Returns (iter): A list of the measurements of nodes in a network.
        """
        logging.info("Query measurements data!")
        measurements = self.data_query(
            dataset=self.measurements_dataset,
            network_id=self.network_id,
            additional_condition=IsNotEqual(INFLUX_PAYLOAD, None, str),  # not to get empty measurements
            time_start=self.time_start,
            node_list=self.node_list,
            time_end=self.time_end,
            limit=self.limit
        )

        if not measurements:
            logging.warning("No measurements have been taken from the database")

        return [Measurement.from_wnt_proto(cf.parse_influxdata(measurement)).to_dict()
                for measurement in measurements]

    def query_references(self):
        """ Returns the references of the tags related to a network. """
        logging.info("Query reference data!")
        references = self.data_query(
            dataset=self.references_dataset,
            network_id=self.reference_network_id,
            additional_condition=[  # Not to get references without coordinates or map.
                IsNotEqual(INFLUX_LATITUDE, None, float),
                IsNotEqual(INFLUX_LONGITUDE, None, float),
                IsNotEqual(INFLUX_MAP_UUID, None, str),
                IsEqual(INFLUX_IS_VIRTUAL, True, bool),
            ],
            node_list=self.node_list
        )

        unique_references = self.remove_duplicate_nodes(references)
        if not unique_references:
            raise ValueError("No references have been taken from the database. "
                             "Please check that the references are referenced as virtual in the WNT. "
                             "And check the reference_network_id and the node list input.")
        else:
            logging.info("%d different reference data have been found!", len(unique_references))

        return [Node.from_wnt_proto(cf.parse_influxdata(node)).to_dict()
                for node in unique_references]

    def query_mesured_positions(self):
        """ Returns the mesured positions of the tags related to a network. """
        logging.info("Query mesured positions!")
        positions = self.data_query(
            dataset=self.locations_dataset,
            network_id=self.network_id,
            additional_condition=[
                IsNotEqual(INFLUX_LATITUDE, None, float),
                IsNotEqual(INFLUX_LONGITUDE, None, float),
            ],
            node_list=self.node_list,
            time_start=self.time_start,
            time_end=self.time_end,
            limit=self.limit
        )

        if not positions:
            raise ValueError("No positions have been taken from the database. "
                             "Please check carefully that the tags are supposed to have "
                             "computed positions with the input parameters!")

        return [Node.from_wnt_proto(cf.parse_influxdata(node)).to_dict()
                for node in positions]

    def get_configure_data(self, get_measurements: bool = True):
        """ Query measurements, anchors from influx database, and metadata
        informations like areas, floor plans.

        Args:
            get_measurements: Boolean to know whether the measurements data need to be queried/stored.

        Returns: Outputs a JSON format of the data in a
        {
            "network": (str),
            "nodes": (list(dict)),
            "areas": (list(dict)),
            "measurements": (list(dict))  # Optional
        } format
        """
        configuration = {NETWORK_FIELD: str(self.network_id)}

        # Query the metadata services.
        self.areas_manager.run_manager()

        # Get anchors data.
        if self.query_anchors_from_rts:
            configuration[NODES_FIELD] = self.areas_manager.get_anchor_data()
        else:
            configuration[NODES_FIELD] = self.query_anchors()

        # Get measurements data.
        if get_measurements:
            configuration[MEASUREMENTS_FIELD] = self.query_measurements()

        metadata = cf.get_data_json(self.metadata_file)
        configuration[AREAS_FIELD] = metadata[AREAS_FIELD]
        return configuration

    def get_reference_data(self):
        """ Query and configure reference data.

        Returns: A JSON format of the data in a
        {
            "network": (str),
            "nodes": (list(dict))
        } format
        """
        references = {}
        references[NETWORK_FIELD] = str(self.reference_network_id)
        references[NODES_FIELD] = self.query_references()

        return references

    def get_mesured_positions(self):
        """ Query mesured tag positions in the WPE.

        Returns: A JSON format of the data in a
        {
            "network": (str),
            "nodes": (list(dict))
        } format
        """
        positions = {}
        positions[NETWORK_FIELD] = str(self.network_id)
        positions[NODES_FIELD] = self.query_mesured_positions()

        return positions

    def store_data(self, filename, json_data):
        """ Store data in a file in the data folder. """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as data_file:
            json.dump(json_data, data_file, indent=4)

    def query_and_store_data(self, get_computed_locations=True, get_measurements=True):
        """ Gets the measurement data related to a network and returns
        a generator containing the values needed to define these.

        Args:
            network_configuration_file (str): If provided, name of the file where the
                configuration and measurements of the network will be stored.
            reference_file_name (str): If provided, name of the file where
                the reference data of the nodes will be stored.
            computed_locations_file (str): If provided, name of the file
                where the computed locations data of the tags will be stored.
        """
        # Get metadata.
        self.areas_manager.connect()
        self.influxdb_token = self.areas_manager.get_influx_token()

        try:
            # Get network configuration data.
            network_configuration_data = self.get_configure_data(get_measurements)
            logging.info("Store configuration data in %s", self.network_configuration_file)
            self.store_data(self.network_configuration_file, network_configuration_data)

            # Get reference data.
            references_data = self.get_reference_data()

            # Add reference areas id if possible
            if self.reference_area_names:
                for reference in references_data[NODES_FIELD]:
                    if int(reference["address"]) not in self.reference_area_names:
                        continue

                    for reference_area_name in self.reference_area_names[int(reference["address"])]:
                        # Check all areas and add the ones with the same names.
                        for area_id, area in network_configuration_data.get(AREAS_FIELD, {}).items():
                            if area.get("name") == reference_area_name:
                                if "area_identifier" not in reference:
                                    reference["area_identifier"] = []
                                reference["area_identifier"].append(area_id)

            logging.info("Store reference data in %s", self.reference_file)
            self.store_data(self.reference_file, references_data)

            # Get computed locations data.
            if get_computed_locations:
                positions_data = self.get_mesured_positions()
                logging.info("Store computed locations in %s", self.computed_locations_file)
                self.store_data(self.computed_locations_file, positions_data)
                reference_nodes = {data["address"] for data in references_data["nodes"]}
                position_nodes = {data["address"] for data in positions_data["nodes"]}
                for node in position_nodes:
                    if node not in reference_nodes:
                        logging.warning("Node %d doesn't have any reference!", node)
        finally:
            # Close websocket connections that were used to query the data.
            self.areas_manager.close_websockets()


def nullable_str(string: str):
    if string:
        return string


def nullable_int(integer: str):
    if integer:
        return int(integer)


def any_int(integer: str):
    return int(integer, 0)


def node_list_args(nodes: str):
    if nodes:
        return [int(node, 0) for node in nodes.split(",")]


def main():
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     fromfile_prefix_chars='@')

    parser.add_argument('--configuration', type=str, required=True,
                        help='Configuration file containing the backend credentials.')
    parser.add_argument('--network_id', type=any_int, required=True,
                        help='Network address of the tags to get data from.')
    parser.add_argument('--reference_network_id', type=any_int, required=True,
                        help='Network address of the reference data.')
    parser.add_argument('--folder_path', type=str, default="wpeapt_data",
                        help='Default to "wpeapt_data". '
                        'Path of the folder to store the collected data.')
    parser.add_argument('--node_list', type=node_list_args, default=None,
                        help='Default to None to take all the data. List of nodes to get data from. '
                        'For example: --node_list 1111,2222,3333')
    parser.add_argument('--time_start', type=nullable_str, default=None,
                        help='Default to None. Minimum UTC time of the data to be retrieved. '
                        'It must have the ISO8601 format: "yyyy-MM-ddTHH:mm:ssZ". '
                        'Example of input: "2024-07-10T8:00:00Z"')
    parser.add_argument('--time_end', type=nullable_str, default=None,
                        help='Default to None. Maximum UTC time of the data to be retrieved. '
                        'It must have the ISO8601 format: "yyyy-MM-ddTHH:mm:ssZ". '
                        'Example of input: "2024-07-10T11:00:00Z"')
    parser.add_argument('--reference_area_names_file', type=nullable_str, default=None,
                        help='Name of a json file to maps the reference positions '
                        'of tags to their respective areas. '
                        'When getting reference data from the WNT those are not linked to any areas. '
                        'This option allow to fix this issue by providing a mapping '
                        'between the node id of the reference positions and their area names. '
                        'Example of content for this file:\n'
                        '{\n'
                        '    "1": [\n'
                        '        "Area name 1"\n'
                        '    ],\n'
                        '    "2": [\n'
                        '        "Area name 1"\n'
                        '    ],\n'
                        '    "3": [\n'
                        '        "Area name 2"\n'
                        '    ]\n'
                        '}\n')
    parser.add_argument('--query_anchors_from_rts', action='store_true', default=False,
                        help='Default to False. If used, the anchors data are took from rts. '
                        'Otherwise, it will get the anchor data from the influx database.')
    parser.add_argument('--query_limit', type=nullable_int, default=10000,
                        help='Default to 10000. Limit of data to retrieve when querying the computed data. '
                        'It can be used to protect the database from doing huge queries.')
    parser.add_argument("--log_level", default="info", type=str,
                        choices=["debug", "info", "warning", "error", "critical"],
                        help="Default to 'info'. Log level to be displayed. "
                        "It has to be chosen between 'debug', 'info', 'warning', 'error' and 'critical'")
    parser.add_argument('--timeout_s', type=nullable_int, default=60,
                        help='Default to 60. Timeout in seconds for each queries.')

    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s | [%(levelname)s] %(filename)s:%(lineno)d:%(funcName)s:%(message)s',
        level=args.log_level.upper(),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("data_collector.log", mode="w")
        ]
    )

    # Query services to get data and store it
    data_collector = DataCollector(configuration=args.configuration,
                                   folder_path=args.folder_path,
                                   network_id=args.network_id,
                                   reference_network_id=args.reference_network_id,
                                   node_list=args.node_list,
                                   time_start=args.time_start,
                                   time_end=args.time_end,
                                   reference_area_names_file=args.reference_area_names_file,
                                   limit=args.query_limit,
                                   query_anchors_from_rts=args.query_anchors_from_rts,
                                   timeout_s=args.timeout_s)

    data_collector.query_and_store_data()


if __name__ == '__main__':
    main()
