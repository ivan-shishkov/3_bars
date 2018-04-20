import json
import os


def load_json_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return json.load(file)


def get_seats_count_in_bar(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_biggest_bar(list_bars):
    return max(list_bars, key=get_seats_count_in_bar)


def get_smallest_bar(list_bars):
    return min(list_bars, key=get_seats_count_in_bar)


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    pass
