from typing import Any
from PIL import Image
from pathlib import Path
import argparse
import os
import ImageTools

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
        parser.add_argument('-ofmt', '--output_format', type=str, required=False, help="输出格式")
        parser.add_argument('-spltw', '--split_image_tile_width', type=int, required=False,
                            help="切割图像的单个图块宽度")
        parser.add_argument('-splth', '--split_image_tile_height', type=int, required=False,
                            help="切割图像的单个图块高度")
        parser.add_argument('-sc', '--scale', type=int, required=False, help="生成图片的放大系数")

        # 解析参数
        args = parser.parse_args()
        mode = args.mode.lower()
        rgba_img = None

        scale = 1

        if args.scale is not None and args.scale != 1:
            scale = args.scale

        if mode in ("s", "single"):
            transparent_color = ImageTools.parse_color_argument(args.color)
            rgba_img = ImageTools.convert_single_file(args.input_file, args.output_file, transparent_color, scale)
        elif mode in ("b", "batch"):
            transparent_color = ImageTools.parse_color_argument(args.color)
            ImageTools.batch_convert(args.input_dir, args.output_dir, args.output_format, transparent_color, scale)

        print("转换成功")

        ba = mode in ("s", "single")
        bb = rgba_img is not None
        bc = args.split_image_tile_width is not None
        bd = args.split_image_tile_height is not None

        if ba and bb and bc and bd:
            ImageTools.split_image_into_tiles(rgba_img, args.split_image_tile_width, args.split_image_tile_height,
                                              Path(args.input_file).stem, args.output_dir)

    except Exception as e:
        print(f"转换失败，发生错误：{e}")


if __name__ == "__main__":
    main()
