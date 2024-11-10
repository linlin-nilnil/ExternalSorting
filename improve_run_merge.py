import os
import random
import time
import pandas as pd


# 1. 随机生成初始数据文件 data.txt
def generate_initial_data(filename, num_records):
    with open(filename, 'w') as f:
        for _ in range(num_records):
            f.write(str(random.randint(1, 1000000)) + '\n')
    print(f"生成初始数据文件：{filename}")


# 2. 顺串生成：将数据分割成多个顺序文件
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


# 3. 败者树：优化k路顺串归并
class LoserTree:
    def __init__(self, k):
        self.k = k
        self.tree = [None] * (2 * k - 1)  # 败者树的数组表示
        self.current = [None] * k  # 当前候选最小值的索引
        self.iterators = [None] * k  # 每个顺串的迭代器
        self.build()

    def build(self):
        for i in range(self.k):
            self.tree[self.k - 1 + i] = None  # 初始化叶子节点为 None
        for i in range(self.k - 2, -1, -1):
            self.tree[i] = None

    def add_runs(self, runs):
        # 给每个顺串分配一个迭代器
        self.iterators = [iter(run) for run in runs]
        for i in range(self.k):
            try:
                val = next(self.iterators[i])
                self.current[i] = val
            except StopIteration:
                self.current[i] = None
        self.build()

    def find_winner(self):
        for i in range(self.k - 2, -1, -1):
            # 比较左子树和右子树的胜者，找出最小值
            left = self.tree[2 * i + 1]
            right = self.tree[2 * i + 2]
            if left is None or (right is not None and left > right):
                self.tree[i] = right
            else:
                self.tree[i] = left
        return self.tree[0]


# 4. k路顺串归并：使用败者树优化归并过程
def merge_runs_with_loser_tree(runs, output_filename, k):
    loser_tree = LoserTree(k)
    loser_tree.add_runs(runs)

    with open(output_filename, 'w') as f:
        while True:
            winner = loser_tree.find_winner()  # 找出最小值
            if winner is None:
                break
            f.write(str(winner) + '\n')

            # 更新败者树中的元素
            for i in range(k):
                if loser_tree.current[i] == winner:
                    try:
                        new_val = next(loser_tree.iterators[i])
                        loser_tree.current[i] = new_val
                    except StopIteration:
                        loser_tree.current[i] = None
                    break

    print(f"归并后的数据已保存至：{output_filename}")


# 5. 性能比较：比较不同k值、内存大小和文件大小对性能的影响
def compare_performance(input_filename, run_size, output_filename, k):
    print(f"当前使用的k值：{k}")  # 打印出当前的k值

    start_time = time.time()

    # 生成顺串
    runs = generate_runs(input_filename, run_size)

    # 使用败者树进行k路顺串归并
    merge_runs_with_loser_tree(runs, output_filename, k)

    end_time = time.time()
    duration = end_time - start_time
    print(f"排序和归并操作完成，耗时：{duration:.4f}秒")
    return duration


# 6. 打印重要参数并保存到Excel
def print_stats(input_filename, run_size, output_filename, k, duration):
    file_size = os.path.getsize(input_filename) / (1024 * 1024)  # MB
    num_records = sum(1 for line in open(input_filename))  # 统计记录数
    num_runs = num_records // run_size + (1 if num_records % run_size else 0)  # 顺串数量

    print(f"文件 {input_filename} 大小: {file_size:.2f} MB")
    print(f"总记录数: {num_records}")
    print(f"顺串数量: {num_runs}")
    print(f"每个顺串的最大长度: {run_size}")

    return {
        "k值": k,
        "文件大小 (MB)": file_size,
        "总记录数": num_records,
        "顺串数量": num_runs,
        "每个顺串的最大长度": run_size,
        "排序和归并耗时 (秒)": duration
    }


def main():
    input_filename = "data.txt"
    output_filename = "sorted_data.txt"
    num_records = 100000  # 初始数据量
    run_size = 1000  # 每个顺串的最大长度
    generate_initial_data(input_filename, num_records)

    results = []  # 存储所有结果以保存到Excel

    # 进行不同k值的测试
    for k in range(3, 21):
        duration = compare_performance(input_filename, run_size, output_filename, k)
        stats = print_stats(input_filename, run_size, output_filename, k, duration)
        results.append(stats)  # 将结果添加到列表

    # 将所有结果保存到Excel文件
    df = pd.DataFrame(results)
    df.to_excel("results.xlsx", index=False)
    print("所有结果已保存至 result.xlsx 文件")


if __name__ == "__main__":
    main()
