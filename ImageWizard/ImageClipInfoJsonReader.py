# 裁剪图片的配置信息json文件的模块

import json
import os


def ReadJsonFile(file_path):
    """
    读取包含矩形信息的JSON文件（旧格式，数组形式）
    :param file_path: JSON文件路径
    :return: 解析后的数据列表，如果出错返回None
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        if not file_path.lower().endswith('.json'):
            raise ValueError("请提供JSON格式的文件")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("JSON文件内容应该是一个数组")

            required_fields = {'name', 'left_top_x', 'left_top_y', 'width', 'height'}
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    raise ValueError(f"第 {i + 1} 个元素不是对象")
                if not required_fields.issubset(item.keys()):
                    missing = required_fields - set(item.keys())
                    raise ValueError(f"第 {i + 1} 个对象缺少字段: {missing}")

                numeric_fields = ['left_top_x', 'left_top_y', 'width', 'height']
                for field in numeric_fields:
                    if not isinstance(item[field], (int, float)):
                        raise ValueError(f"第 {i + 1} 个对象的 {field} 应该是数字")

            return data

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except FileNotFoundError as e:
        print(f"文件错误: {e}")
    except ValueError as e:
        print(f"数据格式错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

    return None


def ReadClipInfoJsonFile(file_path):
    """
    读取包含切片类型的JSON文件（新格式，包含多个切片类型）
    :param file_path: JSON文件路径
    :return: 解析后的数据字典，key为切片类型名称，value为切片信息列表，如果出错返回None
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        if not file_path.lower().endswith('.json'):
            raise ValueError("请提供JSON格式的文件")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("JSON文件内容应该是一个对象")

            required_fields = {'name', 'left_top_x', 'left_top_y', 'width', 'height'}

            for clip_type, clip_list in data.items():
                if not isinstance(clip_list, list):
                    raise ValueError(f"切片类型 {clip_type} 的内容应该是一个数组")

                for i, item in enumerate(clip_list):
                    if not isinstance(item, dict):
                        raise ValueError(f"切片类型 {clip_type} 的第 {i + 1} 个元素不是对象")
                    if not required_fields.issubset(item.keys()):
                        missing = required_fields - set(item.keys())
                        raise ValueError(f"切片类型 {clip_type} 的第 {i + 1} 个对象缺少字段: {missing}")

                    numeric_fields = ['left_top_x', 'left_top_y', 'width', 'height']
                    for field in numeric_fields:
                        if not isinstance(item[field], (int, float)):
                            raise ValueError(f"切片类型 {clip_type} 的第 {i + 1} 个对象的 {field} 应该是数字")

            return data

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except FileNotFoundError as e:
        print(f"文件错误: {e}")
    except ValueError as e:
        print(f"数据格式错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

    return None

'''
# 使用示例
if __name__ == "__main__":
    # 假设JSON文件名为 rectangles.json
    json_data = read_json_file("rectangles.json")

    if json_data:
        print("成功读取JSON数据:")
        for i, rect in enumerate(json_data, 1):
            print(f"\n矩形 {i}:")
            print(f"名称: {rect['name']}")
            print(f"左上角坐标: ({rect['topleft_x']}, {rect['topleft_y']})")
            print(f"宽度: {rect['width']}")
            print(f"高度: {rect['height']}")
            # 计算右下角坐标
            bottom_right_x = rect['topleft_x'] + rect['width']
            bottom_right_y = rect['topleft_y'] + rect['height']
            print(f"右下角坐标: ({bottom_right_x}, {bottom_right_y})")
    else:
        print("读取JSON文件失败")
'''