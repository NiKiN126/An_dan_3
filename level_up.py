#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import click

"""Самостоятельно изучите работу с пакетом click для построения интерфейса командной строки
(CLI). Для своего варианта лабораторной работы 2.16 необходимо реализовать интерфейс
командной строки с использованием пакета click ."""


@click.group()
def cli():
    pass


@cli.command()
@click.option('--file', default='humans.json', help='Файл для сохранения данных')
def select(file):
    # Функция выбора человека по дате рождения
    nom = click.prompt('Введите дату рождения (YYYY-MM-DD)', type=str)
    count = 0
    line = '-' * 64

    with open(file, 'r', encoding='utf-8') as f:
        humans = json.load(f)

    click.echo(line)
    click.echo('| {"№":^4} | {"Ф.И.О.":^20} | {"знак зодиака":^15} | {"Дата рождения":^16} |')
    click.echo(line)

    for i, num in enumerate(humans, 1):
        if nom == num.get('daytime', ''):
            count += 1
            click.echo(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('name', ''),
                    num.get('zodiac', ''),
                    num.get('daytime', 0)))
    click.echo(line)

    if count == 0:
        click.echo('Таких людей нет')


@cli.command()
@click.option('--file', default='humans.json', help='Файл для сохранения данных')
def table(file):
    # Функция вывода списка людей
    line = '-' * 64

    with open(file, 'r', encoding='utf-8') as f:
        humans = json.load(f)

    click.echo(line)
    click.echo('| {:^4} | {:^20} | {:^15} | {:^16} |'.format("№", "Ф.И.О.", "Знак зодиака", "Дата рождения"))
    click.echo(line)
    for i, num in enumerate(humans, 1):
        click.echo(
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('name', ''),
                num.get('zodiac', ''),
                num.get('daytime', 0)
            )
        )
    click.echo(line)


@cli.command()
@click.option('--file', default='humans.json', help='Файл для сохранения данных')
def add(file):
    # Функция добавления новых людей
    daytime = click.prompt('Введите дату рождения (YYYY-MM-DD)', type=str)
    zodiac = click.prompt('Введите знак зодиака', type=str)
    name = click.prompt('Введите Ф.И.О.', type=str)
    date = datetime.datetime.strptime(daytime, '%Y-%m-%d').date()
    air = {
        'zodiac': zodiac,
        'name': name,
        'daytime': daytime
    }

    with open(file, 'r', encoding='utf-8') as f:
        humans = json.load(f)

    humans.append(air)
    if len(humans) > 1:
        humans.sort(key=lambda x: x.get('daytime', ''))

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(humans, f, ensure_ascii=False)


if __name__ == '__main__':
    cli()