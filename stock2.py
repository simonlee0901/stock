from flask import Flask, render_template, request, redirect
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def is_valid_move(board, row, col, num):
    """检查在指定位置放置数字是否有效"""
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True
#test

def generate_board():
    """生成一个数独棋盘"""
    board = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(20):  # 随机填充20个数字
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        while not is_valid_move(board, row, col, num) or board[row][col] != 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
        board[row][col] = num
    return board

def fetch_latest_orders():
    """获取白宫网站上最新的总统令"""
    url = "https://trumpwhitehouse.archives.gov/presidential-actions/"  # 特朗普白宫存档页面
    response = requests.get(url)
    
    if response.status_code != 200:
        print("无法访问白宫网站。状态码：", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    orders = []

    # 查找总统令的标题和链接
    for item in soup.find_all("h2", class_="briefing-statement__title", limit=3):
        title = item.text.strip()
        link = item.find("a")["href"]
        orders.append({"title": title, "link": f"https://trumpwhitehouse.archives.gov{link}"})

    return orders

# 初始化棋盘
board = generate_board()

@app.route("/", methods=["GET", "POST"])
def index():
    global board
    if request.method == "POST":
        try:
            row = int(request.form["row"]) - 1
            col = int(request.form["col"]) - 1
            num = int(request.form["num"])
            if is_valid_move(board, row, col, num):
                board[row][col] = num
            else:
                return render_template("index.html", board=board, error="无效的移动！")
        except ValueError:
            return render_template("index.html", board=board, error="输入格式错误！")
    return render_template("index.html", board=board, error=None)

if __name__ == "__main__":
    app.run(debug=True)