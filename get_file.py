import os


def get(file_dir, all_info):
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        # 获取文件的绝对路径
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path):  # 判断是否是文件还是目录需要用绝对路径
            try:
                with open(path, 'r') as file:
                    lines = ''.join(line for line in file)
            except UnicodeDecodeError: # 处理二进制文件的情况
                with open(path, 'rb') as im:
                    lines = str(im.read())
            # 如果文件的内容是空值，那么可能会引发碰撞，所以在空文件我们将带有路径文件名作为内容，避免碰撞
            if not lines:
                lines = path
            info = {
                'title': path.replace('\\', '/'),
                'content': lines
            }
            all_info.append(info)
        if os.path.isdir(path):
            get(path, all_info)  # 递归子目录
    return all_info


def list_dir(file_path):
    all_info = []
    info = get(file_path, all_info)
    return info
