import time
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0  # 从起点到当前节点的代价
        self.h = 0  # 到终点的估计代价
        self.f = 0  # f = g + h
        self.parent = None  # 父节点

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

def heuristic(node, goal):
    # 曼哈顿距离
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def astar(maze, start, goal):
    open_list = []
    closed_list = set()

    open_list.append(start)

    while open_list:
        # 找到f值最小的节点
        current = min(open_list, key=lambda x: x.f)
        open_list.remove(current)
        closed_list.add((current.x, current.y))

        # 到达目标
        if current.x == goal.x and current.y == goal.y:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            path.reverse()
            return path
        
        # 查看邻居
        for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x, y = current.x + i, current.y + j

            if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != 1 and (x, y) not in closed_list:
                neighbor = Node(x, y)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

                # 如果邻居在open_list中，检查其g值
                if any(neighbor.x == node.x and neighbor.y == node.y for node in open_list):
                    continue

                open_list.append(neighbor)

    return None

def generate_maze(rows, cols):
    """ 使用深度优先搜索生成迷宫 """
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    def carve_passages(x, y):
        maze[x][y] = 0  # 将当前单元格设置为通路
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]  # 可能的移动方向 (x, y)
        random.shuffle(directions)  # 打乱方向顺序，增加随机性
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:  # 确保新单元格在迷宫范围内且未被访问
                maze[x + dx // 2][y + dy // 2] = 0  # 打通当前单元格与新单元格之间的墙壁
                carve_passages(nx, ny)  # 递归访问新单元格

    carve_passages(1, 1)  # 从 (1,1) 开始生成迷宫
    maze[0][1] = 0  # 保证入口
    maze[rows - 1][cols - 2] = 0  # 保证出口
    return maze

# 测试
rows, cols = 31, 31  # 行和列的数量为奇数，以便墙壁可以被正确放置
maze = generate_maze(rows, cols)

start = Node(1, 1)
goal = Node(rows - 2, cols - 2)

# 打印生成的迷宫
print("生成的迷宫：")
for row in maze:
    print(" ".join(str(cell) for cell in row))
    
time.sleep(100)
path = astar(maze, start, goal)
if path:
    print("路径找到：", path)
    # 可视化路径
    plt.imshow(maze, cmap=plt.cm.binary)
    for step in path:
        plt.plot(step[1], step[0], 'ro')  # 在路径上绘制红点
    plt.show()
else:
    print("无法找到路径。")
