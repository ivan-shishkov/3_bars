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


def calculate_distance_to_bar(longitude, latitude):
    def calculate(bar):
        bar_coordinates = bar['geometry']['coordinates']
        bar_longitude = bar_coordinates[0]
        bar_latitude = bar_coordinates[1]

        return ((bar_longitude - longitude) ** 2 + (
                    bar_latitude - latitude) ** 2) ** 0.5

    return calculate


def get_nearest_bar(list_bars, longitude, latitude):
    get_distance_to_bar = calculate_distance_to_bar(longitude, latitude)

    return min(list_bars, key=get_distance_to_bar)


if __name__ == '__main__':
    pass
