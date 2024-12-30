import os
import re

# 设置项目的根目录
PROJECT_DIR = "D:/python/captcha_trainer-master/projects"

# 定义一个图片文件格式列表，支持jpg、jpeg、png、gif、bmp、webp等格式
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]

# 默认标签名称
DEFAULT_LABEL = "_label"

# 正则表达式匹配图片文件名中的标签部分
extract_regex = r"^(.*?)(?=\.(jpg|jpeg|png|gif|bmp|webp)$)"

# 判断文件名是否包含有效标签
def has_valid_label(filename):
    """
    判断文件名中是否包含有效的标签部分（即下划线后面有字符）。
    :param filename: 文件名
    :return: 如果有有效标签则返回 True，否则返回 False
    """
    match = re.search(r"_(\w+)$", filename)
    return match is not None

def remove_extra_label(filename):
    """
    去掉文件名中多余的 `_label`，只保留一个。
    :param filename: 文件名
    :return: 去除多余 `_label` 后的文件名
    """
    # 去掉所有 `_label`，然后保留一个
    parts = filename.split(DEFAULT_LABEL)
    if len(parts) > 2:
        return parts[0] + DEFAULT_LABEL + ''.join(parts[2:])
    return filename

def rename_files_in_directory(directory):
    """
    遍历指定目录，重命名所有没有标签部分的图片文件。
    如果文件名没有有效的标签部分，则自动添加。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 获取文件扩展名
            file_extension = os.path.splitext(file)[1].lower()

            # 如果是图片文件
            if file_extension in IMAGE_EXTENSIONS:
                print(f"Processing: {file}")  # 打印正在处理的文件名

                # 检查是否已经有标签部分
                if file.count(DEFAULT_LABEL) > 1:
                    # 文件名中有多个 '_label'，去除多余的
                    new_name = remove_extra_label(file)
                    print(f"Removed extra '_label' from: {file} -> {new_name}")
                else:
                    # 文件没有标签，添加 '_label'
                    if "_" in file:
                        # 文件名中有下划线，但没有 '_label'，添加 '_label'
                        new_name = file.rsplit('_', 1)[0] + DEFAULT_LABEL + file_extension
                    else:
                        # 文件名没有下划线，直接添加 '_label'
                        match = re.match(extract_regex, file)
                        if match:
                            new_name = match.group(1) + DEFAULT_LABEL + file_extension
                        else:
                            print(f"Skipping: {file} (no valid name prefix found)")
                            continue
                    print(f"Renamed: {file} -> {new_name}")

                # 检查目标文件是否已存在，若已存在则跳过
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                if os.path.exists(new_path):
                    print(f"Skipping: {file} (duplicate name {new_name})")
                else:
                    # 重命名文件
                    os.rename(old_path, new_path)

if __name__ == "__main__":
    rename_files_in_directory(PROJECT_DIR)
