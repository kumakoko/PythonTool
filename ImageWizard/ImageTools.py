from typing import Any
from PIL import Image
from pathlib import Path
import argparse
import ast
import os


# 获取文件路径的后缀名，带点好，例如 .txt
def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension


# 获取文件路径的后缀名，不带点号，例如 .txt
def get_file_extension_without_point(file_path):
    _, extension = os.path.splitext(file_path)
    return extension[1:]  # 去掉点号并转换为大写


# 将指定的图片，转换位24位RGB格式的图
def convert_to_rgb(file_path):
    # 打开图片文件并转换为RGB格式（24位）
    with Image.open(file_path) as img:
        rgb_img = img.convert("RGB")
        print("已将图像转换为24位RGB格式")
        return rgb_img


def get_rgba_img(img_file_path):
    with Image.open(img_file_path) as img:
        img.load()
        # 检查图像模式并输出位深度信息
        if img.mode == 'P':
            rgb_img = img.convert("RGB")
            rgba_img = rgb_img.convert("RGBA")
            print("该图像是PAL8格式（8位调色板格式）。")
            return rgba_img
        elif img.mode == 'RGB':
            rgb_img = img
            rgba_img = rgb_img.convert("RGBA")
            print("该图像是24位格式（RGB，每通道8位）。")
            return rgba_img
        elif img.mode == 'RGBA':
            rgba_img = img
            print("该图像是32位格式（RGB+Alpha，每通道8位）。")
            return rgba_img
        elif img.mode == 'I;16' or img.mode == 'I;16B':
            print("该图像是16位格式（单通道，每像素16位）。")
            rgb_img = img.convert("RGB")
            rgba_img = rgb_img.convert("RGBA")
            return rgba_img
        else:
            print(f"图像格式未知或不支持的模式: {img.mode}")
            return None


# img_file_path 图片文件的路径名
# scale 新图片的放大倍数
def resize_image(img_file_path, scale):
    img = Image.open(img_file_path)
    if scale != 1:
        nw = int(img.width * scale)
        nh = int(img.height * scale)
        img = img.resize((nw, nh), Image.NEAREST)
    return img


# 将指定的图片，转换为32位RGBA格式的图，当像素为指定的透明色transparent_color时，该像素点设置为true
# img_file_path 图片文件的路径名
# transparent_color 作为透明色的颜色三元组
# scale 新图片的放大倍数，默认为1
def convert_to_rgba_with_transparency(img_file_path, transparent_color=(255, 255, 255), scale=1):
    with Image.open(img_file_path) as img:
        # 检查图像模式并输出位深度信息
        if img.mode == 'P':
            rgb_img = img.convert("RGB")
            rgba_img = rgb_img.convert("RGBA")
            print("该图像是PAL8格式（8位调色板格式）。")
        elif img.mode == 'RGB':
            rgb_img = img
            rgba_img = rgb_img.convert("RGBA")
            print("该图像是24位格式（RGB，每通道8位）。")
        elif img.mode == 'RGBA':
            rgba_img = img
            print("该图像是32位格式（RGB+Alpha，每通道8位）。")
        elif img.mode == 'I;16' or img.mode == 'I;16B':
            print("该图像是16位格式（单通道，每像素16位）。")
            rgb_img = img.convert("RGB")
            rgba_img = rgb_img.convert("RGBA")
        else:
            print(f"图像格式未知或不支持的模式: {img.mode}")
            return None

    pixels = rgba_img.load()  # 加载像素数据以便逐个修改

    # 遍历图像像素并设置透明度
    for y in range(rgba_img.height):
        for x in range(rgba_img.width):
            r, g, b, _ = pixels[x, y]
            if (r, g, b) == transparent_color:
                pixels[x, y] = (r, g, b, 0)  # 将指定颜色的Alpha设为0
            else:
                pixels[x, y] = (r, g, b, 255)  # 其他颜色的Alpha设为255

    if scale != 1:
        nw = int(rgba_img.width * scale)
        nh = int(rgba_img.height * scale)
        rgba_img = rgba_img.resize((nw, nh), Image.NEAREST)

    print(f"已将图像转换为32位RGBA格式，并将颜色{transparent_color}设置为透明")
    return rgba_img


def name_to_color(name):
    lower_name = name.lower()
    if lower_name in ("r", "red"):
        return 255, 0, 0
    elif lower_name in ("g", "green"):
        return 0, 255, 0
    elif lower_name in ("b", "blue"):
        return 0, 0, 255
    elif lower_name in ("m", "magenta"):
        return 255, 0, 255
    elif lower_name in ("w", "white"):
        return 255, 255, 255
    elif lower_name in ("bk", "black"):
        return 0, 0, 0
    else:
        return None


def str_to_tuple(s):
    try:
        # 尝试将字符串转换为元组
        result = ast.literal_eval(s)
        if isinstance(result, tuple):
            return result
        else:
            # print("转换成功，但结果不是元组类型")
            return None
    except (ValueError, SyntaxError):
        # 捕获转换失败的异常并返回 None
        # print("转换失败，返回 None")
        return None


def parse_color_argument(arg_color):
    v = str_to_tuple(arg_color)
    if v is None:
        return name_to_color(arg_color)
    else:
        return v


# directory 要获取文件的目录
# extensions 文件类型列表
def get_files_with_extensions(directory, extensions):
    matched_files = []
    # 遍历目录下的所有文件
    for root, _, files in os.walk(directory):
        for file in files:
            # 检查文件后缀名是否在指定的后缀名列表中
            if any(file.lower().endswith(ext) for ext in extensions):
                # 添加完整路径到列表中
                matched_files.append(os.path.join(root, file))
    return matched_files


# filepath，带有完整路径的文件名
def get_filename_without_extension(filepath):
    # 获取不带路径的文件名
    filename_with_extension = os.path.basename(filepath)
    # 去除扩展名
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    return filename_without_extension


# 指定目录批量转换
# input_dir         输入目录
# output_dir        输出目录。不带正斜杠或者反斜杠目录分隔符
# out_format        输出格式
# transparent_color 透明色
# scale             图片放大系数，默认为1
def batch_convert(input_dir, out_dir, out_format, transparent_color, scale=1):
    try:
        extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]  # 指定后缀名列表
        result = get_files_with_extensions(input_dir, extensions)
        for one_file in result:
            base_file_name = get_filename_without_extension(one_file)
            rgba_img = convert_to_rgba_with_transparency(one_file, transparent_color, scale)
            rgba_img.save(f"{out_dir}/{base_file_name}.{out_format}", format=out_format.upper())
    except Exception as e:
        print(f"转换失败，发生错误：{e}")


# input_file            输入文件的完整路径名
# output_file           输出文件的完整路径名
# transparent_color     透明色
# scale             图片放大系数，默认为1
def convert_single_file(input_file, output_file, transparent_color, scale):
    suffix = get_file_extension_without_point(output_file).upper()
    rgba_img = convert_to_rgba_with_transparency(input_file, transparent_color, scale)
    rgba_img.save(output_file, format=suffix)
    return rgba_img


# 从一张大图片中切出一块图片出来并保存
# entire_img 整块图片的img
def crop_one_tile_from_entire_image(entire_img, left_top_x, left_top_y, tile_w, tile_h, tile_file_path):
    # 切割图块
    tile_img = entire_img.crop((left_top_x, left_top_y, left_top_x + tile_w, left_top_y + tile_h))
    tile_img.save(tile_file_path)


# 将图片切割成指定尺寸的图块，并保存为单独文件。
# 参数:
# image : 输入图片路径
# tile_width (int): 每个图块的宽度（像素）
# tile_height (int): 每个图块的高度（像素）
# tile_name (str): 图块文件名
# output_dir (str): 输出目录
def split_image_into_tiles(img, tile_width, tile_height, tile_name, output_dir):
    img_width, img_height = img.size

    if output_dir is None:
        output_dir = os.getcwd()
    else:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

    if tile_name is None:
        tile_name = "tile"

    # 计算图块的行列数
    cols = img_width // tile_width
    rows = img_height // tile_height

    # 遍历切割图块
    tile_count = 0
    for row in range(rows):
        for col in range(cols):
            # 计算当前图块的坐标范围
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height

            # 切割图块
            tile = img.crop((left, upper, right, lower))

            # 保存图块（文件名格式: tile_行_列.jpg）
            tile_path = os.path.join(output_dir, f"{tile_name}_{row}_{col}.png")
            tile.save(tile_path)
            tile_count += 1

    print(f"切割完成，共生成 {tile_count} 个图块，保存在目录: {output_dir}")
