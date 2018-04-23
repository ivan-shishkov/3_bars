import json
import os.path
import argparse
from functools import partial


def load_json_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return json.load(file)


def get_seats_count_in_bar(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_info_about_biggest_bar(list_of_bars):
    return max(list_of_bars, key=get_seats_count_in_bar)


def get_info_about_smallest_bar(list_of_bars):
    return min(list_of_bars, key=get_seats_count_in_bar)


def get_bar_coordinates(bar):
    bar_coordinates = bar['geometry']['coordinates']
    bar_latitude = bar_coordinates[1]
    bar_longitude = bar_coordinates[0]

    return {'latitude': bar_latitude, 'longitude': bar_longitude}


def calculate_distance_to_bar(bar, latitude, longitude):
    bar_coordinates = get_bar_coordinates(bar)
    bar_latitude = bar_coordinates['latitude']
    bar_longitude = bar_coordinates['longitude']

    return ((bar_latitude - latitude) ** 2 + (
            bar_longitude - longitude) ** 2) ** 0.5


def get_info_about_nearest_bar(list_of_bars, latitude, longitude):
    return min(
        list_of_bars,
        key=partial(
            calculate_distance_to_bar,
            latitude=latitude,
            longitude=longitude,
        ),
    )


def print_info_about_bar(bar, feature):
    print()
    print('{:-^30}'.format(feature))

    bar_info = bar['properties']['Attributes']
    print('Название: {}'.format(bar_info['Name']))
    print('Количество мест: {}'.format(bar_info['SeatsCount']))
    print('Административный округ: {}'.format(bar_info['AdmArea']))
    print('Район: {}'.format(bar_info['District']))
    print('Адрес: {}'.format(bar_info['Address']))
    print('Телефон: {}'.format(bar_info['PublicPhone'][0]['PublicPhone']))

    bar_coordinates = get_bar_coordinates(bar)
    bar_latitude = bar_coordinates['latitude']
    bar_longitude = bar_coordinates['longitude']
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

    arguments_from_command_line = parser.parse_args()

    return {
        'filename': arguments_from_command_line.filename,
        'latitude': arguments_from_command_line.latitude,
        'longitude': arguments_from_command_line.longitude,
    }


def main():
    arguments_from_command_line = parse_command_line_arguments()

    filename = arguments_from_command_line['filename']
    latitude = arguments_from_command_line['latitude']
    longitude = arguments_from_command_line['longitude']

    try:
        file_content = load_json_data(filename)
    except (UnicodeDecodeError, json.JSONDecodeError):
        print('Неверный формат файла json')
        return

    if not file_content:
        print('Не найден файл с исходными данными')
        return

    list_of_bars = file_content['features']

    print_info_about_bar(
        bar=get_info_about_biggest_bar(list_of_bars),
        feature='Самый большой бар:',
    )

    print_info_about_bar(
        bar=get_info_about_smallest_bar(list_of_bars),
        feature='Самый маленький бар:',
    )

    print_info_about_bar(
        bar=get_info_about_nearest_bar(list_of_bars, latitude, longitude),
        feature='Самый ближайший бар:',
    )


if __name__ == '__main__':
    main()
