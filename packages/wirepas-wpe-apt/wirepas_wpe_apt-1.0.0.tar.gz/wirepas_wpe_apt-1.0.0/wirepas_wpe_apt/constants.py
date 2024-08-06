"""
Python module with constants needed for connection with the InfluxDB,
the MQTT client of the WPE, and query/listen to those services.
"""

# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#

# Constants for understanding the WNT/Influxdb mapping values:
## For node metadata
INFLUX_LATITUDE: str = "Message_73_1"
INFLUX_LONGITUDE: str = "Message_73_2"
INFLUX_MAP_UUID: str = "Message_73_10"
INFLUX_IS_VIRTUAL: str = "Message_73_23"
INFLUX_POSITIONING_ROLE: str = "Message_73_30"
INFLUX_ANCHOR_ROLE: int = 1

## For meshData:
INFLUX_PAYLOAD: str = "Message_130_8"

# Field names for the general purpose of the tool
NETWORK_FIELD = "network"
NODES_FIELD = "nodes"
MEASUREMENTS_FIELD = "measurements"
MESSAGE_FIELD = "message"
AREAS_FIELD = "areas"
ADDRESS_FIELD = "address"
LOCATION_ERROR_FIELD = "location_error"
MATCH_FLOOR_FIELD = "match_floor"
MATCH_AREA_FIELD = "match_area"
MAP_IDENTIFIER_FIELD = "map_identifier"
REFERENCE_MAP_IDENTIFIER_FIELD = "reference_map_identifier"
MEASUREMENT_TIMESTAMP_FIELD = "measurement_timestamp"
NAME_FIELD = "name"
COMPUTED_LOCATION_FIELD = "computed_location"
REFERENCE_LOCATION_FIELD = "reference_location"
TIMESTAMP_FIELD = "timestamp"
FLOOR_PLANS_FIELD = "floor_plans"
