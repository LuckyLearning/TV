import ipaddress
import os.path
import re  # 正则
import shutil
import sys
import urllib.request
from datetime import datetime
from urllib.parse import urlparse
from datetime import datetime

import config

# 定义要访问的多个URL
urls = config.get_urls()

# 定义多个对象用于存储不同内容的行文本
ys_lines = []  # 央视
ws_lines = []  # 卫视
ty_lines = []  # 体育
sh_lines = []  # 上海
dy_lines = []  # 电影
dsj_lines = []  # 电视剧
gat_lines = []  # 港澳台
gj_lines = []  # 国际台
jlp_lines = []  # 记录片
dhp_lines = []  # 动画片
xq_lines = []  # 戏曲
js_lines = []  # 解说
cw_lines = []  # 春晚
mx_lines = []  # 明星
ztp_lines = []  # 主题片
zy_lines = []  # 综艺频道

all_lines = []
other_lines = []


# 判断URL地址是否是IPv6的
def is_ipv6(url):
	try:
		parsed_url = urlparse(url)
		host = parsed_url.hostname
		ip = ipaddress.ip_address(host)
		return isinstance(ip, ipaddress.IPv6Address)
	except ValueError:
		return False


def process_name_string(input_str):
	parts = input_str.split(',')
	processed_parts = []
	for part in parts:
		processed_part = process_part(part)
		processed_parts.append(processed_part)
	result_str = ','.join(processed_parts)
	return result_str


def process_part(part_str):
	if part_str.startswith("CCTV"):
		part_str = part_str.replace("IPV6", "")
		filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
		if not filtered_str.strip():
			filtered_str = part_str.replace("CCTV", "")
		return "CCTV-" + filtered_str

	elif "卫视" in part_str:
		match = re.search(r'.*卫视', part_str)
		if match:
			return match.group(0)
		else:
			return part_str

	return part_str


def process_url(url):
	try:
		with urllib.request.urlopen(url) as response:
			data = response.read()
			text = data.decode('utf-8')

			lines = text.split('\n')
			for line in lines:
				if "#genre#" not in line and "," in line and ":" in line:
					channel_name = line.split(',')[0].strip().upper()
					channel_address = line.split(',')[1].strip()
					if not channel_address.startswith("http"):
						continue
					if "CCTV" in channel_name:
						ys_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif "卫视" in channel_name:
						ws_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif "体育" in channel_name:
						ty_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in dy_dictionary:
						dy_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in dsj_dictionary:
						dsj_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in sh_dictionary:
						sh_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in gat_dictionary:
						gat_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in gj_dictionary:
						gj_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in jlp_dictionary:
						jlp_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in dhp_dictionary:
						dhp_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in xq_dictionary:
						xq_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in js_dictionary:
						js_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in cw_dictionary:
						cw_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in mx_dictionary:
						mx_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in ztp_dictionary:
						ztp_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					elif channel_name in zy_dictionary:
						zy_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))
					else:
						other_lines.append((process_name_string(line.strip()), is_ipv6(channel_address)))

	except Exception as e:
		print(f"处理URL时发生错误：{e}")


def read_txt_to_array(file_name):
	try:
		with open(file_name, 'r', encoding='utf-8') as file:
			lines = file.readlines()
			lines = [line.strip() for line in lines]
			return lines
	except FileNotFoundError:
		print(f"File '{file_name}' not found.")
		return []
	except Exception as e:
		print(f"An error occurred: {e}")
		return []


def process():
	global ys_dictionary, ws_dictionary, ty_dictionary, sh_dictionary, \
		dy_dictionary, dsj_dictionary, gat_dictionary, gj_dictionary, \
		jlp_dictionary, dhp_dictionary, xq_dictionary, js_dictionary, \
		cw_dictionary, mx_dictionary, ztp_dictionary, zy_dictionary
	dy_dictionary = read_txt_to_array('电影.txt')
	dsj_dictionary = read_txt_to_array('电视剧.txt')
	sh_dictionary = read_txt_to_array('shanghai.txt')
	gat_dictionary = read_txt_to_array('港澳台.txt')
	gj_dictionary = read_txt_to_array('国际台.txt')
	jlp_dictionary = read_txt_to_array('纪录片.txt')
	dhp_dictionary = read_txt_to_array('动画片.txt')
	xq_dictionary = read_txt_to_array('戏曲频道.txt')
	js_dictionary = read_txt_to_array('解说频道.txt')
	cw_dictionary = read_txt_to_array('春晚.txt')
	mx_dictionary = read_txt_to_array('明星.txt')
	ztp_dictionary = read_txt_to_array('主题片.txt')
	zy_dictionary = read_txt_to_array('综艺频道.txt')
	for url in urls:
		print(f"处理URL: {url}")
		process_url(url)


def extract_number(s):
	caption = s.split(',')[0]
	if s.startswith("CCTV"):
		num_str = caption.split('-')[1]
		if "4K" in num_str:
			return 19
		elif "8K" in num_str:
			return 20
		else:
			numbers = re.findall(r'\d+', num_str)
			if len(numbers) == 0:
				return 21
			sort_num = int(numbers[-1])
			if sort_num > 5 or num_str == "5+":
				sort_num += 1
			return sort_num if numbers else 999
	else:
		return abs(hash(caption))


def sort_channels(channels):
	ipv6_channels = [c for c in channels if c[1]]
	other_channels = [c for c in channels if not c[1]]
	sorted_channels = sorted(ipv6_channels, key=lambda x: extract_number(x[0])) + sorted(other_channels,
	                                                                                     key=lambda x: extract_number(
		                                                                                     x[0]))
	return [c[0] for c in sorted_channels]


def sort_channels_ipv6(channels):
	ipv6_channels = [c for c in channels if c[1]]
	sorted_channels = sorted(ipv6_channels, key=lambda x: extract_number(x[0]))
	return [c[0] for c in sorted_channels]


def get_all_lines():
	global all_lines
	version = datetime.now().strftime("%Y%m%d") + ",url"
	all_lines = ["更新时间,#genre#"] + [version] + ['\n'] + \
	            ["央视频道,#genre#"] + sorted(sort_channels(ys_lines), key=lambda x: extract_number(x)) + ['\n'] + \
	            ["卫视频道,#genre#"] + sort_channels_ipv6(ws_lines)


# ["卫视频道,#genre#"] + sort_channels(ws_lines) + ['\n'] + \
# ["体育频道,#genre#"] + sort_channels(ty_lines) + ['\n'] + \
# ["上海频道,#genre#"] + sort_channels(sh_lines) + ['\n'] + \
# ["电影频道,#genre#"] + sort_channels(dy_lines) + ['\n'] + \
# ["电视剧频道,#genre#"] + sort_channels(dsj_lines) + ['\n'] + \
# ["明星,#genre#"] + sort_channels(mx_lines) + ['\n'] + \
# ["主题片,#genre#"] + sort_channels(ztp_lines) + ['\n'] + \
# ["港澳台,#genre#"] + sort_channels(gat_lines) + ['\n'] + \
# ["国际台,#genre#"] + sort_channels(gj_lines) + ['\n'] + \
# ["纪录片,#genre#"] + sort_channels(jlp_lines) + ['\n'] + \
# ["动画片,#genre#"] + sort_channels(dhp_lines) + ['\n'] + \
# ["戏曲频道,#genre#"] + sort_channels(xq_lines) + ['\n'] + \
# ["解说频道,#genre#"] + sort_channels(js_lines) + ['\n'] + \
# ["综艺频道,#genre#"] + sort_channels(zy_lines) + ['\n'] + \
# ["春晚,#genre#"] + sort_channels(cw_lines)

def save_to_file(output_file, others_file):
	try:
		# 写入合并的文本到 output_file
		with open(output_file, 'w', encoding='utf-8') as f:
			for line in all_lines:
				f.write(line + '\n')
		print(f"合并后的文本已保存到文件: {output_file}")

		# 写入其他文件内容到 others_file
		files_to_write = [
			(other_lines, 'other_lines'),
			(ty_lines, 'ty_lines'),
			(sh_lines, 'sh_lines'),
			(dy_lines, 'dy_lines'),
			(dsj_lines, 'dsj_lines'),
			(mx_lines, 'mx_lines'),
			(ztp_lines, 'ztp_lines'),
			(gat_lines, 'gat_lines'),
			(gj_lines, 'gj_lines'),
			(jlp_lines, 'jlp_lines'),
			(dhp_lines, 'dhp_lines'),
			(xq_lines, 'xq_lines'),
			(js_lines, 'js_lines'),
			(zy_lines, 'zy_lines'),
			(cw_lines, 'cw_lines')
		]

		with open(others_file, 'w', encoding='utf-8') as f:
			for lines, name in files_to_write:
				for line, ipv6 in lines:
					f.write(line + '\n')
				print(f"{name} 已保存到文件: {others_file}")

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
