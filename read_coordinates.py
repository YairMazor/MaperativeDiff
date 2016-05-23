__author__ = 'yair-wind'
import xml.etree.ElementTree
import urllib
import math
from collections import namedtuple
import overpass
import sqlite3

Coordinate = namedtuple('Coordinate', ['lat', 'lon'])


def read_coordinates_from_file(filename):
    coordinates = []
    e = xml.etree.ElementTree.parse(filename).getroot()
    for node in e.findall(".//node"):
        lon = float(node.get('lon'))
        lat = float(node.get('lat'))
        coordinates.append(Coordinate(lat, lon))
    return coordinates


def get_remote_files(url, local_filename):
    urllib.urlretrieve(url, local_filename)


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile


def num2deg(xtile, ytile, zoom):
    """
    Tile numbers to lon./lat.
    """
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def get_tile_numbers_from_coordinates(coordinates, zoom):
    tile_numbers = []
    for coordinate in coordinates:
        tile_numbers.append(deg2num(coordinate.lat, coordinate.lon, zoom))
    return tile_numbers


def get_center_tile_coordinates(tile_numbers, zoom):
    coordinates = []
    for tile in tile_numbers:
        coordinates.append(num2deg(tile[0] + 0.5, tile[1] + 0.5, zoom))
    return coordinates


def get_way_nodes(way_id):
    api = overpass.API()
    way_query = overpass.WayQuery('[id="5066205"]')
    response = api.Get(way_query)
    print response


def main():
    filename = '/Users/yair-wind/Downloads/136.osc'
    coordinates = read_coordinates_from_file(filename)
    tile_numbers = set(get_tile_numbers_from_coordinates(coordinates, 15))
    center_coordinates = get_center_tile_coordinates(tile_numbers, 15)
    print (coordinates[:10])
    print len(tile_numbers)
    print center_coordinates[:10]
    # get_way_nodes(1)
    # get_remote_files(url="http://download.geofabrik.de/asia/israel-and-palestine-updates/000/001/063.osc.gz",
    #                  local_filename="063.osc.gz")
    with open(filename, 'r') as f:
        for line in f:
            print line


if __name__ == '__main__':
    main()