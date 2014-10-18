import exifread
import contextlib
import pprint
import sys
import os
import re


def get_tags(path='~/Pictures/plane.jpg'):
    full_path = os.path.expanduser(path)
    with contextlib.closing(open(full_path, 'rb')) as f:
        tags = exifread.process_file(f)
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


def get_gps_coordinates(tags):
    gps_lat_dms = tags['GPS GPSLatitude']
    degrees, minutes, seconds = parse_gps_coordinate(gps_lat_dms)
    gps_lat_dd = dms_to_dd(degrees, minutes, seconds)

    gps_long_dms = tags['GPS GPSLongitude']
    degrees, minutes, seconds = parse_gps_coordinate(gps_long_dms)
    gps_long_dd = dms_to_dd(degrees, minutes, seconds)

    altitude = 0
    match = re.search(r'(\d+)/(\d+)', str(tags['GPS GPSAltitude']))
    if match:
        altitude = int(match.group(1)) / (int(match.group(2)) * 1.0)

    return gps_lat_dd, gps_long_dd, altitude


def get_location(path):
    tags = get_tags(path)
    gps_lat, gps_long, altitude = get_gps_coordinates(tags)
    
    return { 'photo': path, \
             'latitude': gps_lat, \
             'longitude': gps_long, \
             'altitude': altitude
    }


if __name__ == '__main__':
    print get_location(sys.argv[1])
#    tags = get_tags(sys.argv[1])
#    get_gps_coordinates(tags)
#    pprint.pprint(hide_key(tags, 'JPEGThumbnail'))

