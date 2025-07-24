import requests
from bs4 import BeautifulSoup
import json
import re
import os

def fetch_and_save_html():
    """
    从OP.GG获取ARAM模式页面的HTML并保存到本地
    """
    url = "https://op.gg/zh-cn/lol/modes/aram"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        print(f"正在请求HTML页面: {url}...")
        response = requests.get(url, headers=headers)
        
        # 检查响应状态
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None
            
        # 保存HTML到文件
        with open("op_gg_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"已将HTML保存到 op_gg_response.html 文件中")
        
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def parse_html_and_extract_data(html_content=None):
    """
    解析HTML并提取英雄数据
    """
    if html_content is None:
        # 如果没有提供HTML内容，尝试从文件中读取
        try:
            with open("op_gg_response.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            print("从本地文件读取HTML内容")
        except Exception as e:
            print(f"读取本地HTML文件失败: {e}")
            return []
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 打印页面标题，确认我们获取到了正确的页面
    title = soup.title.text if soup.title else "无标题"
    print(f"页面标题: {title}")
    
    # 查找所有英雄名称
    champions_data = []
    rank = 1
    
    # 查找所有英雄名称元素
    name_elements = soup.find_all("strong", class_="flex-1 overflow-hidden text-ellipsis whitespace-nowrap text-xs")
    
    print(f"找到 {len(name_elements)} 个英雄名称元素")
    
    for name_element in name_elements:
        try:
            # 提取英雄名称
            name = name_element.text.strip()
            
            # 查找胜率元素（同级下面的元素）
            win_rate_element = None
            current = name_element.parent
            
            # 向下查找包含胜率的元素
            win_rate_span = None
            pick_rate_span = None
            
            # 查找胜率和选用率
            td_elements = current.find_next_siblings("td")
            for td in td_elements:
                span = td.find("span", class_="text-xs text-gray-600")
                if span:
                    if not win_rate_span:
                        win_rate_span = span
                    elif not pick_rate_span:
                        pick_rate_span = span
                        break
            
            # 提取胜率和选用率
            win_rate = win_rate_span.text.strip() if win_rate_span else "未知"
            pick_rate = pick_rate_span.text.strip() if pick_rate_span else "未知"
            
            # 创建英雄数据字典
            champion_data = {
                'rank': rank,
                'name': name,
                'win_rate': win_rate,
                'pick_rate': pick_rate
            }
            
            champions_data.append(champion_data)
            print(f"已提取英雄: {name}, 排名: {rank}, 胜率: {win_rate}, 选用率: {pick_rate}")
            
            rank += 1
            
        except Exception as e:
            print(f"处理英雄数据时出错: {e}")
    
    # 如果没有找到英雄数据，尝试另一种方法
    if not champions_data:
        print("使用第一种方法未找到英雄数据，尝试另一种方法...")
        
        # 尝试查找表格行
        rows = soup.find_all("tr")
        for row in rows:
            try:
                # 查找英雄名称
                name_element = row.find("strong", class_="flex-1 overflow-hidden text-ellipsis whitespace-nowrap text-xs")
                if not name_element:
                    continue
                
                name = name_element.text.strip()
                
                # 查找所有包含百分比的span元素
                spans = row.find_all("span", class_="text-xs text-gray-600")
                
                if len(spans) >= 2:
                    win_rate = spans[0].text.strip()
                    pick_rate = spans[1].text.strip()
                    
                    champion_data = {
                        'rank': rank,
                        'name': name,
                        'win_rate': win_rate,
                        'pick_rate': pick_rate
                    }
                    
                    champions_data.append(champion_data)
                    print(f"已提取英雄: {name}, 排名: {rank}, 胜率: {win_rate}, 选用率: {pick_rate}")
                    
                    rank += 1
            except Exception as e:
                print(f"处理英雄数据时出错: {e}")
    
    return champions_data

def save_to_json(data, filename="aram_champions.json"):
    """
    将数据保存为JSON文件
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"数据已成功保存到 {filename}")
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

def main():
    print("开始爬取OP.GG ARAM模式英雄数据...")
    
    # 获取HTML内容
    html_content = fetch_and_save_html()
    
    # 解析HTML并提取数据
    champions_data = parse_html_and_extract_data(html_content)
    
    if champions_data:
        print(f"成功提取 {len(champions_data)} 个英雄的数据")
        save_to_json(champions_data)
    else:
        print("未提取到任何数据")
        print("尝试直接从已保存的HTML文件中提取数据...")
        champions_data = parse_html_and_extract_data()
        
        if champions_data:
            print(f"成功提取 {len(champions_data)} 个英雄的数据")
            save_to_json(champions_data)
        else:
            print("未能提取到任何数据")

if __name__ == "__main__":
    main()