import os
import random
import heapq
import time
from tabulate import tabulate
import pandas as pd

# 全局变量，用于统计I/O次数
io_count = 0
block_size = 4096  # 设置块大小，一次性读写4096行

# 1. 随机生成初始数据文件 data.txt
def generate_initial_data(filename, num_records):
    global io_count
    with open(filename, 'w') as f:
        buffer = []
        for _ in range(num_records):
            buffer.append(str(random.randint(1, 1000000)) + '\n')
            if len(buffer) >= block_size:
                f.writelines(buffer)
                buffer = []
                io_count += 1
        if buffer:
            f.writelines(buffer)
            io_count += 1
    print(f"生成初始数据文件：{filename}")

# 3. 顺串归并：使用归并排序进行顺串归并，生成最终排好序的数据文件sorted_data.txt
def merge_runs_with_loser_tree(runs, output_filename):
    global io_count
    with open(output_filename, 'w') as f:
        heap = []
        iterators = [iter(run) for run in runs]

        for i, it in enumerate(iterators):
            first_val = next(it, None)
            if first_val is not None:
                heapq.heappush(heap, (first_val, i))

        buffer = []
        while heap:
            val, run_index = heapq.heappop(heap)
            buffer.append(str(val) + '\n')
            if len(buffer) >= block_size:
                f.writelines(buffer)
                buffer = []
                io_count += 1

            next_val = next(iterators[run_index], None)
            if next_val is not None:
                heapq.heappush(heap, (next_val, run_index))
        if buffer:
            f.writelines(buffer)
            io_count += 1
    print(f"归并后的数据已保存至：{output_filename}")

# 2. 生成顺串
def generate_runs(input_filename, run_size):
    global io_count
    runs = []
    with open(input_filename, 'r') as f:
        numbers = []
        while True:
            lines = f.readlines(block_size)
            if not lines:
                break
            io_count += 1

            for line in lines:
                numbers.append(int(line.strip()))
                if len(numbers) == run_size:
                    runs.append(sorted(numbers))
                    numbers = []
        if numbers:
            runs.append(sorted(numbers))
    print(f"生成顺串，共 {len(runs)} 个顺串，每个顺串最大长度为 {run_size}")
    return runs

# 4. 性能比较
def compare_performance(input_filename, run_size, output_filename):
    start_time = time.time()

    # 生成顺串
    runs = generate_runs(input_filename, run_size)

    # 使用最小败者树进行顺串归并
    merge_runs_with_loser_tree(runs, output_filename)

    end_time = time.time()
    duration = end_time - start_time
    return duration

def main():
    input_filename = "data.txt"
    output_filename = "sorted_data.txt"

    # 存储表格数据
    table_data = [["总记录数", "顺串数量", "顺串最大长度", "外存I/O操作次数", "耗时 (秒)"]]

    for num_record in range(100000, 1100000, 100000):
        run_size = 1000  # 最大顺串长度
        generate_initial_data(input_filename, num_record)

        global io_count
        io_count = 0
        duration = compare_performance(input_filename, run_size, output_filename)

        num_records = sum(1 for line in open(input_filename))
        num_runs = num_records // run_size + (1 if num_records % run_size else 0)
        table_data.append([num_record, num_runs, run_size, io_count, duration])

    for run_size in range(1000, 11000, 1000):
        num_record = 100000  # 初始数据量
        generate_initial_data(input_filename, num_record)

        io_count = 0
        duration = compare_performance(input_filename, run_size, output_filename)

        num_records = sum(1 for line in open(input_filename))
        num_runs = num_records // run_size + (1 if num_records % run_size else 0)
        table_data.append([num_record, num_runs, run_size, io_count, duration])

    # 输出表格
    print(tabulate(table_data, headers="firstrow", tablefmt="grid", floatfmt=".4f"))

    # 将表格数据保存为Excel文件
    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # 排除表头行
    df.to_excel("results.xlsx", index=False)
    print("表格数据已保存到Excel文件：results.xlsx")

if __name__ == '__main__':
    main()

