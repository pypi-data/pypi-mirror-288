"""
File to store classes used for a standard representation of the WNT/WPE objects.
It allows to store and display the object as a reference for the other modules.
These classes provide methods to convert the objects to/from the WPE/WNT protobuf objects.
"""
from wirepas_wpe_apt import wnt_proto, wpe_proto
from google.protobuf import json_format
import json
import math
import numpy as np


def get_proto_field(proto, field):
    """ Return the field value of a protobuf object if it is defined, otherwise return None"""
    if proto.HasField(field):
        return proto.__getattribute__(field)

    return None


def degrees_to_radians(degrees):
    """ Function that converts a degrees angle into a radian one.

    Args:
        degrees (float): The angle to convert.

    Returns (float): The radian angle.
    """
    return degrees * math.pi / 180


class Element:
    def to_wpe_proto(self):
        """ Create a wpe protobuf object from the Element object. """
        raise NotImplementedError

    def to_dict(self):
        """ Return its dictionary representation. """
        return dict(self)

    @classmethod
    def from_wpe_proto(cls, wpe_proto_obj):
        """ Create an object from a wpe protobuf object. """
        raise NotImplementedError

    @classmethod
    def from_wnt_proto(cls, wnt_proto_obj):
        """ Create an object from a wnt protobuf object. """
        raise NotImplementedError

    @classmethod
    def from_dict(cls, json_obj: dict):
        """ Create an object from its dictionary representation. """
        raise NotImplementedError

    def __iter__(self):
        for (attr, value) in self.__dict__.items():
            if value is not None:
                if isinstance(value, list) and len(value) and isinstance(value[0], Element):
                    yield (attr, [dict(element) for element in value.__iter__()])
                else:
                    if isinstance(value, Element):
                        value = dict(value)
                    yield (attr, value)

    def __str__(self):
        return json.dumps(dict(self), indent=4)


class Coordinate(Element):
    """
    Internal representation of a coordinate in the network.
    """
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def to_wpe_proto(self):
        wpe_node_obj = wpe_proto.Point()
        wpe_node_obj.geoid = wpe_proto.Point.GEOID.WGS84
        wpe_node_obj.lla_precise.extend([self.latitude, self.longitude, self.altitude])

        return wpe_node_obj

    def lla(self):
        return [self.latitude, self.longitude, self.altitude]

    @classmethod
    def from_coordinates(cls, proto_obj):
        """ Create a Coordinate object from a proto object
        with latitude/longitude/altitude attributes.
        """
        return Coordinate(latitude=proto_obj.latitude,
                          longitude=proto_obj.longitude,
                          altitude=proto_obj.altitude)

    @classmethod
    def from_dict(cls, json_obj: dict):
        return cls(**json_obj)

    def distance_meters_to(self, other, height_calculated=True):
        """ Calculates the distance between 2 points with geo coordinates in decimal degrees.

        Args:
            other (Coordinate): A node to calculate the distance to.
            height_calculated (bool): True if we want to calculate the distance while taking account of the height.
                                    False if we don't.

        Returns (int): The distance in meters between the 2 point
        """
        earth_radius_meter: int = 6371009
        d_lat = degrees_to_radians(self.latitude - other.latitude)
        d_lon = degrees_to_radians(self.longitude - other.longitude)

        lat1 = degrees_to_radians(self.latitude)
        lat2 = degrees_to_radians(other.latitude)

        a = math.sin(d_lat / 2)**2 + math.sin(d_lon / 2)**2 * math.cos(lat1) * math.cos(lat2)
        distance = earth_radius_meter * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        # distance in meter calculated thanks to the latitude and longitude.

        if height_calculated:  # taking account of height of point
            distance = math.sqrt(distance**2 + (self.altitude - other.altitude)**2)

        return distance


class Node(Element):
    """
    Internal representation of a device in the network.
    """
    def __init__(
        self,
        coordinate,
        address=None,
        network_id=None,
        is_anchor=None,
        map_identifier=None,
        area_identifier=None,
        measurement_offset=None,
        timestamp=None,
        name=None,
        description=None
    ):
        """
        Args:
            coordinate (Coordinate): Coordinate of the node.
            address (int): Node's address
            network_id (int): Network id
            is_anchor (bool): Node's role. If true the node in an anchor, otherwise it is an asset
            map_identifier (list): List of map identifier to locate the node.
            area_identifier (list): List of area identifier to locate the node.
            measurement_offset (float): Offset used for RSSI measurements.
            timestamp (int): Timetamp of the measurement in miliseconds.
            name (str): Name of the node.
            description (str): Description the node.
        """
        self.coordinate = coordinate
        self.address = address
        self.network_id = network_id
        self.is_anchor = is_anchor
        self.map_identifier = map_identifier
        self.area_identifier = area_identifier
        self.measurement_offset = measurement_offset
        self.timestamp = timestamp
        self.name = name
        self.description = description

    def to_wpe_proto(self):
        wpe_node_obj = wpe_proto.Node()
        wpe_node_obj.coordinates.CopyFrom(self.coordinate.to_wpe_proto())

        if self.address is not None:
            wpe_node_obj.address = self.address

        if self.network_id is not None:
            wpe_node_obj.network = int(self.network_id)

        if self.is_anchor is not None and self.is_anchor:
            wpe_node_obj.role = wpe_proto.Node.BASEROLE.HEADNODE
        else:
            wpe_node_obj.role = wpe_proto.Node.BASEROLE.SUBNODE

        if self.map_identifier is not None:
            wpe_node_obj.map_identifier = self.map_identifier[0]

        if self.area_identifier is not None:
            wpe_node_obj.geo_identifier.extend(self.area_identifier)

        if self.timestamp is not None:
            wpe_node_obj.timestamp = int(self.timestamp)

        if self.measurement_offset is not None:
            wpe_node_obj.measurement_offset = self.measurement_offset

        return wpe_node_obj

    @classmethod
    def from_wpe_proto(cls, wpe_proto_obj):
        coordinates = wpe_proto_obj.coordinates.lla_precise or wpe_proto_obj.coordinates.lla
        latitude, longitude, altitude = coordinates
        coordinate = Coordinate(float(latitude), float(longitude), float(altitude))

        map_identifier = area_identifier = None

        if len(wpe_proto_obj.map_identifier):
            map_identifier = [wpe_proto_obj.map_identifier]

        if len(wpe_proto_obj.geo_identifier):
            area_identifier = list(wpe_proto_obj.geo_identifier)

        return Node(coordinate=coordinate,
                    address=get_proto_field(wpe_proto_obj, "address"),
                    network_id=get_proto_field(wpe_proto_obj, "network"),
                    is_anchor=(wpe_proto_obj.role == wpe_proto.Node.BASEROLE.HEADNODE),
                    map_identifier=map_identifier,
                    area_identifier=area_identifier,
                    measurement_offset=get_proto_field(wpe_proto_obj, "measurement_offset"),
                    timestamp=get_proto_field(wpe_proto_obj, "timestamp"))

    @classmethod
    def from_wnt_proto(cls, wnt_proto_obj):
        coordinate = Coordinate.from_coordinates(wnt_proto_obj.node_metadata)
        map_identifier = area_identifier = None

        if len(wnt_proto_obj.node_metadata.map_uuid):
            map_identifier = list(wnt_proto_obj.node_metadata.map_uuid)

        if len(wnt_proto_obj.node_metadata.area_uuid):
            area_identifier = list(wnt_proto_obj.node_metadata.area_uuid)

        return Node(coordinate=coordinate,
                    address=get_proto_field(wnt_proto_obj, "source_address"),
                    network_id=get_proto_field(wnt_proto_obj, "network_id"),
                    is_anchor=(wnt_proto_obj.node_metadata.positioning_role == wnt_proto.NodeMetadata.PositioningRole.ANCHOR),
                    map_identifier=map_identifier,
                    area_identifier=area_identifier,
                    measurement_offset=get_proto_field(wnt_proto_obj.node_metadata, "rssi_offset"),
                    timestamp=get_proto_field(wnt_proto_obj, "tx_time"),
                    name=get_proto_field(wnt_proto_obj.node_metadata, "name"),
                    description=get_proto_field(wnt_proto_obj.node_metadata, "description"))

    @classmethod
    def from_dict(cls, json_obj: dict):
        coordinate_obj = Coordinate.from_dict(json_obj.pop("coordinate"))
        return cls(coordinate=coordinate_obj, **json_obj)


class Area(Element):
    """
    Internal representation of an area.
    """
    def __init__(
        self,
        coordinates,
        identifier,
        floor_plan_identifier,
        name=None,
        colors=None,
        timestamp=None
    ):
        """
        Args:
            coordinates (list): list of coordinates delimiting the area outline.
            identifier (str): Unique id to identify the area.
            floor_plan_identifier (str): Identifier of the floor plan containing the area.
            name (str): Name of the area.
            colors (dict): A dictionary containing: alpha, and RGB color value of the area in the WNT backend.
                Example: {'A': 80, 'R': 0, 'G': 255, 'B': 255}.
            timestamp (int): Timetamp of the measurement in miliseconds.
        """
        self.coordinates = coordinates
        self.identifier = identifier
        self.floor_plan_identifier = floor_plan_identifier
        self.name = name
        self.colors = colors
        self.timestamp = timestamp

    def to_wpe_proto(self):
        wpe_area_obj = wpe_proto.Area()

        if self.name is not None:
            wpe_area_obj.name = self.name

        if self.identifier is not None:
            wpe_area_obj.uuid = self.identifier

        if self.floor_plan_identifier is not None:
            wpe_area_obj.map_identifier = self.floor_plan_identifier

        if self.coordinates is not None:
            wpe_points = [coordinate.to_wpe_proto() for coordinate in self.coordinates]
            wpe_area_obj.coordinates.extend(wpe_points)

        return wpe_area_obj

    @classmethod
    def from_wpe_proto(cls, wpe_proto_obj):
        coordinates = []
        for point in wpe_proto_obj.coordinates:
            coordinate = point.lla_precise or point.lla
            coordinates.append(Coordinate(*coordinate))

        return Area(coordinates=coordinates,
                    identifier=wpe_proto_obj.uuid,
                    floor_plan_identifier=wpe_proto_obj.map_identifier,
                    name=get_proto_field(wpe_proto_obj, "name"))

    @classmethod
    def from_wnt_proto(cls, wnt_proto_obj):
        """ Create an object from a json with wnt proto structure. """
        coordinates = [Coordinate.from_coordinates(point) for point in wnt_proto_obj.polygon_points]

        update_time = get_proto_field(wnt_proto_obj, "update_time")
        if update_time:
            update_time *= 1000  # Conversion from seconds to miliseconds

        return Area(coordinates=coordinates,
                    identifier=wnt_proto_obj.id,
                    floor_plan_identifier=wnt_proto_obj.floor_plan_id,
                    name=get_proto_field(wnt_proto_obj, "name"),
                    colors=json_format.MessageToDict(wnt_proto_obj.color),
                    timestamp=update_time)

    @classmethod
    def from_dict(cls, json_obj: dict):
        coordinates = json_obj.pop("coordinates")
        coordinate_objs = [Coordinate.from_dict(coord) for coord in coordinates]
        return cls(coordinates=coordinate_objs, **json_obj)

    def get_color(self):
        """ Return the color RGBA of an area with the values between 0 and 1.

        Returns (tuple): The tuple (red, green, blue, alpha) with values
                between 0 and 1.
        """
        alpha = self.colors["A"] / 255
        red = self.colors["R"] / 255
        green = self.colors["G"] / 255
        blue = self.colors["B"] / 255
        return red, green, blue, alpha


class Measurement(Element):
    """
    Internal representation of a mesurement.
    """
    class MeasureData(Element):
        def __init__(self, type, target, value, time=None):
            """
            Args:
                type (wpe_proto.MeasurementData.DOMAIN): Type of the measurement.
                target (int): To whom the measurement is done.
                value (float): Measurement value
                time (float): Amount of seconds to when measurement was done.
            """
            self.type = wpe_proto.MeasurementData.DOMAIN.Name(type)
            self.target = target
            self.value = value
            self.time = time

        @classmethod
        def from_wnt_proto(self, wpe_proto_obj):
            return Measurement.MeasureData(wpe_proto_obj.type,
                                           wpe_proto_obj.target,
                                           wpe_proto_obj.value,
                                           get_proto_field(wpe_proto_obj, "time"))

        def to_wpe_proto(self):
            return json_format.ParseDict(dict(self), wpe_proto.MeasurementData())

        @classmethod
        def from_dict(cls, json_obj: dict):
            type_domain = json_obj.pop("type")
            return cls(type=wpe_proto.MeasurementData.DOMAIN.Value(type_domain), **json_obj)

    def __init__(self, measures, address, network_id, timestamp=None,
                 version=None, use_strongest_neighbors=None):
        """
        Args:
            measures (list): Measurement data of a position.
            address (int): Node's address.
            network_id (int): Network id.
            timestamp (int): Timetamp of the measurement in miliseconds.
            version(float): Version.
            use_strongest_neighbors (int): Number of strongest neighbors to use.
        """
        self.address = address
        self.network_id = network_id
        self.timestamp = timestamp
        self.version = version
        self.measures = measures
        self.use_strongest_neighbors = use_strongest_neighbors

    def to_wpe_proto(self):
        wpe_meas_obj = wpe_proto.MeshData()

        if self.address is not None:
            wpe_meas_obj.source = self.address

        if self.network_id is not None:
            wpe_meas_obj.network = self.network_id

        if self.version is not None:
            wpe_meas_obj.version = self.version

        if self.timestamp is not None:
            wpe_meas_obj.timestamp = self.timestamp

        if self.measures is not None:
            wpe_meas_obj.payload.extend([mes.to_wpe_proto() for mes in self.measures])

        if self.use_strongest_neighbors is not None:
            wpe_meas_obj.use_strongest_neighbors = self.use_strongest_neighbors

        return wpe_meas_obj

    @classmethod
    def from_wpe_proto(cls, wpe_proto_obj):
        mesures = [Measurement.MeasureData.from_wnt_proto(measure) for measure in wpe_proto_obj.payload]

        return Measurement(measures=mesures,
                           address=wpe_proto_obj.source,
                           network_id=wpe_proto_obj.network,
                           timestamp=get_proto_field(wpe_proto_obj, "timestamp"),
                           version=get_proto_field(wpe_proto_obj, "version"),
                           use_strongest_neighbors=get_proto_field(wpe_proto_obj, "use_strongest_neighbors"))

    @classmethod
    def from_wnt_proto(cls, wnt_proto_obj):
        mesures = [Measurement.MeasureData.from_wnt_proto(measure) for measure in wnt_proto_obj.positioning_mesh_data.payload]

        return Measurement(
            measures=mesures,
            address=wnt_proto_obj.source_address,
            network_id=wnt_proto_obj.network_id,
            timestamp=get_proto_field(wnt_proto_obj, "tx_time"),
            version=get_proto_field(wnt_proto_obj.positioning_mesh_data, "version"),
            use_strongest_neighbors=get_proto_field(wnt_proto_obj.positioning_mesh_data, "use_strongest_neighbors")
        )

    @classmethod
    def from_dict(cls, json_obj: dict):
        measures = json_obj.pop("measures")
        measure_objs = [Measurement.MeasureData.from_dict(measure) for measure in measures]
        return cls(measures=measure_objs, **json_obj)


class FloorPlan(Element):
    """
    Internal representation of a floor plan.
    """
    def __init__(self, **kwargs):
        """
        Permissive class to represent a floor plan.
        It must at least have an id, a rotation matrix, an image and its dimension width/height,
        the number pixels per meter and the offset for the conversion local to ecef and ecef to local.
        """
        assert "id" in kwargs, "An identifier 'id' must be provided when setting a floor plan!"
        assert "rotation_matrix" in kwargs, "'rotation_matrix' must be provided when setting a floor plan!"
        assert "image" in kwargs, "An 'image' must be provided when setting a floor plan!"
        assert "image_width" in kwargs, "'image_width' must be provided when setting a floor plan!"
        assert "image_height" in kwargs, "'image_height' must be provided when setting a floor plan!"
        assert "pixels_per_meter" in kwargs, "'pixels_per_meter' must be provided when setting a floor plan!"
        assert "offset_ecef_to_local" in kwargs, "'offset_ecef_to_local' must be provided when setting a floor plan!"
        assert "offset_local_to_ecef" in kwargs, "'offset_local_to_ecef' must be provided when setting a floor plan!"

        for field, value in kwargs.items():
            self.__setattr__(field, value)

    @classmethod
    def from_dict(cls, json_obj: dict):
        return FloorPlan(**json_obj)

    def wgs84_to_pixel(self, coordinates):
        """ Convert wgs84 coordinates into pixel in the floor image.

        Args:
            coordinates (Coordinate): Coordinates of a point

        Return: Pixel positions of the point in the image.
        """
        latitude = coordinates.latitude
        longitude = coordinates.longitude
        altitude = coordinates.altitude

        latitude = degrees_to_radians(latitude)
        longitude = degrees_to_radians(longitude)

        pixels_per_meter = self.pixels_per_meter
        rotation_matrix = np.array(list(self.rotation_matrix.values()))
        rotation_matrix = np.reshape(rotation_matrix, (3, 3))
        translation_matrix = np.array(list(self.offset_local_to_ecef.values()))
        translation_matrix = np.reshape(translation_matrix, (3, 1))

        E = self.wgs84_to_ecef(latitude, longitude, altitude)
        r = np.dot(rotation_matrix, E - translation_matrix) * pixels_per_meter
        x_pixel, y_pixel, _ = np.reshape(r, 3).tolist()

        return [x_pixel, y_pixel]

    def wgs84_to_ecef(self, latitude, longitude, altitude=0):
        """ Convert wgs84 coordinates to ecef. """
        a = 6378137.0
        e2 = 0.00669437999014133
        v = a / math.sqrt(1 - e2 * math.sin(latitude)**2)

        # calculating ECEF coordinates
        x = (v + altitude) * math.cos(latitude) * math.cos(longitude)
        y = (v + altitude) * math.cos(latitude) * math.sin(longitude)
        z = (v * (1 - e2) + altitude) * math.sin(latitude)
        E = np.array([x, y, z])
        return np.reshape(E, (3, 1))
