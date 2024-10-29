from PIL import Image
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


# 将指定的图片，转换为32位RGBA格式的图，当像素为指定的透明色transparent_color时，该像素点设置为true
# img_file_path 图片文件的路径名
# transparent_color 作为透明色的颜色三元组
def convert_to_rgba_with_transparency(img_file_path, transparent_color=(255, 255, 255)):
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

    print(f"已将图像转换为32位RGBA格式，并将颜色{transparent_color}设置为透明")
    return rgba_img


def name_to_color(name):
    lower_name = name.lower()
    if lower_name in ("r", "red"):
        return 255, 0, 0
    elif lower_name in ("g", "green"):
        return 0, 255, 0
    elif lower_name in ("b", "blue"):
        return 0, 255, 0
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
def batch_convert(input_dir, out_dir, out_format, transparent_color):
    try:
        extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]  # 指定后缀名列表
        result = get_files_with_extensions(input_dir, extensions)
        for one_file in result:
            base_file_name = get_filename_without_extension(one_file)
            rgba_img = convert_to_rgba_with_transparency(one_file, transparent_color)
            rgba_img.save(f"{out_dir}/{base_file_name}.{out_format}", format=out_format.upper())
    except Exception as e:
        print(f"转换失败，发生错误：{e}")


# input_file            输入文件的完整路径名
# output_file           输出文件的完整路径名
# transparent_color     透明色
def convert_single_file(input_file, output_file, transparent_color):
    suffix = get_file_extension_without_point(output_file).upper()
    rgba_img = convert_to_rgba_with_transparency(input_file, transparent_color)
    rgba_img.save(output_file, format=suffix)
    pass


def main():
    try:
        # 创建解析器
        parser = argparse.ArgumentParser(description="ImageWizard命令行程序")

        # 添加参数
        parser.add_argument('-m', '--mode', type=str, required=True, help="转换模式")
        parser.add_argument('-if', '--input_file', type=str, required=False, help="输入文件")
        parser.add_argument('-of', '--output_file', type=str, required=False, help="输出文件")
        parser.add_argument('-c', '--color', type=str, required=True, help="要作为透明色的颜色")
        parser.add_argument('-idir', '--input_dir', type=str, required=False, help="输入目录")
        parser.add_argument('-odir', '--output_dir', type=str, required=False, help="输出目录")
        parser.add_argument('-ofmt', '--output_format', type=str, required=False, help="输出目录")

        # 解析参数
        args = parser.parse_args()

        mode = args.mode.lower()

        if mode in ("s", "single"):
            transparent_color = parse_color_argument(args.color)
            convert_single_file(args.input_file, args.output_file, transparent_color)
        elif mode in ("b", "batch"):
            transparent_color = parse_color_argument(args.color)
            batch_convert(args.input_dir, args.output_dir, args.output_format, transparent_color)

        print("转换成功")
    except Exception as e:
        print(f"转换失败，发生错误：{e}")


if __name__ == "__main__":
    main()
