import exifread
import contextlib
import pprint
import sys
import os
import re


def get_tags(photo_fd):
    tags = exifread.process_file(photo_fd)
    return tags


def get_thumbnail(path):
    tags = get_tags(path)
    thumbnail = tags['JPEGThumbnail']
    return thumbnail


def save_thumnail(source, destination):
    thumbnail = get_thumbnail(source)
    with open('destination', 'wb') as writer:
        writer.write(thumbnail)


def hide_key(tags, key):
    return dict(tags.items() + [(key, '')])


def dms_to_dd(degrees, minutes, seconds):
    return degrees + minutes / 60.0 + seconds / 3600.0


def parse_gps_coordinate(coordinate):
    match = re.search(r'\[(\d+), (\d+), (\d+)/(\d+)\]', str(coordinate))
    if match:
        degrees = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3)) / (int(match.group(4)) * 1.0)
        return degrees, minutes, seconds

    return None, None, None


def get_gps_coordinates(tags):
    gps_lat_dms = tags.get('GPS GPSLatitude')
    gps_lat_dd = None
    if gps_lat_dms is not None:
        degrees, minutes, seconds = parse_gps_coordinate(gps_lat_dms)
        if degrees is not None and minutes is not None and seconds is not None:
            gps_lat_dd = dms_to_dd(degrees, minutes, seconds)

    gps_long_dms = tags.get('GPS GPSLongitude')
    gps_long_dd = None
    if gps_long_dms is not None:
        degrees, minutes, seconds = parse_gps_coordinate(gps_long_dms)
        if degrees is not None and minutes is not None and seconds is not None:
            gps_long_dd = dms_to_dd(degrees, minutes, seconds)

    gps_alt_tag = tags.get('GPS GPSAltitude')
    gps_alt = None
    if gps_alt_tag is not None:
        match = re.search(r'(\d+)/(\d+)', str(gps_alt_tag))
        if match:
            gps_alt = int(match.group(1)) / (int(match.group(2)) * 1.0)

    return gps_lat_dd, gps_long_dd, gps_alt


def get_location(photo_fd):
    tags = get_tags(photo_fd)
    gps_lat, gps_long, gps_alt = get_gps_coordinates(tags)

    location_dict = {}
    if gps_lat is not None and gps_long is not None and gps_alt is not None:
        location_dict['latitude'] = gps_lat
        location_dict['longitude'] = gps_long
        location_dict['altitude'] = gps_alt

    return location_dict


if __name__ == '__main__':
    print get_location(sys.argv[1])
