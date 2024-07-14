import ipaddress
import re
from urllib.parse import urlparse

import yaml


def get_urls():
	with open('urls.yml', 'r', encoding='utf-8') as file:
		config = yaml.safe_load(file)
	urls = config.get('urls', [])
	return urls

def is_ipv6(url):
	"""
	判断URL地址是否是IPv6的
	:param url: url地址
	:return: True or False
	"""
	try:
		parsed_url = urlparse(url)
		host = parsed_url.hostname
		ip = ipaddress.ip_address(host)
		return isinstance(ip, ipaddress.IPv6Address)
	except ValueError:
		return False


def process_name_string(input_str):
	parts = input_str.split(',')
	result_str = process_part(parts[0].upper()) + ',' + parts[1]
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

def sort_group(group_name):
	if group_name.startswith('央视频道'):
		return (0, group_name)  # '央视频道' 排在最前面
	elif group_name.startswith('卫视频道'):
		return (1, group_name)
	return (2, group_name)  # 其他项按默认顺序排列


def sort_channels_cctv(channels):
	ipv6_channels = [c for c in channels if c[1]]
	other_channels = [c for c in channels if not c[1]]
	sorted_channels = sorted(ipv6_channels, key=lambda x: extract_number(x[0])) + sorted(other_channels,
	                                                                                     key=lambda x: extract_number(
		                                                                                     x[0]))
	return [c[0] for c in sorted_channels]

def sort_channels_cctv_ipv6(channels):
	ipv6_channels = [c for c in channels if c[1]]
	sorted_channels = sorted(ipv6_channels, key=lambda x: extract_number(x[0]))
	return [c[0] for c in sorted_channels]

def sort_channels(channels):
	sorted_channels = sorted(channels)
	return [c[0] for c in sorted_channels]

def sort_channels_ipv6(channels):
	ipv6_channels = [c for c in channels if c[1]]
	sorted_channels = sorted(ipv6_channels)
	return [c[0] for c in sorted_channels]


def sort_channels_ws(channels):
	ipv6_channels = [c for c in channels if c[1]]
	sorted_channels = sorted(ipv6_channels, key=lambda x: extract_number(x[0]))
	return [c[0] for c in sorted_channels]

def sort_channels_ws_ipv6(channels):
	ipv6_channels = [c for c in channels if c[1]]
	sorted_channels = sorted(ipv6_channels, key=lambda x: extract_number(x[0]))
	return [c[0] for c in sorted_channels]


def get_dict_from_file():
	"""
	获取白名单的字典
	:return:
	"""
	dy_dictionary = read_txt_to_array('电影.txt')
	dsj_dictionary = read_txt_to_array('电视剧.txt')
	sh_dictionary = read_txt_to_array('上海.txt')
	gat_dictionary = read_txt_to_array('港澳台.txt')
	gj_dictionary = read_txt_to_array('国际台.txt')
	jlp_dictionary = read_txt_to_array('纪录片.txt')
	dhp_dictionary = read_txt_to_array('动画片.txt')
	xq_dictionary = read_txt_to_array('戏曲.txt')
	js_dictionary = read_txt_to_array('解说.txt')
	cw_dictionary = read_txt_to_array('春晚.txt')
	mx_dictionary = read_txt_to_array('明星.txt')
	ztp_dictionary = read_txt_to_array('主题片.txt')
	zy_dictionary = read_txt_to_array('综艺.txt')
	all_dict = {
		"上海": sh_dictionary,
		"电影": dy_dictionary,
		"电视剧": dsj_dictionary,
		"明星": mx_dictionary,
		"主题片": ztp_dictionary,
		"港澳台": gat_dictionary,
		"国际台": gj_dictionary,
		"纪录片": jlp_dictionary,
		"动画片": dhp_dictionary,
		"戏曲": xq_dictionary,
		"解说": js_dictionary,
		"春晚": cw_dictionary,
		"综艺": zy_dictionary
	}
	return all_dict
