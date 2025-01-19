import re
import sys
import urllib.request
from datetime import datetime

import copy_utils
import trans_utils
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


def process_url_m3u(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            text = data.decode('utf-8')
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('#EXTINF'):
                    match = re.search(r'tvg-name="([^"]+)"', line)
                    if match:
                        channel_name = match.group(1)
                    else:
                        match = re.search(r'tvg-id="([^"]+)"', line)
                        if match:
                            channel_name = match.group(1)
                        else:
                            channel_name = line.split(',')[-1].strip()
                    channel_name = utils.process_part(channel_name.upper())
                    if channel_name not in channel_info:
                        channel_info[channel_name] = []
                elif line and not line.startswith('#'):
                    channel_url = line
                    channel_info[channel_name].append(channel_url)
    except Exception as e:
        print(f"处理URL时发生错误：{e}")


def process():
    for url in urls:
        print(f"处理URL: {url}")
        if url.endswith(".m3u"):
            print(f"处理m3u文件: {url}")
            process_url_m3u(url)
        else:
            print(f"处理非m3u文件: {url}")
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


def get_all_lines():
    sorted_key = sorted(channel.keys(), key=utils.sort_group)
    for group in sorted_key:
        group_lines = list(set(channel[group]))
        if group == "央视频道,#genre#":
            channel[group] = sorted(utils.sort_channels_cctv_not_ipv6(group_lines),
                                    key=lambda x: utils.extract_number(x))
            channel_ipv6["IPV6_央视频道,#genre#"] = sorted(utils.sort_channels_cctv_ipv6(group_lines),
                                         key=lambda x: utils.extract_number(x))
        elif group == "卫视频道,#genre#":
            channel[group] = utils.sort_channels_ws_not_ipv6(group_lines)
            channel_ipv6["IPV6_卫视频道,#genre#"] = utils.sort_channels_ws_ipv6(group_lines)


def save_to_file(output_file):
    try:
        # 获取当前日期和时间，格式为 yyyy-mm-dd HH:mm:ss
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 写入合并的文本到 output_file
        with open(output_file, 'w', encoding='utf-8') as f:
            for group in channel:
                group_lines = channel[group]
                if len(group_lines) == 0:
                    continue
                f.write(group + '\n')
                for line in group_lines:
                    f.write(line + '\n')
                f.write('\n')
            f.write('\n')

            for group in channel_ipv6:
                group_lines = channel_ipv6[group]
                if len(group_lines) == 0:
                    continue
                f.write(group + '\n')
                for line in group_lines:
                    f.write(line + '\n')
            f.write('\n')
            # 写入更新日期作为新的频道组名
            f.write(f"更新时间: {current_time},#genre#\n")
            f.write(f"最后更新时间: {current_time}\n")
        print(f"合并后的文本已保存到文件: {output_file}")

    except Exception as e:
        print(f"保存文件时发生错误：{e}")


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) == 1:
        output_file = "merged_output.txt"
    elif len(arguments) == 2:
        output_file = arguments[1]
    else:
        print("Usage: python script.py [output_file]")
        sys.exit(1)
    process()
    get_all_lines()
    save_to_file(output_file)

    copy_utils.copy_file_with_retention(output_file, 30)
    copy_utils.copy_source_2_target(output_file, "../local.txt")
    trans_utils.trans2m3u(output_file)
