import json
from PIL import Image


def load_color_dict():
    with open('color_dict.json', 'r') as f:
        data = json.load(f)
        return {tuple(map(int, k.strip('()').split(','))): v for k, v in data.items()}


def find_closest_color(target_color, color_dict):
    min_dist = float('inf')
    closest_color = None
    for color in color_dict.keys():
        dist = sum((a - b) ** 2 for a, b in zip(target_color, color))
        if dist < min_dist:
            min_dist = dist
            closest_color = color
    return closest_color


def create_pixel_art(input_image_path, color_dict):
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

    # Создаем матрицу ближайших цветов
    color_matrix = [[None for _ in range(grid_w)] for _ in range(grid_h)]

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
            color_matrix[i][j] = closest_color

    final_width = grid_w * block_w
    final_height = grid_h * block_h

    final_img = Image.new('RGB', (final_width, final_height))

    for i in range(grid_h):
        for j in range(grid_w):
            color = color_matrix[i][j]
            for x in range(block_w):
                for y in range(block_h):
                    final_img.putpixel((j * block_w + x, i * block_h + y), color)

    return final_img, color_matrix


color_dict = load_color_dict()
pixel_art_img, color_matrix = create_pixel_art('input.jpg', color_dict)
pixel_art_img.save('pixel_art_result.jpg')