# Код для загрузки словаря и выполнения алгоритма
import json
import os
import numpy as np
from PIL import Image
from collections import defaultdict
import random


def load_color_dict():
    with open('color_dict.json', 'r') as f:
        data = json.load(f)
        return {tuple(map(int, k.strip('()').split(','))): v for k, v in data.items()}


def get_average_color(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        pixels = list(img.getdata())
        r = sum(pixel[0] for pixel in pixels) // len(pixels)
        g = sum(pixel[1] for pixel in pixels) // len(pixels)
        b = sum(pixel[2] for pixel in pixels) // len(pixels)
    return (r, g, b)


def find_closest_color(target_color, color_dict):
    min_dist = float('inf')
    closest_color = None
    for color in color_dict.keys():
        dist = sum((a - b) ** 2 for a, b in zip(target_color, color))
        if dist < min_dist:
            min_dist = dist
            closest_color = color
    return closest_color


def mosaic_algorithm(input_image_path, color_dict, allow_repeats=True):
    input_img = Image.open(input_image_path).convert('RGB')
    width, height = input_img.size

    block_w, block_h = 16, 9

    # Вычисляем размеры сетки
    grid_w = width // block_w
    grid_h = height // block_h

    # Обрезаем изображение до нужного размера
    trimmed_width = grid_w * block_w
    trimmed_height = grid_h * block_h
    input_img = input_img.crop((0, 0, trimmed_width, trimmed_height))

    # Создаем матрицу для хранения путей
    path_matrix = [[None for _ in range(grid_w)] for _ in range(grid_h)]

    used_paths = set()

    for i in range(grid_h):
        for j in range(grid_w):
            left = j * block_w
            top = i * block_h
            right = left + block_w
            bottom = top + block_h

            block = input_img.crop((left, top, right, bottom))

            # Считаем средний цвет блока
            pixels = list(block.getdata())
            avg_r = sum(p[0] for p in pixels) // len(pixels)
            avg_g = sum(p[1] for p in pixels) // len(pixels)
            avg_b = sum(p[2] for p in pixels) // len(pixels)
            avg_color = (avg_r, avg_g, avg_b)

            # Находим ближайший цвет в словаре
            closest_color = find_closest_color(avg_color, color_dict)

            # Выбираем путь к изображению
            available_paths = [p for p in color_dict[closest_color]
                               if allow_repeats or p not in used_paths]

            if available_paths:
                chosen_path = random.choice(available_paths)
                if not allow_repeats:
                    used_paths.add(chosen_path)
            else:
                all_paths = []
                for paths_list in color_dict.values():
                    all_paths.extend(paths_list)
                chosen_path = random.choice(all_paths)

            path_matrix[i][j] = chosen_path

    # Создаем финальное изображение
    final_width = grid_w * 320
    final_height = grid_h * 180

    final_img = Image.new('RGB', (final_width, final_height))

    for i in range(grid_h):
        for j in range(grid_w):
            img_path = path_matrix[i][j]
            tile_img = Image.open(img_path).convert('RGB')
            if tile_img.size != (320, 180):
                tile_img = tile_img.resize((320, 180))

            x_pos = j * 320
            y_pos = i * 180
            final_img.paste(tile_img, (x_pos, y_pos))

    return final_img, path_matrix


color_dict = load_color_dict()
result_img, matrix = mosaic_algorithm('input.jpg', color_dict, allow_repeats=True)
result_img.save('mosaic_result2.jpg')