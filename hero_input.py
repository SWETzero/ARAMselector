#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def main():
    heroes = []
    rank = 1
    
    print("英雄排名输入器")
    print("请逐个输入英雄名字，按回车确认")
    print("输入 'end' 结束输入并保存")
    print("-" * 30)
    
    while True:
        hero_name = input(f"请输入第{rank}名英雄: ").strip()
        
        if hero_name.lower() == "end":
            break
            
        if hero_name:  # 确保输入不为空
            heroes.append({
                "name": hero_name,
                "rank": rank
            })
            print(f"已添加: {hero_name} (排名: {rank})")
            rank += 1
        else:
            print("英雄名字不能为空，请重新输入")
    
    if heroes:
        # 保存到JSON文件
        with open("heroes_ranking.json", "w", encoding="utf-8") as f:
            json.dump(heroes, f, ensure_ascii=False, indent=2)
        
        print(f"\n成功保存 {len(heroes)} 个英雄到 heroes_ranking.json")
        print("\n最终排名:")
        for hero in heroes:
            print(f"{hero['rank']}. {hero['name']}")
    else:
        print("没有输入任何英雄名字")

if __name__ == "__main__":
    main