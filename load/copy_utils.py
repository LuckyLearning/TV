import os
import shutil
from datetime import datetime

def cpoy_file(output_file, other_file, days_to_keep):
    path_to_check = "merge"
    if not os.path.exists(path_to_check):
        # 如果路径不存在，则创建路径
        os.makedirs(path_to_check)
        print(f"路径 '{path_to_check}' 创建成功。")
    else:
        print(f"路径 '{path_to_check}' 已经存在。")

    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy_mm_dd_
    formatted_date = current_date.strftime('%Y_%m_%d')

    # 获取源文件名和扩展名
    file_name1, file_ext1 = os.path.splitext(os.path.basename(output_file))
    file_name2, file_ext2 = os.path.splitext(os.path.basename(other_file))

    # 构建新文件名
    new_output_file = f"{formatted_date}_{file_name1}{file_ext1}"
    new_other_file = f"{formatted_date}_{file_name2}{file_ext2}"

    # 构建目标文件路径
    destination_output_file = os.path.join(path_to_check, new_output_file)
    destination_other_file = os.path.join(path_to_check, new_other_file)

    # 复制文件并处理异常
    def copy_file(src, dst):
        try:
            shutil.copy(src, dst)
            print(f"文件 '{src}' 复制并重命名为 '{dst}' 在 '{path_to_check}' 中。")
        except FileNotFoundError:
            print(f"错误: '{src}' 未找到。")
        except PermissionError:
            print(f"错误: 拒绝复制 '{src}' 的权限。")
        except Exception as e:
            print(f"发生错误: {e}")

    copy_file(output_file, destination_output_file)
    copy_file(other_file, destination_other_file)

    # 检查文件名中的日期，删除超期文件
    def manage_folder_by_date(folder, days_to_keep):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        today = datetime.now()
        for file_path in files:
            file_name = os.path.basename(file_path)
            # 从文件名中提取日期部分，假设文件名格式为 yyyy_mm_dd_*
            try:
                date_part = file_name.split('_')[0:3]  # 取出前三段作为日期部分
                file_date = datetime.strptime('_'.join(date_part), '%Y_%m_%d')
                if (today - file_date).days > days_to_keep:
                    os.remove(file_path)
                    print(f"文件 '{file_path}' 超期，已删除。")
            except ValueError:
                print(f"警告: 文件名 '{file_name}' 中的日期无效，跳过。")

    # 调用日期管理函数，删除超期文件
    manage_folder_by_date(path_to_check, days_to_keep)

def copy_file_with_retention(output_file, days_to_keep):
    """
    复制文件到 merge 文件夹，并根据文件名中的日期删除超期文件
    :param output_file: 要复制的文件路径
    :param days_to_keep: 保留文件的天数
    """
    # 检查 merge 文件夹是否存在，如果不存在则创建
    path_to_check = "merge"
    if not os.path.exists(path_to_check):
        os.makedirs(path_to_check)
        print(f"路径 '{path_to_check}' 创建成功。")
    else:
        print(f"路径 '{path_to_check}' 已经存在。")

    # 获取当前日期并格式化
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y_%m_%d')

    # 获取源文件名和扩展名
    file_name, file_ext = os.path.splitext(os.path.basename(output_file))

    # 构建新文件名
    new_output_file = f"{formatted_date}_{file_name}{file_ext}"

    # 构建目标文件路径
    destination_output_file = os.path.join(path_to_check, new_output_file)

    # 复制文件并处理异常
    try:
        shutil.copy(output_file, destination_output_file)
        print(f"文件 '{output_file}' 复制并重命名为 '{destination_output_file}' 在 '{path_to_check}' 中。")
    except FileNotFoundError:
        print(f"错误: '{output_file}' 未找到。")
    except PermissionError:
        print(f"错误: 拒绝复制 '{output_file}' 的权限。")
    except Exception as e:
        print(f"发生错误: {e}")

    # 检查文件名中的日期，删除超期文件
    def manage_folder_by_date(folder, days_to_keep):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        today = datetime.now()
        for file_path in files:
            file_name = os.path.basename(file_path)
            # 从文件名中提取日期部分，假设文件名格式为 yyyy_mm_dd_*
            try:
                date_part = file_name.split('_')[0:3]  # 取出前三段作为日期部分
                file_date = datetime.strptime('_'.join(date_part), '%Y_%m_%d')
                if (today - file_date).days > days_to_keep:
                    os.remove(file_path)
                    print(f"文件 '{file_path}' 超期，已删除。")
            except ValueError:
                print(f"警告: 文件名 '{file_name}' 中的日期无效，跳过。")

    # 调用日期管理函数，删除超期文件
    manage_folder_by_date(path_to_check, days_to_keep)


def copy_source_2_target(source_file, target_file):
	try:
		# 复制文件并重命名
		shutil.copy(source_file, target_file)
		print(f"文件 {source_file} 复制并重命名为 {target_file}'。")
	except FileNotFoundError:
		print(f"错误: {source_file} 未找到。")
	except PermissionError:
		print(f"错误: 拒绝复制 {source_file} 的权限。")
	except Exception as e:
		print(f"发生错误: {e}")
