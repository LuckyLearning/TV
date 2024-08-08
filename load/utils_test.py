import cv2
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

# 函数：获取视频分辨率
def get_video_resolution(video_path, timeout=13):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return (width, height)

# 函数：处理每一行
def process_line(line, order_list, valid_count, invalid_count, total_lines):
    parts = line.strip().split(',')
    if '#genre#' in line:
        # 如果行包含 '#genre#'，直接写入新文件
        return line, None, None
    elif len(parts) == 2:
        channel_name, channel_url = parts
        resolution = get_video_resolution(channel_url, timeout=5)
        if resolution and resolution[1] >= 540:  # 检查分辨率是否大于等于720p
            order_list.append((channel_name, resolution[1], channel_url))
            valid_count[0] += 1
            return f"{channel_name}[{resolution[1]}p],{channel_url}\n", channel_name, resolution[1]
        else:
            invalid_count[0] += 1
    return None, None, None

# 主函数
def main(source_file_path, output_file_path):
    order_list = []
    valid_count = [0]
    invalid_count = [0]
    task_queue = Queue()

    # 读取源文件
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        lines = source_file.readlines()

    total_lines = len(lines)

    with open(output_file_path + '.txt', 'w', encoding='utf-8') as output_file:
        # 创建线程池
        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = [executor.submit(process_line, line, order_list, valid_count, invalid_count, total_lines) for line in lines]

            for future in as_completed(futures):
                result, channel_name, resolution = future.result()
                if result:
                    output_file.write(result)
                    if channel_name and resolution:
                        print(f"Channel '{channel_name}' accepted with resolution {resolution}p.")
                print(f"有效: {valid_count[0]}, 无效: {invalid_count[0]}, 总数: {total_lines}, 进度: {(valid_count[0] + invalid_count[0]) / total_lines * 100:.2f}%")

    with open(output_file_path + '.txt', 'r', encoding='utf-8') as output_file:
        lines = output_file.readlines()
        for line in lines:
            print(line)

    print(f"任务完成，有效频道数：{valid_count[0]}, 无效频道数：{invalid_count[0]}, 总频道数：{total_lines}")

if __name__ == "__main__":
    source_file_path = 'merged_output.txt'  # 替换为你的源文件路径
    output_file_path = 'merged_output-有效源'  # 替换为你的输出文件路径
    main(source_file_path, output_file_path)
