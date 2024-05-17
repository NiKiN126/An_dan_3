#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import datetime
import jsonschema
from argparse import ArgumentParser


"""Для своего варианта лабораторной работы 2.16 необходимо дополнительно реализовать
 интерфейс командной строки (CLI)."""


def select(line, humans):
    # Функция выбора человека по дате рождения
    nom = input('Введите дату рождения (YYYY-MM-DD): ')
    count = 0
    print(line)
    print(
        '| {"№":^4} | {"Ф.И.О.":^20} | {"знак зодиака":^15} | {"Дата рождения":^16} |')
    print(line)

    for i, num in enumerate(humans, 1):
        if nom == num.get('daytime', ''):
            count += 1
            print(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('name', ''),
                    num.get('zodiac', ''),
                    num.get('daytime', 0)))
    print(line)

    if count == 0:
        print('Таких людей нет')


def table(line, humans):
    # Функция вывода списка людей
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Ф.И.О.",
            "Знак зодиака",
            "Дата рождения"))
    print(line)
    for i, num in enumerate(humans, 1):
        print(
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('name', ''),
                num.get('zodiac', ''),
                num.get('daytime', 0)
            )
        )
    print(line)


def add(humans):
    # Функция добавления новых людей
    daytime = input('Введите дату рождения (YYYY-MM-DD): ')
    zodiac = input('Введите знак зодиака: ')
    name = input('Введите Ф.И.О.: ')
    date = datetime.datetime.strptime(daytime, '%Y-%m-%d').date()
    air = {
        'zodiac': zodiac,
        'name': name,
        'daytime': daytime
    }

    humans.append(air)
    if len(humans) > 1:
        humans.sort(key=lambda x: x.get('daytime', ''))


def save_to_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def load_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            validate_data(data)
            return data
    except FileNotFoundError:
        return []


def validate_data(data):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "zodiac": {"type": "string"},
                "daytime": {"type": "string", "format": "date"}
            },
            "required": ["name", "zodiac", "daytime"]
        }
    }

    jsonschema.validate(data, schema)


def parse_command_line():
    parser = ArgumentParser(description='Список людей и команды')
    subparsers = parser.add_subparsers(title='команда')

    # Команда 'select'
    select_parser = subparsers.add_parser('select', help='Выбрать человека по дате рождения')
    select_parser.set_defaults(func=select)

    # Команда 'add'
    add_parser = subparsers.add_parser('add', help='Добавить человека')
    add_parser.set_defaults(func=add)

    # Команда 'list'
    list_parser = subparsers.add_parser('list', help='Показать список людей')
    list_parser.set_defaults(func=table)

    # Команда 'exit'
    exit_parser = subparsers.add_parser('exit', help='Завершить работу')
    exit_parser.set_defaults(func=save_to_json)

    args = parser.parse_args()
    return args.func


def main():
    # Загрузка данных из файла
    humans = load_from_json('humans.json')

    while True:
        print('Список команд: \n')
        print('1. Выбрать человека')
        print('2. Добавить человека')
        print('3. Показать список людей')
        print('4. Выход')
        choice = int(input('Введите номер команды: '))

        if choice == 1:
            parse_command_line()(humans)
        elif choice == 2:
            add(humans)
        elif choice == 3:
            table('', humans)
        elif choice == 4:
            save_to_json('humans.json', humans)
            break
        else:
            print('Неправильный выбор команды. Попробуйте еще.', file=sys.stderr)


if __name__ == '__main__':
    main()
