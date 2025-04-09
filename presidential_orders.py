import requests
from bs4 import BeautifulSoup

def fetch_latest_orders():
    """获取白宫网站上最新的总统令"""
    url = "https://trumpwhitehouse.archives.gov/presidential-actions/"  # 特朗普白宫存档页面
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("无法访问白宫网站。状态码：", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    orders = []

    # 调试：打印页面内容
    # print(response.text)

    # 查找总统令的标题和链接
    for item in soup.find_all("h2", class_="briefing-statement__title", limit=3):
        title = item.text.strip()
        link = item.find("a")["href"]
        orders.append({"title": title, "link": f"https://trumpwhitehouse.archives.gov{link}"})

    return orders

def main():
    print("获取特朗普最新的3条总统令...")
    orders = fetch_latest_orders()

    if not orders:
        print("未能获取到总统令。")
    else:
        print("\n最新的总统令：")
        for i, order in enumerate(orders, start=1):
            print(f"{i}. {order['title']}")
            print(f"   链接: {order['link']}")

if __name__ == "__main__":
    main()