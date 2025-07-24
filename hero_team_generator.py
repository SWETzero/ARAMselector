#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from math import ceil

def load_heroes(filename="heroes_ranking.json"):
    """从JSON文件加载英雄数据"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            heroes = json.load(f)
        return heroes
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filename}")
        print("请先运行 hero_input.py 创建英雄排名文件")
        return None
    except json.JSONDecodeError:
        print(f"错误: {filename} 文件格式不正确")
        return None

def divide_heroes_into_tiers(heroes):
    """将英雄按排名分为T1-T5等级"""
    total_heroes = len(heroes)
    if total_heroes < 10:
        print(f"警告: 英雄数量不足({total_heroes}个)，建议至少10个英雄")
    
    # 计算每个等级的英雄数量
    base_count = total_heroes // 5
    remainder = total_heroes % 5
    
    tiers = {}
    start_idx = 0
    
    for tier in range(1, 6):
        # T5包含余数部分
        count = base_count + (1 if tier == 5 and remainder > 0 else 0)
        if tier <= remainder and tier < 5:
            count += 1
            
        end_idx = start_idx + count
        tiers[f"T{tier}"] = heroes[start_idx:end_idx]
        start_idx = end_idx
    
    return tiers

def select_team_from_tiers(tiers, team_name):
    """从每个等级随机选择2个英雄组成队伍"""
    team = []
    
    print(f"\n{team_name}队选择过程:")
    for tier_name, tier_heroes in tiers.items():
        if len(tier_heroes) == 0:
            continue
            
        # 从当前等级随机选择2个英雄（如果该等级英雄数量不足2个，则全选）
        select_count = min(2, len(tier_heroes))
        selected = random.sample(tier_heroes, select_count)
        
        team.extend(selected)
        
        hero_names = [hero["name"] for hero in selected]
        print(f"  {tier_name}: {', '.join(hero_names)}")
    
    return team

def print_team_summary(team, team_name):
    """打印队伍总结"""
    print(f"\n{team_name}队最终阵容:")
    print("-" * 20)
    for i, hero in enumerate(team, 1):
        print(f"{i}. {hero['name']} (原排名: {hero['rank']})")

def ban_heroes(heroes):
    """ban英雄环节，最多ban 10个英雄"""
    print("\nBan英雄环节")
    print("=" * 20)
    print("最多可以ban 10个英雄")
    print("输入英雄名字进行ban，输入'done'结束ban选环节")
    print("可用英雄列表:")
    
    # 显示所有可用英雄
    for i, hero in enumerate(heroes, 1):
        print(f"{i}. {hero['name']}")
    
    banned_heroes = []
    available_heroes = heroes.copy()
    
    while len(banned_heroes) < 10:
        ban_input = input(f"\n请输入要ban的英雄名字 ({len(banned_heroes)}/10): ").strip()
        
        if ban_input.lower() == "done":
            break
        
        if not ban_input:
            continue
        
        # 查找要ban的英雄
        found_hero = None
        for hero in available_heroes:
            if hero['name'] == ban_input:
                found_hero = hero
                break
        
        if found_hero:
            banned_heroes.append(found_hero)
            available_heroes.remove(found_hero)
            print(f"已ban: {found_hero['name']} (原排名: {found_hero['rank']})")
            
            if len(banned_heroes) == 10:
                print("已达到最大ban数量(10个)")
                break
        else:
            print(f"未找到英雄: {ban_input}")
            print("请检查英雄名字是否正确")
    
    if banned_heroes:
        print(f"\n本局ban掉的英雄 ({len(banned_heroes)}个):")
        for hero in banned_heroes:
            print(f"- {hero['name']} (原排名: {hero['rank']})")
    else:
        print("\n没有ban任何英雄")
    
    return available_heroes, banned_heroes

def main():
    print("英雄队伍生成器")
    print("=" * 30)
    
    # 加载英雄数据
    heroes = load_heroes()
    if not heroes:
        return
    
    print(f"成功加载 {len(heroes)} 个英雄")
    
    # Ban英雄环节
    available_heroes, banned_heroes = ban_heroes(heroes)
    
    if len(available_heroes) < 10:
        print(f"\n警告: 剩余英雄数量不足({len(available_heroes)}个)，建议至少10个英雄用于组队")
        if len(available_heroes) == 0:
            print("没有可用英雄，程序结束")
            return
    
    print(f"\n剩余可用英雄: {len(available_heroes)} 个")
    
    # 按排名分为T1-T5等级（使用ban后的可用英雄）
    tiers = divide_heroes_into_tiers(available_heroes)
    
    print("\n英雄等级分配:")
    for tier_name, tier_heroes in tiers.items():
        hero_names = [hero["name"] for hero in tier_heroes]
        print(f"{tier_name}: {len(tier_heroes)}个英雄 - {', '.join(hero_names)}")
    
    # 生成红色队和蓝色队
    red_team = select_team_from_tiers(tiers, "红色")
    blue_team = select_team_from_tiers(tiers, "蓝色")
    
    # 打印最终结果
    print("\n" + "=" * 50)
    print_team_summary(red_team, "红色")
    print_team_summary(blue_team, "蓝色")
    
    print(f"\n红色队总计: {len(red_team)} 个英雄")
    print(f"蓝色队总计: {len(blue_team)} 个英雄")

if __name__ == "__main__":
    main()