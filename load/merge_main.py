import os.path
import shutil
import sys
import urllib.request
from datetime import datetime

import utils

# 定义要访问的多个URL
urls = utils.get_urls()

# 定义多个对象用于存储不同内容的行文本
ys_lines = []  # 央视
ws_lines = []  # 卫视
dying_lines = []  # 电影
dsj_lines = []  # 电视剧
NewTV_lines = []  # NewTV
ty_lines = []  # 体育
cw_lines = []  # 春晚
dy_lines = []  # 斗鱼
hy_lines = []  # 虎牙
bli_lines = []  # 哔哩
dydy_lines = []  # 斗鱼电影
dydsj_lines = []  # 斗鱼电视剧
# 斗鱼旅行
dylx_lines = []
# 斗鱼综艺
dyzy_lines = []
# 斗鱼歌舞
dygw_lines = []
# 斗鱼游戏
dyyx_lines = []
js_lines = []  # 解说
# BESTV
bestv_lines = []
cetv_lines = []  # CETV
cgtn_lines = []  # CGTN
tvbs_lines = []  # TVBS
chc_lines = []  # CHC
gb_lines = []  # 广播

all_lines = []
other_lines = []

channel_info = {}


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
			for channel_address in channel_addresses:
				ys_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "卫视" in channel_name:
			for channel_address in channel_addresses:
				ws_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("NEWTV"):
			for channel_address in channel_addresses:
				NewTV_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("CETV"):
			for channel_address in channel_addresses:
				cetv_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("CGTN"):
			for channel_address in channel_addresses:
				cgtn_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("TVBS"):
			for channel_address in channel_addresses:
				tvbs_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("CHC"):
			for channel_address in channel_addresses:
				chc_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("BESTV"):
			for channel_address in channel_addresses:
				bestv_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "体育" in channel_name:
			for channel_address in channel_addresses:
				ty_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "春晚" in channel_name:
			for channel_address in channel_addresses:
				cw_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("斗鱼电影"):
			for channel_address in channel_addresses:
				dydy_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("斗鱼电视剧"):
			for channel_address in channel_addresses:
				dydsj_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼综艺" in channel_name:
			for channel_address in channel_addresses:
				dyzy_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼旅行" in channel_name:
			for channel_address in channel_addresses:
				dylx_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼游戏" in channel_name:
			for channel_address in channel_addresses:
				dyyx_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼歌舞" in channel_name:
			for channel_address in channel_addresses:
				dygw_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "斗鱼" in channel_name:
			for channel_address in channel_addresses:
				dy_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "虎牙" in channel_name:
			for channel_address in channel_addresses:
				hy_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("「B站」"):
			for channel_address in channel_addresses:
				bli_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.startswith("解说"):
			for channel_address in channel_addresses:
				js_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "电影" in channel_name:
			for channel_address in channel_addresses:
				dying_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif "电视剧" in channel_name:
			for channel_address in channel_addresses:
				dsj_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		elif channel_name.endswith("广播"):
			for channel_address in channel_addresses:
				gb_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))
		else:
			for channel_address in channel_addresses:
				other_lines.append((channel_name + "," + channel_address, utils.is_ipv6(channel_address)))


def get_all_lines():
	global all_lines
	version = datetime.now().strftime("%Y%m%d") + ",url"
	all_lines = ["更新时间,#genre#"] + [version] + ['\n'] + \
	            ["央视频道,#genre#"] + sorted(utils.sort_channels_cctv(ys_lines),
	                                          key=lambda x: utils.extract_number(x)) + ['\n'] + \
	            ["卫视频道,#genre#"] + utils.sort_channels_ws(ws_lines) + ['\n'] + \
	            ["电影频道,#genre#"] + utils.sort_channels(dying_lines) + ['\n'] + \
	            ["电视剧频道,#genre#"] + utils.sort_channels(dsj_lines) + ['\n'] + \
	            ["体育频道,#genre#"] + utils.sort_channels(ty_lines) + ['\n'] + \
	            ["NewTV,#genre#"] + utils.sort_channels(NewTV_lines) + ['\n'] + \
	            ["CETV,#genre#"] + utils.sort_channels(cetv_lines) + ['\n'] + \
	            ["CGTN,#genre#"] + utils.sort_channels(cgtn_lines) + ['\n'] + \
	            ["TVBS,#genre#"] + utils.sort_channels(tvbs_lines) + ['\n'] + \
	            ["CHC,#genre#"] + utils.sort_channels(chc_lines) + ['\n'] + \
	            ["Bestv,#genre#"] + utils.sort_channels(bestv_lines) + ['\n'] + \
	            ["春晚,#genre#"] + utils.sort_channels(cw_lines) + ['\n'] + \
	            ["斗鱼电影,#genre#"] + utils.sort_channels(dydy_lines) + ['\n'] + \
	            ["斗鱼电视剧,#genre#"] + utils.sort_channels(dydsj_lines) + ['\n'] + \
	            ["斗鱼综艺,#genre#"] + utils.sort_channels(dyzy_lines) + ['\n'] + \
	            ["斗鱼旅行,#genre#"] + utils.sort_channels(dylx_lines) + ['\n'] + \
	            ["斗鱼游戏,#genre#"] + utils.sort_channels(dyyx_lines) + ['\n'] + \
	            ["斗鱼歌舞,#genre#"] + utils.sort_channels(dygw_lines) + ['\n'] + \
	            ["斗鱼,#genre#"] + utils.sort_channels(dy_lines) + ['\n'] + \
	            ["虎牙,#genre#"] + utils.sort_channels(hy_lines) + ['\n'] + \
	            ["哔哩哔哩,#genre#"] + utils.sort_channels(bli_lines) + ['\n'] + \
	            ["解说,#genre#"] + utils.sort_channels(js_lines) + ['\n'] + \
	            ["广播,#genre#"] + utils.sort_channels(gb_lines)


def save_to_file(output_file, others_file):
	try:
		# 写入合并的文本到 output_file
		with open(output_file, 'w', encoding='utf-8') as f:
			for line in all_lines:
				f.write(line + '\n')
		print(f"合并后的文本已保存到文件: {output_file}")

		with open(others_file, 'w', encoding='utf-8') as f:
			for line, ipv6 in other_lines:
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
