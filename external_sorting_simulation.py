import os
import random
import heapq
import time
from openpyxl import Workbook

# 初始化Excel工作簿和表格
workbook = Workbook()
sheet = workbook.active
sheet.title = "Results"
sheet.append(["记录数", "顺串最大长度", "文件大小 (MB)", "总记录数", "顺串数量", "耗时 (秒)"])

# 1. 随机生成初始数据文件data.txt
def generate_initial_data(filename, num_records):
    with open(filename, 'w') as f:
        for _ in range(num_records):
            f.write(str(random.randint(1, 1000000)) + '\n')
    print(f"生成初始数据文件：{filename}")

# 2. 顺串生成：将数据文件分割成多个顺序文件
def generate_runs(input_filename, run_size):
    runs = []
    with open(input_filename, 'r') as f:
        numbers = []
        for line in f:
            numbers.append(int(line.strip()))
            if len(numbers) == run_size:
                runs.append(sorted(numbers))  # 排序每个顺串
                numbers = []
        if numbers:
            runs.append(sorted(numbers))  # 最后一个顺串
    print(f"生成顺串，共 {len(runs)} 个顺串，每个顺串最大长度为 {run_size}")
    return runs

# 3. 顺串归并：2路归并，生成最终排好序的数据文件sorted_data.txt
def merge_runs(runs, output_filename):
    with open(output_filename, 'w') as f:
        # 使用堆来进行2路归并
        heap = []
        iterators = [iter(run) for run in runs]
        for i, it in enumerate(iterators):
            first_val = next(it, None)
            if first_val is not None:
                heapq.heappush(heap, (first_val, i))  # 推送第一个元素到堆中

        while heap:
            val, run_index = heapq.heappop(heap)
            f.write(str(val) + '\n')
            next_val = next(iterators[run_index], None)
            if next_val is not None:
                heapq.heappush(heap, (next_val, run_index))
    print(f"归并后的数据已保存至：{output_filename}")

# 4. 性能比较并保存结果到Excel
def compare_performance(input_filename, run_size, output_filename, num_records):
    start_time = time.time()

    # 生成顺串
    runs = generate_runs(input_filename, run_size)

    # 进行顺串归并
    merge_runs(runs, output_filename)

    end_time = time.time()
    duration = end_time - start_time
    print(f"排序和归并操作完成，耗时：{duration:.4f}秒")

    # 获取文件大小等统计信息
    file_size = os.path.getsize(input_filename) / (1024 * 1024)  # MB
    num_records = sum(1 for line in open(input_filename))  # 统计记录数
    num_runs = num_records // run_size + (1 if num_records % run_size else 0)  # 顺串数量

    # 将结果写入Excel
    sheet.append([num_records, run_size, file_size, num_records, num_runs, duration])

def main():
    input_filename = "data.txt"
    output_filename = "sorted_data.txt"

    for num_record in range(10000, 110000, 10000): # 初始数据量
        # 生成初始数据文件
        generate_initial_data(input_filename, num_record)
        # 性能比较和结果写入Excel
        run_size = 1000  # 每个顺串的最大长度
        compare_performance(input_filename, run_size, output_filename, num_record)

    for run_size in range(100, 1100, 100):  # 每个顺串的最大长度
        num_record = 100000  # 初始数据量
        # 生成初始数据文件
        generate_initial_data(input_filename, num_record)
        compare_performance(input_filename, run_size, output_filename, num_record)

    # 保存Excel文件
    workbook.save("results.xlsx")
    print("所有结果已保存到results.xlsx文件中")

if __name__ == '__main__':
    main()
