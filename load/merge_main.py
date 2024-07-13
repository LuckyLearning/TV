import os.path
import shutil
import sys
import urllib.request
from datetime import datetime

import utils

# 定义要访问的多个URL
urls = utils.get_urls()

channel_info = {}
channel = {}
channel_ipv6 = {}


def process_url(url):
	try:
		with urllib.request.urlopen(url) as response:
			data = response.read()
			text = data.decode('utf-8')

			lines = text.split('\n')
			for line in lines:
				if "#genre#" not in line and "," in line and ":" in line:
					line = utils.process_name_string(line.strip())
					channel_name = line.split(',')[0].strip()
					channel_address = line.split(',')[1].strip()
					if not channel_address.startswith("http"):
						continue
					if channel_name not in channel_info:
						channel_info[channel_name] = []
					channel_info[channel_name].append(channel_address)
	except Exception as e:
		print(f"处理URL时发生错误：{e}")


def process():
	for url in urls:
		print(f"处理URL: {url}")
		process_url(url)
	print(f"size: {len(channel_info)}")
	for channel_name, channel_addresses in channel_info.items():
		if channel_name.startswith("CCTV") and not "K" in channel_name and not "COM" in channel_name:
			if "央视频道,#genre#" not in channel:
				channel["央视频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["央视频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "卫视" in channel_name:
			if "卫视频道,#genre#" not in channel:
				channel["卫视频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["卫视频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("NEWTV"):
			if "NewTV频道,#genre#" not in channel:
				channel["NewTV频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["NewTV频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("CETV"):
			if "CETV频道,#genre#" not in channel:
				channel["CETV频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["CETV频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("CGTN"):
			if "CGTN频道,#genre#" not in channel:
				channel["CGTN频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["CGTN频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("TVBS"):
			if "TVBS频道,#genre#" not in channel:
				channel["TVBS频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["TVBS频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("CHC"):
			if "CHC频道,#genre#" not in channel:
				channel["CHC频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["CHC频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("BESTV"):
			if "BESTV频道,#genre#" not in channel:
				channel["BESTV频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["BESTV频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "体育" in channel_name:
			if "体育频道,#genre#" not in channel:
				channel["体育频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["体育频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "春晚" in channel_name:
			if "春晚频道,#genre#" not in channel:
				channel["春晚频道,#genre#"] = []
			for channel_address in channel_addresses:
				channel["春晚频道,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("斗鱼电影"):
			if "斗鱼电影,#genre#" not in channel:
				channel["斗鱼电影,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼电影,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("斗鱼电视剧"):
			if "斗鱼电视剧,#genre#" not in channel:
				channel["斗鱼电视剧,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼电视剧,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼综艺" in channel_name:
			if "斗鱼综艺,#genre#" not in channel:
				channel["斗鱼综艺,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼综艺,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼旅行" in channel_name:
			if "斗鱼旅行,#genre#" not in channel:
				channel["斗鱼旅行,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼旅行,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼游戏" in channel_name:
			if "斗鱼游戏,#genre#" not in channel:
				channel["斗鱼游戏,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼游戏,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼歌舞" in channel_name:
			if "斗鱼歌舞,#genre#" not in channel:
				channel["斗鱼歌舞,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼歌舞,#genre#"].append(
					(channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼" in channel_name:
			if "斗鱼,#genre#" not in channel:
				channel["斗鱼,#genre#"] = []
			for channel_address in channel_addresses:
				channel["斗鱼,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "虎牙" in channel_name:
			if "虎牙,#genre#" not in channel:
				channel["虎牙,#genre#"] = []
			for channel_address in channel_addresses:
				channel["虎牙,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("「B站」"):
			if "B站,#genre#" not in channel:
				channel["B站,#genre#"] = []
			for channel_address in channel_addresses:
				channel["B站,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("解说"):
			if "解说,#genre#" not in channel:
				channel["解说,#genre#"] = []
			for channel_address in channel_addresses:
				channel["解说,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "电影" in channel_name:
			if "电影,#genre#" not in channel:
				channel["电影,#genre#"] = []
			for channel_address in channel_addresses:
				channel["电影,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "电视剧" in channel_name:
			if "电视剧,#genre#" not in channel:
				channel["电视剧,#genre#"] = []
			for channel_address in channel_addresses:
				channel["电视剧,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.endswith("广播"):
			if "广播,#genre#" not in channel:
				channel["广播,#genre#"] = []
			for channel_address in channel_addresses:
				channel["广播,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		else:
			if "其他,#genre#" not in channel:
				channel["其他,#genre#"] = []
			for channel_address in channel_addresses:
				channel["其他,#genre#"].append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))


def get_all_lines():
	for group in channel:
		group_lines = list(set(channel[group]))
		if group == "央视频道,#genre#":
			channel[group] = sorted(utils.sort_channels_cctv(group_lines),
			                        key=lambda x: utils.extract_number(x))
			channel_ipv6[group] = sorted(utils.sort_channels_cctv_ipv6(group_lines),
			                             key=lambda x: utils.extract_number(x))
		elif group == "卫视频道,#genre#":
			channel[group] = utils.sort_channels_ws(group_lines)
			channel_ipv6[group] = utils.sort_channels_ws_ipv6(group_lines)
		else:
			channel[group] = utils.sort_channels(group_lines)
			channel_ipv6[group] = utils.sort_channels_ipv6(group_lines)


def save_to_file(output_file, others_file):
	try:
		# 写入合并的文本到 output_file
		with open(output_file, 'w', encoding='utf-8') as f:
			for group in channel:
				if group != "其他,#genre#":
					group_lines = channel[group]
					if len(group_lines) == 0:
						continue
					f.write(group + '\n')
					for line in group_lines:
						f.write(line + '\n')
				f.write('\n')
		print(f"合并后的文本已保存到文件: {output_file}")

		with open("merge_ipv6.txt", 'w', encoding='utf-8') as f:
			for group in channel_ipv6:
				if group != "其他,#genre#":
					group_lines = channel_ipv6[group]
					if len(group_lines) == 0:
						continue
					f.write(group + '\n')
					for line in group_lines:
						f.write(line + '\n')
				f.write('\n')
		print(f"合并后的文本已保存到文件: merge_ipv6.txt")

		with open(others_file, 'w', encoding='utf-8') as f:
			f.write("其他,#genre#" + '\n')
			for line in channel.get("其他,#genre#", []):
				f.write(line + '\n')
			print(f"已保存到文件: {others_file}")

	except Exception as e:
		print(f"保存文件时发生错误：{e}")


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

	try:
		# 复制文件并重命名
		shutil.copy("merge_ipv6.txt", "../local.txt")
		print(f"文件 merge_ipv6.txt 复制并重命名为 local.txt' 在 ../ 中。")
	except FileNotFoundError:
		print(f"错误: merge_ipv6.txt 未找到。")
	except PermissionError:
		print(f"错误: 拒绝复制 merge_ipv6.txt 的权限。")
	except Exception as e:
		print(f"发生错误: {e}")


if __name__ == '__main__':
	arguments = sys.argv
	if len(arguments) == 1:
		output_file = "merged_output.txt"
		other_file = "others_output.txt"
	elif len(arguments) == 3:
		output_file = arguments[1]
		other_file = arguments[2]
	else:
		print("Usage: python script.py [output_file] [other_file]")
		sys.exit(1)
	process()
	get_all_lines()
	save_to_file(output_file, other_file)
	cpoy_file(output_file, other_file)
