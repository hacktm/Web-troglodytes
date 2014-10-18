import exifread
import contextlib
import pprint
import sys
import os


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


def hide_key(dict_, key):
    return dict(tags.items() + [(key, '')])


if __name__ == '__main__':
    tags = get_tags(sys.argv[1])
    pprint.pprint(hide_key(tags, 'JPEGThumbnail'))
