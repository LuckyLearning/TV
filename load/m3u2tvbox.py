import re
import sys
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


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("用法: python m3u2tvbox.py m3u.m3u tvbox.txt")
		sys.exit(1)

	m3u = sys.argv[1]
	txt = sys.argv[2]
	m3u_to_tvbox(m3u, txt)
	print(f"转换完成,输出文件为{txt}")
