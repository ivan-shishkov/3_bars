import json
import os.path
import argparse
from functools import partial
import sys


def load_json_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return json.load(file)


def get_seats_count_in_bar(bar_info):
    return bar_info['properties']['Attributes']['SeatsCount']


def get_biggest_bar_info(bars_info):
    return max(bars_info, key=get_seats_count_in_bar)


def get_smallest_bar_info(bars_info):
    return min(bars_info, key=get_seats_count_in_bar)


def calculate_distance_to_bar(bar_info, latitude, longitude):
    bar_longitude, bar_latitude = bar_info['geometry']['coordinates']

    return ((bar_latitude - latitude) ** 2 + (
            bar_longitude - longitude) ** 2) ** 0.5


def get_nearest_bar_info(bars_info, user_latitude, user_longitude):
    return min(
        bars_info,
        key=partial(
            calculate_distance_to_bar,
            latitude=user_latitude,
            longitude=user_longitude,
        ),
    )


def print_bar_info(bar_info, feature):
    print()
    print('{:-^30}'.format(feature))

    bar_info_attributes = bar_info['properties']['Attributes']
    print('Название: {}'.format(bar_info_attributes['Name']))
    print('Количество мест: {}'.format(bar_info_attributes['SeatsCount']))
    print('Административный округ: {}'.format(bar_info_attributes['AdmArea']))
    print('Район: {}'.format(bar_info_attributes['District']))
    print('Адрес: {}'.format(bar_info_attributes['Address']))
    print('Телефон: {}'.format(
        bar_info_attributes['PublicPhone'][0]['PublicPhone'],
    ))

    bar_longitude, bar_latitude = bar_info['geometry']['coordinates']
    print('Координаты: {:.6f} с.ш.  {:.6f} в.д.'.format(
        bar_latitude,
        bar_longitude,
    ))


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',
        help='json файл, загруженный с https://apidata.mos.ru, '
             'с данными о барах',
        type=str,
    )
    parser.add_argument(
        'latitude',
        help='Широта вашего местоположения в градусах, например 55.443322',
        type=float,
    )
    parser.add_argument(
        'longitude',
        help='Долгота вашего местоположения в градусах, например 37.223344',
        type=float,
    )

    command_line_arguments = parser.parse_args()

    return command_line_arguments


def main():
    command_line_arguments = parse_command_line_arguments()

    filename = command_line_arguments.filename
    user_latitude = command_line_arguments.latitude
    user_longitude = command_line_arguments.longitude

    try:
        bars_data = load_json_data(filename)
    except (UnicodeDecodeError, json.JSONDecodeError):
        sys.exit('Неверный формат файла json')

    if not bars_data:
        sys.exit('Не найден файл с исходными данными')

    bars_info = bars_data['features']

    print_bar_info(
        bar_info=get_biggest_bar_info(bars_info),
        feature='Самый большой бар:',
    )

    print_bar_info(
        bar_info=get_smallest_bar_info(bars_info),
        feature='Самый маленький бар:',
    )

    print_bar_info(
        bar_info=get_nearest_bar_info(
            bars_info,
            user_latitude,
            user_longitude,
        ),
        feature='Самый ближайший бар:',
    )


if __name__ == '__main__':
    main()
