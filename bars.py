import json
import os
import argparse


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


def get_bar_coordinates(bar):
    bar_coordinates = bar['geometry']['coordinates']
    bar_latitude = bar_coordinates[1]
    bar_longitude = bar_coordinates[0]

    return {'latitude': bar_latitude, 'longitude': bar_longitude}


def create_calculator_of_distance_to_bar(latitude, longitude):
    def calculate(bar):
        bar_coordinates = get_bar_coordinates(bar)
        bar_latitude = bar_coordinates['latitude']
        bar_longitude = bar_coordinates['longitude']

        return ((bar_latitude - latitude) ** 2 + (
                bar_longitude - longitude) ** 2) ** 0.5

    return calculate


def get_nearest_bar(list_bars, latitude, longitude):
    get_distance_to_bar = create_calculator_of_distance_to_bar(latitude,
                                                               longitude)

    return min(list_bars, key=get_distance_to_bar)


def print_bar_info(bar, feature):
    print('\n' + '-' * 20)

    print('Самый ' + feature + ' бар:')
    print('-' * 20)

    bar_info = bar['properties']['Attributes']
    print('Название: ', bar_info['Name'])
    print('Количество мест: ', bar_info['SeatsCount'])
    print('Административный округ: ', bar_info['AdmArea'])
    print('Район: ', bar_info['District'])
    print('Адрес: ', bar_info['Address'])
    print('Телефон: ', bar_info['PublicPhone'][0]['PublicPhone'])

    bar_coordinates = get_bar_coordinates(bar)
    bar_latitude = bar_coordinates['latitude']
    bar_longitude = bar_coordinates['longitude']
    print('Координаты: {} с.ш.  {} в.д.'.format(bar_latitude, bar_longitude))


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='json file downloaded from http://data.mos.ru with data about bars',
                        type=str)
    parser.add_argument('latitude',
                        help='latitude of your location in degrees, e.g. 55.35721',
                        type=float)
    parser.add_argument('longitude',
                        help='longitude of your location in degrees, e.g. 37.42145',
                        type=float)
    args = parser.parse_args()
    return {'filename': args.filename, 'latitude': args.latitude,
            'longitude': args.longitude}


def run_script():
    arguments_from_command_line = parse_command_line_arguments()

    filename = arguments_from_command_line['filename']
    latitude = arguments_from_command_line['latitude']
    longitude = arguments_from_command_line['longitude']

    file_content = load_json_data(filename)

    if not file_content:
        print('Не найден файл с исходными данными')
        return

    list_bars = file_content['features']

    print_bar_info(bar=get_biggest_bar(list_bars), feature='большой')
    print_bar_info(bar=get_smallest_bar(list_bars), feature='маленький')
    print_bar_info(bar=get_nearest_bar(list_bars, latitude, longitude),
                   feature='ближайший')


if __name__ == '__main__':
    run_script()
