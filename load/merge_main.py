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
        if channel_name.startswith("CCTV") and "K" not in channel_name and "COM" not in channel_name:
            group_name = "央视频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "卫视" in channel_name:
            group_name = "卫视频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("NEWTV"):
            group_name = "NewTV频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("CETV"):
            group_name = "CETV频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("CGTN"):
            group_name = "CGTN频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("TVBS"):
            group_name = "TVBS频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("CHC"):
            group_name = "CHC频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("BESTV"):
            group_name = "BESTV频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "体育" in channel_name:
            group_name = "体育频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "春晚" in channel_name:
            group_name = "春晚频道,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("斗鱼电影"):
            group_name = "斗鱼电影,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("斗鱼电视剧"):
            group_name = "斗鱼电视剧,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "斗鱼综艺" in channel_name:
            group_name = "斗鱼综艺,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "斗鱼旅行" in channel_name:
            group_name = "斗鱼旅行,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "斗鱼游戏" in channel_name:
            group_name = "斗鱼游戏,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "斗鱼歌舞" in channel_name:
            group_name = "斗鱼歌舞,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "斗鱼" in channel_name:
            group_name = "斗鱼,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "虎牙" in channel_name:
            group_name = "虎牙,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("「B站」"):
            group_name = "B站,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.startswith("解说"):
            group_name = "解说,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "电影" in channel_name:
            group_name = "电影,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif "电视剧" in channel_name:
            group_name = "电视剧,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        elif channel_name.endswith("广播"):
            group_name = "广播,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))
        else:
            group_name = "其他,#genre#"
            if group_name not in channel:
                channel[group_name] = []
            for idx, addr in enumerate(channel_addresses, 1):
                addr_with_line = f"{addr}$线路{idx}"
                channel[group_name].append((f"{channel_name},{addr_with_line}", utils.is_ipv6(addr)))


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
        else:
            channel[group] = utils.sort_channels(group_lines)
            channel_ipv6[group] = utils.sort_channels_ipv6(group_lines)


def save_to_file(output_file, others_file):
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(output_file, 'w', encoding='utf-8') as f:
            for group in channel:
                group_lines = channel[group]
                if len(group_lines) == 0:
                    continue
                f.write(group + '\n')
                for line in group_lines:
                    line_entry = line[0] if isinstance(line, tuple) else line
                    f.write(f"{line_entry}\n")
                f.write('\n')

            for group in channel_ipv6:
                group_lines = channel_ipv6[group]
                if len(group_lines) == 0:
                    continue
                f.write(group + '\n')
                for line in group_lines:
                    line_entry = line[0] if isinstance(line, tuple) else line
                    f.write(f"{line_entry}\n")
                f.write('\n')
            f.write(f"更新时间: {current_time},#genre#\n")
            f.write(f"最后更新时间: {current_time}\n")
        print(f"合并后的文本已保存到文件: {output_file}")

        with open(others_file, 'w', encoding='utf-8') as f:
            f.write("其他,#genre#\n")
            for line in channel.get("其他,#genre#", []):
                line_entry = line[0] if isinstance(line, tuple) else line
                f.write(f"{line_entry}\n")
            print(f"已保存到文件: {others_file}")

    except Exception as e:
        print(f"保存文件时发生错误：{e}")


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

    copy_utils.cpoy_file(output_file, other_file, 30)
    copy_utils.copy_source_2_target(output_file, "../local.txt")
    trans_utils.trans2m3u(output_file)
