import subprocess
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 函数：使用 ffprobe 获取视频分辨率
def get_video_resolution_ffprobe(channel_name, video_path, timeout=13):
    try:
        # 调用 ffprobe 获取视频信息
        command = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'json', video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=True)
        info = json.loads(result.stdout)

        if 'streams' in info and len(info['streams']) > 0:
            width = info['streams'][0]['width']
            height = info['streams'][0]['height']
            return (width, height), False
        return None, True
    except subprocess.CalledProcessError as e:
        print(f"Channel '{channel_name}'-'{video_path}'\nError while processing video with ffprobe: {e}")
        return None, True
    except subprocess.TimeoutExpired:
        print(f"Channel '{channel_name}'-'{video_path}'\nTimeout while processing video with ffprobe.")
        return None, True

# 函数：处理每一行
def process_line(line):
    parts = line.strip().split(',')
    if '#genre#' in line:
        # 如果行包含 '#genre#'，直接写入新文件
        return line, None, None, False
    elif len(parts) == 2:
        channel_name, channel_url = parts

        resolution, timeout = get_video_resolution_ffprobe(channel_name, channel_url, timeout=5)
        if timeout:
            return channel_url, channel_name, None, True
        elif resolution and resolution[1] > 720:  # 检查分辨率是否大于720p
            return f"{channel_name}[{resolution[1]}p],{channel_url}\n", channel_name, resolution[1], False
        else:
            return f"Channel '{channel_name}' has resolution {resolution[1]}p which is less than 720p.\n", channel_name, resolution[1], False
    return None, None, None, False

# 主函数
def main(source_file_path, output_file_path, max_workers=8):
    order_list = []
    valid_count = [0]
    invalid_count = [0]

    # 读取源文件
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        lines = source_file.readlines()

    total_lines = len(lines)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_line, line) for line in lines]

        with open(output_file_path + '.txt', 'w', encoding='utf-8') as output_file:
            for future in as_completed(futures):
                result, channel_name, resolution, timeout = future.result()
                if timeout:
                    print(f"Channel '{channel_name}-{result}' connection timed out or URL is invalid.")
                    invalid_count[0] += 1
                elif result:
                    if resolution and resolution > 720:
                        output_file.write(result)
                        print(f"Channel '{channel_name}'-'{result}' accepted with resolution {resolution}p.")
                        valid_count[0] += 1
                    else:
                        print(result)  # 打印分辨率小于720p的提示信息
                print(f"有效: {valid_count[0]}, 无效: {invalid_count[0]}, 总数: {total_lines}, 进度: {(valid_count[0] + invalid_count[0]) / total_lines * 100:.2f}%")

    # 全量打印结果
    with open(output_file_path + '.txt', 'r', encoding='utf-8') as output_file:
        all_lines = output_file.readlines()
        print("\n--- 全部结果 ---")
        for line in all_lines:
            print(line.strip())

    print(f"任务完成，有效频道数：{valid_count[0]}, 无效频道数：{invalid_count[0]}, 总频道数：{total_lines}")

if __name__ == "__main__":
    # 总耗时
    start_time = time.time()
    source_file_path = 'merge_ipv6.txt'  # 替换为你的源文件路径
    output_file_path = '有效源'  # 替换为你的输出文件路径
    main(source_file_path, output_file_path, 4)
    end_time = time.time()
    print(f"总耗时：{end_time - start_time}秒")
