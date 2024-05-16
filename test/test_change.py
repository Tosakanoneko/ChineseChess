import time
import copy

# 初始列表
list1 = [
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'b', '.', '.', '.', '.', '.', 'b', '.'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.', 'r'],
    ['.', 'r', '.', '.', '.', '.', '.', 'r', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']
]

list2 = [
    ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', 'p', '.', 'p', '.', 'p', '.', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', 'P', '.', 'P'],
    ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]


# 打印列表的函数
def print_list(lst):
    for row in lst:
        print(' '.join(row))
    print()

# 查找变化的函数
def find_changes(initial, current):
    changes = []
    for i in range(len(initial)):
        for j in range(len(initial[i])):
            if initial[i][j] != current[i][j]:
                changes.append(((i, j), initial[i][j], current[i][j]))
    return changes

# 打印变化的函数
def print_changes(changes):
    for change in changes:
        (i, j), old, new = change
        if old != '.' and new == '.':
            print(f"元素 '{old}' 从位置 ({i}, {j}) 移动了")
        elif old == '.' and new != '.':
            print(f"元素 '{new}' 出现在新位置 ({i}, {j})")

# 检查列表变化的函数
def check_list_changes():
    global last_steady_state
    stable_time = 5  # 稳定时间阈值，单位为秒
    check_interval = 1  # 检查间隔，单位为秒

    last_time = time.time()
    while True:
        time.sleep(check_interval)
        current_time = time.time()
        changes = find_changes(last_steady_state, list1)
        if changes:
            last_time = current_time
            print("列表发生变化:")
            print_changes(changes)
        elif current_time - last_time >= stable_time:
            print("达到新的稳态:")
            print_list(list1)
            last_steady_state = copy.deepcopy(list1)
            last_time = current_time

# 模拟 list1 的变化（此处仅为演示，实际应用中应替换为你的变化逻辑）
def simulate_changes():
    time.sleep(2)
    list1[2][1] = '.'
    list1[4][4] = 'b'
    time.sleep(2)
    list1[4][4] = '.'
    list1[5][5] = 'b'
    time.sleep(6)
    list1[5][5] = '.'
    list1[6][6] = 'b'

import threading
if __name__ == '__main__':
# 运行检测和模拟
    # 用于比较的初始稳态
    last_steady_state = copy.deepcopy(list1)

    t1 = threading.Thread(target=check_list_changes)
    t2 = threading.Thread(target=simulate_changes)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
