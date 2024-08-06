# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import argparse

import statistics
import matplotlib.cbook as cbook
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
import os
import sys
import logging
import json
import math
import mpld3
from mpld3 import plugins
from datetime import datetime
from dateutil import parser
from dateutil.parser import ParserError
from importlib.metadata import version
import pytz
import shutil
from typing import List

from wirepas_wpe_apt.constants import *
from wirepas_wpe_apt.element import Coordinate, Node
from wirepas_wpe_apt import common_functions as cf


TITLE_SIZE = 15
DPI = 300


def timestamp_to_str(timestamp):
    """ Return the string representation of a timestamp in ms. """
    return str(datetime.fromtimestamp(int(timestamp) / 1000, tz=pytz.utc)).replace('+00:00', 'Z')


class ResultComparison:
    def __init__(self, reference_node, measurement_node):
        """ Generate a Result comparison between 1 node and its calculated position.
        It contains matches success for the area and floor, the precision on the location
        and all the informations needed to recognise the node in the database.

        Args:
            reference_node (Node): References of a node.
            measurement_node (Node): Computation result of the same node.

        Return (ResultComparison): Result of the comparision between the two nodes.
        """
        self.address: int = reference_node.address
        self.location_error: float = np.nan
        self.match_floor: bool = np.nan
        self.match_area: bool = np.nan
        self.map_identifier: str = np.nan  # Map identifier of the tag calculated position.
        self.reference_map_identifier: str = np.nan  # Map identifier of the reference.
        self.measurement_timestamp: str = timestamp_to_str(measurement_node.timestamp)
        self.reference_location: List[float] = reference_node.coordinate
        self.computed_location: List[float] = measurement_node.coordinate
        self.name = reference_node.name or measurement_node.name

        if reference_node.map_identifier:
            reference_floor_id = reference_node.map_identifier[0]
            tag_floor_id = measurement_node.map_identifier[0]
            self.match_floor = False
            self.reference_map_identifier = reference_floor_id
            self.map_identifier = tag_floor_id
            if measurement_node.map_identifier:
                self.match_floor = reference_floor_id == tag_floor_id

        if reference_node.area_identifier:
            area_id = reference_node.area_identifier[0]
            self.match_area = False
            if measurement_node.area_identifier:
                self.match_area = area_id in measurement_node.area_identifier

        # Calculates location error
        self.location_error = self.reference_location.distance_meters_to(self.computed_location)

    def __iter__(self):
        yield ADDRESS_FIELD, self.address
        yield LOCATION_ERROR_FIELD, self.location_error
        yield MATCH_FLOOR_FIELD, self.match_floor
        yield MATCH_AREA_FIELD, self.match_area
        yield MAP_IDENTIFIER_FIELD, self.map_identifier
        yield REFERENCE_MAP_IDENTIFIER_FIELD, self.reference_map_identifier
        yield MEASUREMENT_TIMESTAMP_FIELD, self.measurement_timestamp
        yield NAME_FIELD, self.name
        yield REFERENCE_LOCATION_FIELD, self.reference_location.lla()
        yield COMPUTED_LOCATION_FIELD, self.computed_location.lla()

    def to_dict(self):
        """ Transform a ResultComparison into a dict. """
        return dict(self)


class ReportGenerator:
    def __init__(self,
                 folder_path="wpeapt_data",
                 marker_size=10,
                 time_start=None,
                 time_end=None):
        """ Initiate the Report Generator.

        Args:
            folder_path: Default to "wpeapt_data".
                Path of the folder to get the collected data and store the report.
            marker_size: Size of the points in the nodes positions generated image.
            time_start: Default to None.
                        Minimum UTC time of the computed locations present in the report.
                        It must have the ISO8601 format: "yyyy-MM-ddTHH:mm:ssZ"
                        Example of input: "2024-07-10T11:00:00Z"
            time_end: Default to None.
                      Maximum UTC time of the computed locations present in the report.
                      It must have the ISO8601 format: "yyyy-MM-ddTHH:mm:ssZ"
                      Example of input: "2024-07-10T18:00:00Z"
        """
        # Output files
        self.folder_path = folder_path
        logging.info("Using %s folder to generate the reports.", self.folder_path)

        self.floor_plans_images_dir = os.path.join(self.folder_path, "floor_plans_images")
        self.csv_file = os.path.join(self.folder_path, "report", "report.csv")
        self.html_file = os.path.join(self.folder_path, "report", "report.html")
        self.css_file = os.path.join(self.folder_path, "report", "css_style_for_html_report.css")

        # Input files
        computed_locations_file = os.path.join(self.folder_path, "data", "computed_locations.json")
        metadata_file = os.path.join(self.folder_path, "data", "metadata.json")
        references_file = os.path.join(self.folder_path, "data", "reference.json")
        configuration_data_file = os.path.join(self.folder_path, "data", "network_configuration.json")

        # Statistics values
        self.location_errors: List[float] = []
        self.match_floor_success: int = 0
        self.match_area_success: int = 0
        self.match_location_error: int = 0
        self.match_floor_error: int = 0
        self.match_area_error: int = 0

        # Report parameters.
        self.marker_size = marker_size

        # Data time filtering parameters
        self.timestamp_start_ms = None
        self.timestamp_end_ms = None

        try:
            if time_start:
                time_start = parser.parse(time_start)
                self.timestamp_start_ms = datetime.timestamp(time_start) * 1000
            if time_end:
                time_end = parser.parse(time_end)
                self.timestamp_end_ms = datetime.timestamp(time_end) * 1000
        except ParserError:
            logging.exception("Invalid input time format!")
            exit()

        # Data used for the generation of the report
        self.results: pd.DataFrame = pd.DataFrame()
        self.computed_locations: dict = {}
        self.configuration_data: dict = {}
        self.reference_locations: dict = {}
        self.data_metadata: dict = {}
        self.set_data_from_files(references_file=references_file,
                                 computed_locations_file=computed_locations_file,
                                 metadata_file=metadata_file,
                                 configuration_data_file=configuration_data_file)

        # Boolean to determine which parts of the report will be generated.
        self.generate_html_nodes_plot = True
        self.generate_html_location_error_graph = True
        self.generate_html_location_error_histogram = True
        self.generate_html_metrics_table = True

    def set_data_from_files(self, references_file=None, computed_locations_file=None,
                            metadata_file=None, configuration_data_file=None):
        """ Get the data retrieved by the Data Collector module.

        Args:
            references_file (str): File name with the reference node data.
            measurements_file (str): File name with the measurements data.
            metadata_file (str): File name with the data from metadata service.
            configuration_data_file (str): File name with the anchor data
                used for the configuration of the WPE.
        """
        if references_file:
            self.reference_locations = cf.parse_elements_file(references_file)
            assert NODES_FIELD in self.reference_locations, "No references have been found!"
            logging.info("%d reference nodes have been found!", len(self.reference_locations[NODES_FIELD]))

        if computed_locations_file:
            self.computed_locations = cf.parse_elements_file(computed_locations_file)
            assert NODES_FIELD in self.computed_locations, "No computed locations have been found!"
            logging.info("%d computed locations have been found!", len(self.computed_locations[NODES_FIELD]))

            self.computed_locations[NODES_FIELD] = self.filter_node_by_time(self.computed_locations[NODES_FIELD])
            logging.info("%d computed locations are kept after filtering on the timestamp!",
                         len(self.computed_locations[NODES_FIELD]))

            if not len(self.computed_locations[NODES_FIELD]):
                raise ValueError("No computed locations have been found! "
                                 "Check input data and your filters if there are any!")

        if metadata_file:
            self.data_metadata = cf.parse_elements_file(metadata_file)
            assert FLOOR_PLANS_FIELD in self.data_metadata, "No floor plans have been found!"
            logging.info("%d floor plans have been found!", len(self.data_metadata[FLOOR_PLANS_FIELD]))

        if configuration_data_file:
            self.configuration_data = cf.parse_elements_file(configuration_data_file)
            if NODES_FIELD not in self.configuration_data:
                logging.warning("No anchors have been found!")
                self.configuration_data[NODES_FIELD] = []
            else:
                logging.info("%d anchors have been found!", len(self.configuration_data[NODES_FIELD]))

            if AREAS_FIELD not in self.configuration_data:
                logging.warning("No areas have been found!")
                self.configuration_data[AREAS_FIELD] = []
            else:
                logging.info("%d areas have been found!", len(self.configuration_data[AREAS_FIELD]))

    def filter_node_by_time(self, data):
        """ Filter a list of nodes by time. """
        if self.timestamp_start_ms or self.timestamp_end_ms:
            logging.info("Filter data based on time!")
        else:
            return data

        filter_data = []
        for data_item in data:
            if "timestamp" in data_item:
                if self.timestamp_start_ms and int(data_item.timestamp) < self.timestamp_start_ms:
                    continue
                elif self.timestamp_end_ms and int(data_item.timestamp) > self.timestamp_end_ms:
                    continue

            filter_data.append(data_item)

        return filter_data

    def compare_positions(self):
        """ Compare reference positions with the computed ones.
        Must be called after the initiation of the computed locations and references files.
        """
        logging.info("Compare reference positions and computed positions.")
        if not self.computed_locations or not self.reference_locations:
            logging.error("Computed locations and references files must "
                          "be set in set_files before the comparison.")
            return

        result_data_frames = []
        for reference_node in self.reference_locations[NODES_FIELD]:
            measurement_data = cf.search_node(self.computed_locations, reference_node.address)
            if measurement_data:
                result_data_frames.append(
                    pd.DataFrame([dict(ResultComparison(reference_node, measurement))
                                  for measurement in measurement_data])
                )

        assert result_data_frames, "No references data could be linked to tags data"
        self.results = pd.concat(result_data_frames, ignore_index=True)

        # These 2 lines correct numpy automatic conversions boolean to float
        self.results[MATCH_FLOOR_FIELD] = self.results[MATCH_FLOOR_FIELD].map(bool, na_action='ignore')
        self.results[MATCH_AREA_FIELD] = self.results[MATCH_AREA_FIELD].map(bool, na_action='ignore')

    def save_floor_plans_images(self):
        """ Get floor plans images from the metadata file and store them
        as <image_id>.png files.
        """
        logging.info("Saving the floor plan images!")
        if self.floor_plans_images_dir:
            os.makedirs(self.floor_plans_images_dir, exist_ok=True)

        for floor_plan in self.data_metadata[FLOOR_PLANS_FIELD].values():
            data_base64 = floor_plan.image
            file_name = floor_plan.image_id + '.png'
            path_name = os.path.join(self.floor_plans_images_dir, file_name)
            logging.info("Save a floor plan image in the file %s", path_name)
            with open(path_name, "wb") as file:
                file.write(base64.b64decode(data_base64))
                file.close()

    def get_point_pixel(self, data, map_img_int):
        """
        Returns a tuple containing (the axe to draw, the point pixels, the node id).
        Returns None if the data can't be displayed on the image
            (if the data has no address, no map identifier, no associated image,
            or the point would be outside the image of the floor plan).
        """
        nodeid = data.address
        if not nodeid:
            logging.warning("A point to display has no address!")
            return None

        floor_id = data.map_identifier
        if not floor_id:
            logging.warning("A point to display %s has no map identifier!", nodeid)
            return None

        floor = self.data_metadata[FLOOR_PLANS_FIELD].get(floor_id[0], None)
        if not floor:
            logging.warning("A point to display %s has no recognised associated floor %s!", nodeid, floor_id[0])
            return None

        floor_index = map_img_int[floor.id]
        x_data, y_data = floor.wgs84_to_pixel(data.coordinate)

        if not (0 <= x_data <= floor.image_width and 0 <= y_data <= floor.image_height):
            logging.warning("A point to display %s is outside the image of its floor plan %s!", nodeid, floor_id[0])
            return None

        return floor_index, (x_data, y_data), nodeid

    def draw_points(self, data_iterable, axs, map_img_int, check_nodeid=False,
                    add_line=False, *args, **kwargs):
        """ Draws points from a data iterable.

        Args:
            data_iterable: Data iterable. Each of the data dictionaries must contain "coordinates"."lla",
                "map_identifier", "address" in order to be drawn.
            map_img_int: A dicitonary mapping the image id to its matplotlib subplots index.
            check_nodeid (bool): Default to False.
                Boolean asserting if the nodes must be drawn by node id which can lead to more calculs.
            add_line (bool): Default to False. If True, a line is drawn between the points.
            *args, **kwargs: options to be parsed to the image plot method (pyplot.plot or pyplot.scatter).

        Returns: A list of tuples containing (the plot id, the pyplot draw object).
        """
        default_plot_id = None
        plots = {}  # Dictionary mapping plots[floor_index][plot_id] to the list of points to draw.

        # Fill the relevant information to the plots dictionary
        for data in data_iterable:
            point_pixel_info = self.get_point_pixel(data, map_img_int)
            if point_pixel_info is None:
                continue

            floor_index, (x_data, y_data), nodeid = point_pixel_info
            plot_id = nodeid if check_nodeid else default_plot_id

            # Check fields of the plots dictionary
            if floor_index not in plots:
                plots[floor_index] = {}
            if plot_id not in plots[floor_index]:
                plots[floor_index][plot_id] = {"x": [], "y": []}

            plots[floor_index][plot_id]["x"].append(x_data)
            plots[floor_index][plot_id]["y"].append(y_data)

        # Plots the points by groups in the good figures.
        draws = []
        for floor_index, plot_ids in plots.items():
            for plot_id, points in plot_ids.items():
                if add_line:
                    draw, = axs[floor_index].plot(points["x"], points["y"], *args, **kwargs)
                else:
                    draw = axs[floor_index].scatter(points["x"], points["y"], *args, **kwargs)

                draws.append((plot_id, draw))

        return draws

    def generate_floor_images(self):
        """ Generate a picture file for each floor where their nodes and their areas are plotted.
        Areas will have the same colors as they have in the WNT.
        This function generates the same picture as the one stored in the WNT
        to display floor plans, but also plot the nodes with their address.
        The reference positions of nodes are plotted in red and the computation
        by the WPE in blue.
        """
        logging.info("Generate nodes positions on their floor plans drawings.")
        floor_plans = self.data_metadata[FLOOR_PLANS_FIELD]
        nb_img = len(floor_plans)

        map_img_int = dict()
        for index, floor_id in enumerate(floor_plans):
            map_img_int[floor_id] = index

        # Get floor plan images
        images = []
        for floor_id, nb_ax in map_img_int.items():
            # We must get current path as cbook.get_sample_data takes absolute path
            floor_image = os.path.join(os.getcwd(), self.floor_plans_images_dir,
                                       floor_plans[floor_id].image_id + '.png')

            with cbook.get_sample_data(floor_image) as file:
                images.append(mpimg.imread(file, 0))

        fig, axs = plt.subplots(nb_img, squeeze=False)
        axs = axs.flatten()  # Force the axis to be a 1-D np.array
        dpi = fig.get_dpi()
        fig.set_size_inches(min(max([image.shape[1] for image in images]), 1000) / dpi + 1,
                            len(images) * 500 / dpi)
        fig.tight_layout()  # Separate sub plots
        plt.subplots_adjust(right=.8)  # Allow legend to be displayed without truncation.

        # Plot floor plan
        for nb_ax, image in enumerate(images):
            axs[nb_ax].imshow(image)
            axs[nb_ax].set_xticks([])  # Remove x and y ticks from the images
            axs[nb_ax].set_yticks([])  # mpld3 does not support hiding the axis yet.

        # Draw areas on the floor image
        for area in self.configuration_data[AREAS_FIELD].values():
            try:
                floor_id = area.floor_plan_identifier
                floor = self.data_metadata[FLOOR_PLANS_FIELD][floor_id]
                xy = [floor.wgs84_to_pixel(point)[0:2] for point in area.coordinates]
                nb_ax = map_img_int[floor.id]
                axs[nb_ax].add_patch(patches.Polygon(xy=xy, color=area.get_color()))
            except Exception:
                logging.exception("An area can't be display on the floor plan: %s", area.name)

        # Reference all the tags and their references and their links to be drawn.
        results = json.loads(self.results.to_json(orient='records'))
        tags_to_draw = []  # Tags to be plotted as scatter plots
        reference_to_draw = []  # Reference to be plotted as scatter plots in another color
        lines_to_draw = []  # Link between computed locations and their reference when they are in the same floor:

        for result in results:
            node_id = result["address"]
            tag = Node(Coordinate(*result["computed_location"]),
                       address=node_id,
                       map_identifier=[result["map_identifier"]])
            reference = Node(Coordinate(*result["reference_location"]),
                             address=node_id,
                             map_identifier=[result["reference_map_identifier"]])

            if tag not in tags_to_draw:
                tags_to_draw.append(tag)
            if reference not in reference_to_draw:
                reference_to_draw.append(reference)

            if result["match_floor"]:
                lines_to_draw += [reference, tag]

        map_address_plots = {}
        # Draw tags in red and references in blue and a link between these in green node id by node id.
        lines_plot = self.draw_points(lines_to_draw, axs, map_img_int, check_nodeid=True, color='g',
                                      add_line=True, markersize=self.marker_size, label='All', zorder=1)
        tags_plot = self.draw_points(tags_to_draw, axs, map_img_int, check_nodeid=True, color='r',
                                     marker='.', alpha=1, s=self.marker_size**2, label='All', zorder=3)
        references_plot = self.draw_points(reference_to_draw, axs, map_img_int, check_nodeid=True,
                                           color='b', marker='.', s=self.marker_size**2, alpha=1, label='All', zorder=4)

        for plot_id, plot in lines_plot + tags_plot + references_plot:
            if plot_id not in map_address_plots:
                map_address_plots[plot_id] = []
            map_address_plots[plot_id].append(plot)

        # Draw tags in red and references in blue and a link between these in green all at once.
        lines_plot = self.draw_points(lines_to_draw, axs, map_img_int, color='g',
                                      check_nodeid=True, add_line=True,
                                      markersize=self.marker_size, label='All', zorder=1)
        tags_plot = self.draw_points(tags_to_draw, axs, map_img_int, color='r', marker='.',
                                     alpha=1, s=self.marker_size**2, label='All', zorder=3)
        references_plot = self.draw_points(reference_to_draw, axs, map_img_int, color='b',
                                           marker='.', alpha=1, s=self.marker_size**2, label='All', zorder=4)

        lines_plots = [line_plot for _, line_plot in lines_plot]
        tags_plots = [tag_plot for _, tag_plot in tags_plot]
        references_plots = [reference_plot for _, reference_plot in references_plot]
        all_plots = lines_plots + tags_plots + references_plots

        # Draw anchors in orange
        anchor_data = self.configuration_data[NODES_FIELD]
        all_anchors = self.draw_points(anchor_data, axs, map_img_int, color='orange',
                                       marker='.', s=self.marker_size**2, alpha=1, zorder=2)
        all_anchors_plots = [all_anchor_plot for _, all_anchor_plot in all_anchors]

        # Adding title for each floor plan images
        for floor in self.data_metadata[FLOOR_PLANS_FIELD].values():
            nb_ax = map_img_int[floor.id]
            if floor.name:
                axs[nb_ax].set_title("Nodes computation for " + floor.name, fontsize=TITLE_SIZE)

        # Make the legend interactive
        if all_anchors_plots:
            labels = ["Anchors", "all nodes"]
            nodes = [all_anchors_plots, all_plots]
            start_visible = [True, False]
        else:
            labels = ["all tags"]
            nodes = [all_plots]
            start_visible = [False]

        for address, plots in map_address_plots.items():
            labels.append(address)
            nodes.append(plots)

        interactive_legend = plugins.InteractiveLegendPlugin(
            nodes,
            labels,
            alpha_unsel=0,
            alpha_over=0.4,
            start_visible=start_visible + [False] * (len(labels) - len(start_visible))
        )

        plugins.connect(fig, interactive_legend)
        fig_html = mpld3.fig_to_html(fig)
        plt.close()  # Release memory
        return fig_html

    def generate_table_of_contents(self):
        """ Generate table of contents for the html file.

        Return (str): The table of contents of the html file in a string.
        """
        logging.info("Generate table of contents!")
        content_number = 2
        html_contents_table = "<div id=\"toc_container\">\n" \
            "<p class=\"toc_title\">Contents</p>\n" \
            "<ul class=\"toc_list\">\n" \
            "<li><a href=\"#Analysis\">1. Analysis of the network</a></li>\n" \
            "<li><a href=\"#High_level_info\">2. High level informations</a></li>\n"

        if self.generate_html_nodes_plot:
            content_number += 1
            html_contents_table += f"<li><a href=\"#Images\">{content_number}. Plot of the nodes</a></li>\n"

        if self.generate_html_location_error_graph:
            content_number += 1
            html_contents_table += f"<li><a href=\"#Location_Error_Graphs\">{content_number}. Location error graphs</a></li>\n"

        if self.generate_html_location_error_histogram:
            content_number += 1
            html_contents_table += f"<li><a href=\"#Location_Error_Histograms\">{content_number}. Location error histograms</a></li>\n"

        if self.generate_html_metrics_table:
            content_number += 1
            html_contents_table += f"<li><a href=\"#metrics_table\">{content_number}. Table of metrics</a></li>\n"

        html_contents_table += "</ul>\n" \
            "</div>\n\n"

        return html_contents_table

    def generate_high_level_info(self):
        """ Generate html to display high level information for tags and anchors.

        Returns (str): html string of the high level information.
        """
        logging.info("Generate high level info table!")
        tags = self.computed_locations[NODES_FIELD]
        anchors_number = len(self.configuration_data[NODES_FIELD])
        positions_number = len(tags)
        try:
            tags_number = len(self.results.groupby(self.results.address))
        except AttributeError:
            tags_number = 0

        time_period = [timestamp_to_str(min(tag.timestamp for tag in tags)),
                       timestamp_to_str(max(tag.timestamp for tag in tags))]

        # Add overall information
        html_data = "<h2 id=\"High_level_info\">High level information</h2>\n" \
            f"number of anchors retrieved: {anchors_number}<br>\n" \
            f"number of tags analysed: {tags_number}<br>\n" \
            f"number of positions analysed: {positions_number}<br>\n" \
            f"time period selected: {time_period}<br>\n"

        # Add general information per nodes as a table
        html_data += "<table>\n" \
                     "<thead>\n" \
                     "<tr>\n" \
                     "<th>Node address</th>\n" \
                     "<th>Tag name</th>\n" \
                     "<th>Number of locations received</th>\n" \
                     "<th>Time of first location update</th>\n" \
                     "<th>Time of last location update</th>\n" \
                     "<th>Average location update interval in seconds</th>\n" \
                     "<th>Average location accuracy</th>\n" \
                     "<th>Coordinate of the reference location</th>\n" \
                     "</tr>\n" \
                     "</thead>\n" \
                     "<tbody>\n"

        tags_analyzed = []  # List of the tags that are present in the table
        for tag in tags:
            tag_id = tag.address
            if tag_id in tags_analyzed:
                continue

            tags_analyzed.append(tag_id)
            tag_result = self.results[self.results.address == tag_id]
            if not tag_result.address.any():
                logging.warning("A tag is not referenced: %s", tag_id)
                continue

            # Get basic information on the tags
            location_received_number = len(tag_result)

            if tag_result.measurement_timestamp.empty:
                first_time = np.nan
                last_time = np.nan
                total_update_interval = np.nan
                avg_update_interval = 0
            else:
                first_time = min(tag_result.measurement_timestamp)
                last_time = max(tag_result.measurement_timestamp)
                tag_name = tag_result.name.any()
                if not tag_name:
                    tag_name = "/"

                total_update_interval = (parser.parse(last_time) - parser.parse(first_time))
                if total_update_interval != 0:
                    avg_update_interval = round(total_update_interval.total_seconds() / (location_received_number + 1), 2)
                else:
                    avg_update_interval = 0

            avg_location_error = round(tag_result.location_error.mean(), 2)
            if not math.isnan(avg_location_error):
                avg_location_error = str(avg_location_error) + " m"

            reference_location = [round(num, 7) for num in tag_result.reference_location.iloc[0]]

            html_data += "<tr>\n" \
                         f"<td>{tag_id}</td>\n" \
                         f"<td>{tag_name}</td>\n" \
                         f"<td>{location_received_number}</td>\n" \
                         f"<td>{first_time}</td>\n" \
                         f"<td>{last_time}</td>\n" \
                         f"<td>{avg_update_interval}</td>\n" \
                         f"<td>{avg_location_error}</td>\n" \
                         f"<td>{reference_location}</td>\n" \
                         "</tr>\n"

        html_data += "</tbody>\n" \
                     "</table>\n\n"

        return html_data

    def generate_statistics(self):
        """
        Generate statistics attributes for the report generator.
        """
        self.location_errors = self.results[LOCATION_ERROR_FIELD].to_list()
        self.location_error_None = np.isnan(self.location_errors).sum()
        self.location_errors = list(filter(lambda x: not np.isnan(x), self.location_errors))

        self.match_floor_success = self.results[MATCH_FLOOR_FIELD].sum()
        self.match_floor_error = self.results[MATCH_FLOOR_FIELD].isna().sum()

        self.match_area_success = self.results[MATCH_AREA_FIELD].sum()
        self.match_area_error = self.results[MATCH_AREA_FIELD].isna().sum()

    def generate_metrics_table(self):
        """ Generate html to display the metrics of result comparisons.

        Returns (str): html string of the metrics.
        """
        logging.info("Generate metrics table!")
        html_data = "<h2 id=\"metrics_table\">Table of metrics</h2>\n" \
                    "<table>\n" \
                    "<thead>\n" \
                    "<tr>\n" \
                    "<th>Address of the node</th>\n" \
                    "<th>Tag name</th>\n" \
                    "<th>Numbers of locations computed</th>\n" \
                    "<th>Mean of location error in meters</th>\n" \
                    "<th>Median of location error in meters</th>\n" \
                    "<th>Variance of location error</th>\n" \
                    "<th>% floor match success</th>\n" \
                    "<th>% area match success</th>\n" \
                    "<th>% non location computed node</th>\n" \
                    "<th>% non floor computed node</th>\n" \
                    "<th>% non area computed node</th>\n" \
                    "</tr>\n" \
                    "</thead>\n" \
                    "<tbody>\n"

        self.generate_statistics()
        group_nodes = self.results.groupby(self.results.address)

        for data in group_nodes:
            node_number = len(data[1])
            tag_name = data[1].name.any()
            if not tag_name:
                tag_name = "/"

            html_data += "<tr>\n" \
                         f"<td>{data[0]}</td>\n" \
                         f"<td>{tag_name}</td>\n" \
                         f"<td>{node_number}</td>\n" \
                         f"<td>{str(round(data[1].location_error.mean(), 2)) + ' m'}</td>\n" \
                         f"<td>{str(round(data[1].location_error.median(), 2)) + ' m'}</td>\n" \
                         f"<td>{str(round(data[1].location_error.var(), 2)) + ' m2' if len(data[1].location_error)>1 else np.nan}</td>\n" \
                         f"<td>{round(data[1].match_floor.sum() / node_number * 100, 2)} %</td>\n" \
                         f"<td>{round(data[1].match_area.sum() / node_number * 100, 2)} %</td>\n" \
                         f"<td>{round(data[1].location_error.isna().sum() / node_number * 100, 2)} %</td>\n" \
                         f"<td>{round(data[1].match_floor.isna().sum() / node_number * 100, 2)} %</td>\n" \
                         f"<td>{round(data[1].match_area.isna().sum() / node_number * 100, 2)} %</td>\n" \
                         "</tr>\n"

        node_number = len(self.results)
        html_data += "<tr>\n" \
                     f"<td>Total</td>\n" \
                     f"<td>/</td>\n" \
                     f"<td>{node_number}</td>\n" \
                     f"<td>{str(round(statistics.mean(self.location_errors), 2))+' m' if self.location_errors else np.nan}</td>\n" \
                     f"<td>{str(round(statistics.median(self.location_errors), 2))+' m' if self.location_errors else np.nan}</td>\n" \
                     f"<td>/</td>\n" \
                     f"<td>{round(self.match_floor_success / node_number * 100, 2)} %</td>\n" \
                     f"<td>{round(self.match_area_success / node_number * 100, 2)} %</td>\n" \
                     f"<td>{round(self.location_error_None / node_number * 100, 2)} %</td>\n" \
                     f"<td>{round(self.match_floor_error / node_number * 100, 2)} %</td>\n" \
                     f"<td>{round(self.match_area_error / node_number * 100, 2)} %</td>\n" \
                     "</tr>\n" \
                     "</tbody>\n" \
                     "</table>\n\n"

        return html_data

    def generate_img_html(self):
        """ Plot reference nodes in red and measurements nodes in blue for each
        floor plan. Must be called after the initialization of the metadata
        file as it is saving into png the picture of floors from the WNT.

        Return (str): html string to display images
        """
        assert self.data_metadata, "metadata file must be initialized" \
                                   "with set_files methods to display floors"

        self.save_floor_plans_images()

        html_data = "<h2 id=\"Images\">Nodes positions</h2>\n"
        html_data += self.generate_floor_images()

        return html_data

    def generate_location_errors_graphs(self):
        """ Generate an interactive graph to display location errors.
        The graph will display each result according to their location error.
        When the cursor is placed on one of the points, additionnal information
        will be displayed as for example, the address of the node,
        the location error, the floor name of the node, if the areas match
        but also the measurement timestamp to find the node more easily in the data.

        Return (str): html string to display the graphs.
        """
        logging.info("Generate the location errors graphs")

        html_data = "<h2 id=\"Location_Error_Graphs\">Location error graphs</h2>\n"
        node_results = self.results.groupby(self.results.address)

        for result in node_results:
            node_id = result[0]
            tag_results = result[1]
            html_data += self.generate_location_errors_graph(node_id, tag_results)

        return html_data

    def generate_location_errors_graph(self, node_id, tag_results):
        """ Generate an interactive graph to display location errors of a tag.
        The graph will display each result according to their location error.
        When the cursor is placed on one of the point, additionnal information
        will be displayed like for example, the address of the node,
        the location error, the floor name of the node, if the areas match
        but also the measurement timestamp to find the node more easily in the
        data.

        Args:
            node_id (int): Node id of the tag.
            tag_results: Data comparisons results of the tag.

        Return (str): html string to display the graph.
        """
        logging.info("Generate the location errors graph for %s", node_id)

        # creating the graph
        fig, ax = plt.subplots()

        # Sort data by tag id then time ascending
        data_to_display = tag_results.sort_values(by="measurement_timestamp", ascending=True)

        points = ax.plot(data_to_display[LOCATION_ERROR_FIELD].to_list(), 'o', color='g')

        ax.set_title(f"Location error graph for {node_id}")
        ax.set_ylabel('Location error in meters')
        ax.set_xlabel('Individual calculated positions')
        plt.xticks([], [])  # remove x ticks
        ax.grid(axis='y', color='grey', linestyle=':', linewidth=0.1)

        # new graph creator
        tool_tips = []
        for res in data_to_display.iterrows():
            address = res[1].address if 'address' in res[1] else 'nan'
            location_error = round(res[1].location_error, 2) if 'location_error' in res[1] else 'nan'
            try:
                floor = self.data_metadata[FLOOR_PLANS_FIELD][res[1].map_identifier].name if res[1].map_identifier else 'NAN'
            except:
                floor = 'NAN'

            text = "<loc_error_graph_label>" \
                f"address: {address} <br>" \
                f"location_error: {location_error}m <br>" \
                f"floor: {floor} <br>" \
                f"match area:{res[1].match_area}<br>" \
                f"timestamp: {res[1].measurement_timestamp}" \
                "</loc_error_graph_label>"

            tool_tips.append(text)

        white_background = """
        loc_error_graph_label
        {
        background-color: #ffffff;
        }
        """

        tooltip = plugins.PointHTMLTooltip(points[0],
                                           tool_tips,
                                           voffset=0, hoffset=20, css=white_background)

        plugins.connect(fig, tooltip)
        # exporting the graph to html

        fig_html = mpld3.fig_to_html(fig)
        plt.close()  # Release memory
        return fig_html

    def generate_location_errors_histograms(self):
        """ Generate location error histograms.

        Return (str): html string to display the graphs.
        """
        logging.info("Generate the location errors graphs")

        html_data = "<h2 id=\"Location_Error_Histograms\">Location error histograms</h2>\n"
        node_results = self.results.groupby(self.results.address)

        for result in node_results:
            node_id = result[0]
            tag_results = result[1]
            html_data += self.generate_location_errors_histogram(node_id, tag_results)

        return html_data

    def generate_location_errors_histogram(self, node_id, tag_results):
        """ Generate a location error histogram for a tag.

        Args:
            node_id (int): Node id of the tag.
            tag_results: Data comparisons results of the tag.

        Return (str): html string to display the graph.
        """
        logging.info("Generate the location errors histogram for %s", node_id)

        # Creating the graph
        fig, ax = plt.subplots()

        # Prepare parameters for the histogram
        max_value = max(tag_results[LOCATION_ERROR_FIELD].tolist())

        # Minimum of 5 steps and one step per 0.5 meter.
        bins = max(min(math.ceil(max_value * 2), 50), 5)

        # Precision in meter of the max value round up in the histogram.
        precision = min(math.ceil(max_value * 5) / 10, 1) / 2
        max_value_rounded_up = math.ceil(max_value / precision) * precision

        # Round up the max value at a 0.5 precision
        plt.hist(tag_results[LOCATION_ERROR_FIELD].tolist(),
                 bins=bins,
                 range=(0, max_value_rounded_up))

        ax.set_title(f"Location error histogram for {node_id}")
        ax.set_ylabel('Occurrences')
        ax.set_xlabel('Error in meters')

        fig_html = mpld3.fig_to_html(fig)
        plt.close()  # Release memory
        return fig_html

    def insert_wirepas_logo(self):
        """ Return a html link to the wirepas logo. """
        library_path = os.path.dirname(__file__)
        logo_path = os.path.join("images", "wirepas_logo.jpg")
        final_logo_path = os.path.join(self.folder_path, "report", logo_path)

        # Copy logo from the package to the report folder
        os.makedirs(os.path.dirname(final_logo_path), exist_ok=True)
        shutil.copyfile(os.path.join(library_path, logo_path), final_logo_path)

        return f"<img src='{logo_path}' alt='wirepas logo'>"

    def generate_html(self, generate_css=True):
        """ Generate and store a html file that analyses result comparisons between
        computed nodes and their real values.

        Args:
            generate_css (bool): True for generating the css file (default)
                False if the css file has already been generated.
        """
        if generate_css:
            self.generate_css()

        html_data = "<!DOCTYPE html>\n" \
                    "<html>\n" \
                    "<head>\n" \
                    "<title> Wirepas WPE APT report </title>\n" \
                    f"<link rel=\"stylesheet\" href=\"{os.path.basename(self.css_file)}\">\n" \
                    "</head>\n" \
                    "<body>\n\n"

        html_data += self.insert_wirepas_logo()
        html_data += "<h1 id=\"Analysis\">Wirepas WPE APT Report</h1>\n"
        html_data += f"<h3> Version of the tool : {version('wirepas_wpe_apt')} </h3>\n\n"
        html_data += self.generate_table_of_contents()
        html_data += self.generate_high_level_info()

        if self.generate_html_nodes_plot:
            html_data += self.generate_img_html()

        if self.generate_html_location_error_graph:
            html_data += self.generate_location_errors_graphs()

        if self.generate_html_location_error_histogram:
            html_data += self.generate_location_errors_histograms()

        if self.generate_html_metrics_table:
            html_data += self.generate_metrics_table()

        html_data += "</body>\n" \
                     "</html>\n"

        logging.info("Save the html report to %s", self.html_file)
        with open(self.html_file, 'w') as htmlfile:
            htmlfile.write(html_data)

    def generate_css(self):
        """ Generate the css file for the html report. """
        logging.info("Save the css file to %s", self.css_file)

        css_data = "h1, h2 {\n" \
                   "text-decoration:underline;\n" \
                   "color: #121212;\n" \
                   "}\n" \
                   "table {\n" \
                   "border-collapse: collapse;\n" \
                   "margin: 25px 0;\n" \
                   "font-size: 0.9em;\n" \
                   "font-family: sans-serif;\n" \
                   "min-width: 400px;\n" \
                   "box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);\n" \
                   "text-align: center;\n" \
                   "}\n" \
                   "table thead tr {\n" \
                   "background-color: #F04B30;\n" \
                   "color: #ffffff;\n" \
                   "}\n" \
                   "table th, table td {\n" \
                   "padding: 12px 15px;\n" \
                   "}\n" \
                   "table tbody tr {\n" \
                   "color: #42242A;\n" \
                   "border-bottom: 1px solid #ffffff;\n" \
                   "}\n" \
                   "table tbody tr:nth-of-type(even) {\n" \
                   "color: #121212;\n" \
                   "background-color: #FCF3E8;\n" \
                   "}\n" \
                   "table tbody tr:last-of-type {\n" \
                   "border-bottom: 2px solid #F04B30;\n" \
                   "}\n" \
                   "#toc_container {\n" \
                   "width: 300px;\n" \
                   "border: 3px solid #42242A;\n" \
                   "margin: 20px;\n" \
                   "padding: 5px;\n" \
                   "background-color: #FCF3E8;\n" \
                   "}\n" \
                   ".toc_title {\n" \
                   "font-weight: bold;\n" \
                   "text-align: center;\n" \
                   "text-decoration:underline;\n" \
                   "color: #42242A;\n" \
                   "}\n" \
                   "#toc_container.toc_list {\n" \
                   "text-align: center;\n" \
                   "}\n" \
                   "#toc_container li, #toc_container ul, #toc_container ul li {\n" \
                   "color: #42242A;\n" \
                   "}\n" \
                   "#toc_container a:link {color:#0000ff;}\n" \
                   "#toc_container a:visited {color:#0000ff;}\n" \
                   "#toc_container a:hover {color:#F04B30;font-weight: bold;}\n" \
                   "\n"

        with open(self.css_file, 'w') as file:
            file.write(css_data)

    def generate_csv(self):
        """ Generate csv file for database that analyses result comparisons
        between computed nodes and their real values.
        """
        logging.info("Save the csv file to %s", self.csv_file)
        with open(self.csv_file, 'w') as file:
            self.results.to_csv(file, header=True, index=False)

    def generate_report(self, generate_css=True):
        """ Generate the html report of analysis of comparison results
        and store the data that have been used in a csv file.

        Args:
            generate_css (bool): True for generating the css file (default)
                                 False if the css file has already been generated.
        """
        os.makedirs(os.path.dirname(self.html_file), exist_ok=True)
        self.compare_positions()
        self.generate_csv()
        self.generate_html(generate_css)


def str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    # Argument parser
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--folder_path', type=str, default="wpeapt_data",
                        help='Default to "wpeapt_data". '
                        'Path of the folder to get the collected data and store the report.')
    parser.add_argument('--marker_size', type=int, default=10,
                        help='Default to 10. Size of the points in the nodes positions generated image.')
    parser.add_argument('--time_start', type=str, default=None,
                        help='Default to None. '
                        'Minimum UTC time of the computed locations present in the report.\n'
                        'It must have the ISO8601 format: "yyyy-MM-ddTHH:mm:ssZ".\n'
                        'Example of input: --time_start 2024-07-10T11:00:00Z')
    parser.add_argument('--time_end', type=str, default=None,
                        help='Default to None. '
                        'Maximum UTC time of the computed locations present in the report.\n'
                        'It must have the ISO8601 format: "yyyy-MM-ddTHH:mm:ssZ".\n'
                        'Example of input: --time_end 2024-07-10T18:00:00Z')
    parser.add_argument("--log_level", default="info", type=str,
                        choices=["debug", "info", "warning", "error", "critical"],
                        help="Log level to be displayed.")

    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s | [%(levelname)s] %(filename)s:%(lineno)d:%(funcName)s:%(message)s',
        level=args.log_level.upper(),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("report_generator.log", mode="w")
        ]
    )

    # Get the command line arguments
    report = ReportGenerator(
        folder_path=args.folder_path,
        marker_size=args.marker_size,
        time_start=args.time_start,
        time_end=args.time_end
    )

    report.generate_report()


if __name__ == '__main__':
    main()
