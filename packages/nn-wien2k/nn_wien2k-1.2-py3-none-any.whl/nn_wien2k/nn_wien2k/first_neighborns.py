# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:47:16 2024.

@author: gp
"""
import re
from collections import defaultdict

# Регулярные выражения для поиска блоков атомов, параметров и расстояний
RE_BLOCKS = r'ATOM:\s*\d+\s+EQUIV.\s+\d+\s+\w+.*?(?=\n\s*ATOM:\s*\d+\s+EQUIV.|\Z)'
RE_PARAMS = r'ATOM:\s+\d+\s+EQUIV.\s+\d+\s+(\w+)'
RE_DIST = r'ATOM:\s+\d+\s+(\w+)\s+AT.*?IS\s+[\d.]+\s+A\.U\.\s+([\d.]+)\s+ANG'


def remove_numbers(string: str):
    """
    Удаляет цифры из строки.

    Parameters
    ----------
    string : str
        Строка с цифрами.

    Returns
    -------
    str
        Строка без цифр.

    """
    return re.sub(r'\d+', '', string)


def parse_file(filename: str, distance: float = 3.0):
    """
    Парсим файл case.outputnn.

    Parameters
    ----------
    filename : str
        Название файла.
    distance : float, optional
        Отсечка расстояний до ближайших соседей. The default is 3.0.

    Returns
    -------
    results : collections.defaultdict
        Словарь с ближайшими соседями.

    """
    with open(filename, 'r') as file:
        content = file.read()

    # Находим все блоки атомов
    atom_blocks = re.findall(RE_BLOCKS, content, re.DOTALL)

    # Инициализируем словарь для хранения результатов
    results = defaultdict(lambda: {"count": 0, "environment": None})

    for block in atom_blocks:
        lines = block.split('\n')
        atom_info = re.match(RE_PARAMS, lines[0])
        if atom_info:
            atom_type = remove_numbers(atom_info.group(1))
        else:
            continue  # Пропускаем блок, если не удалось определить тип атома

        # Словарь для хранения расстояний до соседей
        distances = defaultdict(lambda: defaultdict(int))

        for line in lines[1:]:
            match = re.search(RE_DIST, line)
            if match:
                neighbor_type, dist = match.groups()
                dist = float(dist)
                # Обрабатываем соседей в зависимости от расстояния
                if dist <= distance:
                    distances[remove_numbers(neighbor_type)][dist] += 1
                else:
                    if remove_numbers(neighbor_type) not in distances:
                        distances[remove_numbers(neighbor_type)][dist] += 1
                    else:
                        if dist in distances[remove_numbers(neighbor_type)]:
                            distances[remove_numbers(neighbor_type)][dist] += 1

        # Преобразуем distances в кортеж для использования в качестве ключа
        environment = tuple(
            sorted((k, tuple(sorted(v.items()))) for k, v in distances.items())
            )

        # Группируем атомы с одинаковым окружением
        key = (atom_type, environment)
        results[key]["count"] += 1
        results[key]["environment"] = environment

    return results


def print_results(results: defaultdict):
    """
    Функция выводит результаты.

    Parameters
    ----------
    results : collections.defaultdict
        Результаты от функции parse_file.

    Returns
    -------
    None.

    """
    for (atom_type, _), data in sorted(results.items()):
        print(f"{atom_type} (количество: {data['count']}):")
        for neighbor_type, distances in data['environment']:
            print(f"  {neighbor_type}:")
            for distance, count in distances:
                print(f"    {distance:.5f} ANG: {count}")
        print()

