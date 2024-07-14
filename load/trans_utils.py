import os
import re
from collections import defaultdict


def m3u_to_tvbox(m3u_file, tvbox_file):
	# 读取m3u格式的直播源信息
	with open(m3u_file, 'r', encoding='utf-8') as file:
		m3u_content = file.read()

	# 解析m3u格式的直播源信息
	channel_info = re.findall(r'#EXTINF:-1.*?tvg-name="(.*?)".*?group-title="(.*?)".*?\n(.*?)\n', m3u_content)

	# 按分组合并频道
	channel_groups = defaultdict(list)
	for name, group, url in channel_info:
		channel_groups[group].append((name, url))

	# 转换为tvbox识别的txt格式
	with open(tvbox_file, 'w', encoding='utf-8') as file:
		for group, channels in channel_groups.items():
			file.write(f'#genre#{group}\n')
			for name, url in channels:
				file.write(f'{name},{url}\n')
			file.write('\n')


def trans2m3u(tvbox_file):
	file_name, file_ext = os.path.splitext(os.path.basename(tvbox_file))
	m3u_file = f"{file_name}.m3u"
	with open(tvbox_file, 'r', encoding="utf-8") as f:
		lines = f.readlines()

	channels = {}
	current_genre = None

	# Parse the tvbox file
	for line in lines:
		line = line.strip()
		if line.endswith('#genre#'):
			current_genre = line.split(',')[0]
		elif line:
			channel_name, channel_url = line.split(',')
			if current_genre not in channels:
				channels[current_genre] = []
			channels[current_genre].append((channel_name, channel_url))

	# Generate the m3u playlist
	with open(m3u_file, 'w', encoding="utf-8") as f:
		for genre, channel_list in channels.items():
			f.write("#EXTM3U\n")
			for channel_name, channel_url in channel_list:
				f.write(
					'#EXTINF:-1 tvg-name="{channel_name}" group-title="{genre}",{channel_name}\n{channel_url}\n'.format(
						channel_name=channel_name, genre=genre, channel_url=channel_url))
			f.write('\n')

	print('Conversion complete. The m3u playlist has been saved as', m3u_file)
