import os.path
import shutil
from datetime import datetime


def cpoy_file(output_file, other_file):
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

	try:
		# 复制文件并重命名
		shutil.copy(output_file, destination_output_file)
		print(f"文件 '{output_file}' 复制并重命名为 '{new_output_file}' 在 '{path_to_check}' 中。")
	except FileNotFoundError:
		print(f"错误: '{output_file}' 未找到。")
	except PermissionError:
		print(f"错误: 拒绝复制 '{output_file}' 的权限。")
	except Exception as e:
		print(f"发生错误: {e}")

	try:
		shutil.copy(other_file, destination_other_file)
		print(f"文件 '{other_file}' 复制并重命名为 '{new_other_file}' 在 '{path_to_check}' 中。")
	except FileNotFoundError:
		print(f"错误: '{other_file}' 未找到。")
	except PermissionError:
		print(f"错误: 拒绝复制 '{other_file}' 的权限。")
	except Exception as e:
		print(f"发生错误: {e}")


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
