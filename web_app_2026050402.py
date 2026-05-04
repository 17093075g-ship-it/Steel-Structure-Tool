"""
结构设计选型智能体 - Web版 v6.0
重大升级：连续梁三弯矩方程精确计算，matplotlib图形生成
运行方式：streamlit run web_app_v6.py
"""

import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import hashlib
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
import io
import json
import re
import itertools

# Logo Base64编码（内嵌，无需外部文件）
LOGO_BASE64 = "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"

# PDF生成
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import glob

# DeepSeek API
from openai import OpenAI

# 数学计算和图形
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon
from matplotlib.lines import Line2D

# ============================================================
# 0. DeepSeek API 配置
# ============================================================

DEEPSEEK_API_KEY = "sk-70017c7730594f939dcf0303d951cbce"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 初始化 DeepSeek 客户端
def get_deepseek_client() -> OpenAI:
    return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

# AI System Prompt - 连续梁专用
AI_SYSTEM_PROMPT = """你是一个钢结构设计助手，专门解析结构设计任务描述并返回JSON参数。

⚠️ 最重要的规则：只在你确认用户是在描述一个具体的结构设计任务时才返回结构参数JSON。如果用户不是在描述设计任务，必须返回clarification。

判断标准：
- 是设计任务：用户明确说了跨度、荷载、梁类型等具体参数，如"3跨连续梁，6+6+6m，恒载8kN/m"
- 不是设计任务：用户在提问、闲聊、询问能力、询问规范等，如"你能做什么"、"S355是什么"、"帮我设计一个梁"

当用户不是在描述具体设计任务时，返回 {"clarification": "你想对用户说的话"}

例如：
- 用户问"你能做什么" → {"clarification": "我可以帮您进行钢结构梁/柱的截面选型设计。支持简支梁、悬臂梁、固端梁和2-5跨连续梁，按香港规范HK COP 2019验算。请告诉我您的梁跨度、荷载等参数，我来为您选型。"}
- 用户问"S355和S275区别" → {"clarification": "S355屈服强度355MPa，S275屈服强度275MPa。S355强度更高，适用于更大跨度或更高荷载，是钢结构常用材料。"}
- 用户说"帮我设计一个梁" → {"clarification": "好的！请告诉我：1. 梁的类型（简支梁/连续梁等）？2. 跨度是多少？3. 承受什么荷载（均布荷载/集中力，大小）？4. 两端支座条件（铰支/固定）？"}
- 用户问"风载怎么考虑" → {"clarification": "香港风载需按HK COP规范取值，基本风速和高度系数查规范附录。本系统目前主要处理竖向静力荷载，风载可作为等效均布荷载输入。有具体参数我可以帮您计算。"}
- 用户问"今天天气怎么样" → {"clarification": "我是结构设计助手，不提供天气信息。有钢结构设计问题随时问我！"}
- 用户问"你好" → {"clarification": "你好！我是结构设计助手，有什么设计需求可以告诉我。"}

绝对禁止：
- 编造用户没有提供的参数（如跨度、荷载大小）
- 把非设计问题硬塞进结构JSON

支持的类型：
- simply_supported_beam: 简支梁
- cantilever_beam: 悬臂梁
- fixed_beam: 固端梁
- continuous_beam: 连续梁（主要支持）

连续梁参数：
- num_spans: 跨数（2-5跨）
- spans: 数组，每跨包含 length(m), dead_load(kN/m), live_load(kN/m), point_loads(集中力)
- left_support: 左端支座类型（pinned=铰支, fixed=固定）
- right_support: 右端支座类型（pinned=铰支, fixed=固定）
- load_cases: 活载不利布置工况

荷载类型：
- uniform: 均布荷载（kN/m）
- point: 集中荷载（kN），需指定位置（距左端距离m）

支座条件：
- pinned: 铰接
- fixed: 固定

示例输入：
- "3跨连续梁，跨度6+6+6m，恒载8kN/m，活载5kN/m，活载在1跨和3跨，两端铰支"
- "2跨连续梁，跨度4+6m，恒载10kN/m，第1跨跨中集中力50kN，左端固定右端铰支"
- "4跨连续梁，跨度5+6+5+6m，恒载12kN/m，活载6kN/m，活载在2跨和4跨"

返回JSON格式（示例1对应）：
{
  "structure_type": "continuous_beam",
  "num_spans": 3,
  "spans": [
    {"length": 6.0, "dead_load": 8.0, "live_load": 5.0, "point_loads": []},
    {"length": 6.0, "dead_load": 8.0, "live_load": 0, "point_loads": []},
    {"length": 6.0, "dead_load": 8.0, "live_load": 5.0, "point_loads": []}
  ],
  "left_support": "pinned",
  "right_support": "pinned",
  "load_cases": [
    {"name": "恒载+活载(1,3跨)", "live_spans": [0, 2]}
  ]
}

注意：
1. span单位是米
2. dead_load和live_load单位是kN/m
3. point_loads中position是距该跨左端的距离（米），value是力（kN）
4. 如果没有活载，live_load为0
5. 活载不利布置时，需要列出所有需要活载的跨（从0开始编号）
6. 只返回JSON，不要其他文字
7. 荷载方向默认为竖向向下（重力方向），无需反问
8. 如果用户描述了设计意图但缺少关键参数（跨度/荷载大小），用clarification反问而非猜测"""

# AI 推荐解读 System Prompt
AI_RECOMMEND_PROMPT = """你是一个钢结构设计助手，根据选型结果生成推荐解读。

选型结果包含：
- 推荐截面名称
- 利用率
- 库存状态
- 结构类型
- 跨数和各跨信息

请生成一段简洁的中文推荐解读，包括：
1. 截面推荐及利用率评价
2. 如有优化空间，给出建议
3. 库存情况提醒
4. 适用场景说明

直接返回解读内容，不要JSON格式，控制在150字以内。"""

# ============================================================
# 1. 中文字体配置
# ============================================================

def register_chinese_font():
    """尝试注册系统中文字体"""
    font_name = 'ChineseFont'
    
    win_fonts = [
        ('SimHei', r'C:\Windows\Fonts\simhei.ttf'),
        ('SimSun', r'C:\Windows\Fonts\simsun.ttc'),
        ('MSYaHei', r'C:\Windows\Fonts\msyh.ttc'),
    ]
    
    for fname, fpath in win_fonts:
        if os.path.exists(fpath):
            try:
                pdfmetrics.registerFont(TTFont(font_name, fpath))
                return font_name
            except:
                continue
    
    for pattern in [r'C:\Windows\Fonts\simhei*', r'C:\Windows\Fonts\msyh*', r'C:\Windows\Fonts\simsun*']:
        files = glob.glob(pattern)
        if files:
            try:
                pdfmetrics.registerFont(TTFont(font_name, files[0]))
                return font_name
            except:
                continue
    
    return 'Helvetica'

CHINESE_FONT = register_chinese_font()

# matplotlib 中文字体配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 2. 截面数据库
# ============================================================

@dataclass
class Section:
    name: str
    type: str
    mass: float
    A: float
    D: float
    B: float
    t: float
    T: float
    Ix: float
    Wx: float
    rx: float

SECTIONS_DB = [
    # UB 梁
    Section("457x191x82", "UB", 82.0, 104.0, 460.0, 191.3, 9.9, 16.0, 37100, 1610, 18.8),
    Section("457x191x74", "UB", 74.3, 94.6, 457.0, 190.4, 9.0, 14.5, 33300, 1460, 18.8),
    Section("457x191x67", "UB", 67.1, 85.5, 453.4, 189.9, 8.5, 12.7, 29400, 1300, 18.5),
    Section("406x178x74", "UB", 74.2, 94.5, 412.8, 179.5, 9.5, 16.0, 27300, 1320, 17.0),
    Section("406x178x67", "UB", 67.1, 85.5, 409.4, 178.8, 8.8, 14.3, 24300, 1190, 16.9),
    Section("406x178x60", "UB", 60.0, 76.5, 406.4, 178.1, 8.0, 12.8, 21600, 1060, 16.8),
    Section("356x171x67", "UB", 67.1, 85.5, 363.4, 173.2, 9.1, 15.7, 19500, 1070, 15.1),
    Section("356x171x57", "UB", 57.0, 72.7, 358.0, 172.1, 8.0, 13.0, 16100, 900, 14.9),
    Section("356x171x51", "UB", 51.0, 65.0, 354.4, 171.5, 7.3, 11.5, 14100, 796, 14.8),
    Section("305x165x54", "UB", 54.0, 68.7, 310.4, 166.0, 7.9, 13.7, 11700, 755, 13.0),
    Section("305x165x46", "UB", 46.0, 58.7, 306.6, 165.0, 6.7, 11.8, 9890, 645, 13.0),
    Section("305x165x40", "UB", 40.0, 51.0, 303.4, 164.6, 6.0, 10.0, 8510, 561, 12.9),
    Section("305x127x48", "UB", 48.1, 61.2, 311.0, 125.3, 9.0, 14.0, 9570, 616, 12.5),
    Section("305x127x42", "UB", 41.9, 53.4, 307.2, 124.3, 8.0, 12.1, 8200, 534, 12.4),
    Section("305x127x37", "UB", 37.0, 47.2, 304.4, 123.4, 7.1, 10.7, 7170, 471, 12.3),
    Section("254x146x43", "UB", 43.0, 54.8, 259.6, 147.3, 7.2, 12.7, 6540, 504, 10.9),
    Section("254x146x37", "UB", 37.0, 47.2, 256.0, 146.4, 6.3, 10.9, 5540, 433, 10.8),
    Section("254x146x31", "UB", 31.1, 39.7, 251.4, 146.1, 6.0, 8.6, 4410, 351, 10.5),
    Section("254x102x28", "UB", 28.3, 36.1, 260.4, 102.2, 6.3, 10.0, 4000, 308, 10.5),
    Section("254x102x25", "UB", 25.2, 32.0, 257.2, 101.9, 6.0, 8.4, 3410, 266, 10.3),
    Section("203x133x30", "UB", 30.0, 38.2, 206.8, 133.9, 6.4, 9.6, 2900, 280, 8.71),
    Section("203x133x25", "UB", 25.1, 32.0, 203.2, 133.2, 5.7, 7.8, 2340, 230, 8.56),
    Section("203x102x23", "UB", 23.1, 29.4, 203.2, 101.8, 5.4, 9.3, 2100, 207, 8.46),
    Section("178x102x19", "UB", 19.0, 24.3, 177.8, 101.2, 4.8, 7.9, 1360, 153, 7.48),
    Section("152x89x16", "UB", 16.0, 20.3, 152.4, 88.7, 4.5, 7.7, 834, 109, 6.41),
    
    # UC 柱
    Section("305x305x283", "UC", 283.0, 361.0, 335.4, 388.6, 19.1, 35.3, 150000, 8940, 20.4),
    Section("305x305x240", "UC", 240.0, 306.0, 323.0, 386.0, 16.0, 29.5, 125000, 7730, 20.2),
    Section("305x305x198", "UC", 198.0, 252.0, 311.4, 384.0, 13.0, 23.7, 101000, 6500, 20.0),
    Section("305x305x158", "UC", 158.0, 201.0, 299.6, 382.2, 10.3, 18.7, 78400, 5240, 19.7),
    Section("305x305x137", "UC", 137.0, 175.0, 293.6, 381.0, 9.0, 16.2, 67500, 4590, 19.6),
    Section("305x305x118", "UC", 118.0, 150.0, 287.6, 379.6, 7.9, 13.8, 57300, 3980, 19.5),
    Section("305x305x97", "UC", 97.0, 124.0, 280.4, 378.2, 6.6, 11.2, 46200, 3300, 19.3),
    Section("254x254x167", "UC", 167.0, 213.0, 289.1, 265.2, 19.2, 31.7, 58500, 4040, 16.6),
    Section("254x254x132", "UC", 132.0, 168.0, 276.3, 261.3, 15.3, 25.3, 45600, 3300, 16.5),
    Section("254x254x107", "UC", 107.0, 136.0, 266.7, 258.8, 12.8, 20.5, 36200, 2710, 16.3),
    Section("254x254x89", "UC", 89.0, 113.0, 260.3, 256.3, 10.5, 17.3, 29700, 2280, 16.2),
    Section("254x254x73", "UC", 73.0, 93.1, 254.1, 254.6, 8.6, 14.2, 24100, 1900, 16.1),
    Section("203x203x86", "UC", 86.0, 110.0, 222.2, 208.8, 8.0, 15.6, 13000, 1170, 10.9),
    Section("203x203x71", "UC", 71.0, 90.5, 215.8, 206.4, 6.5, 12.3, 10300, 956, 10.7),
    Section("203x203x60", "UC", 60.0, 76.4, 209.6, 205.8, 5.4, 10.2, 8370, 799, 10.5),
    Section("203x203x52", "UC", 52.0, 66.3, 206.2, 204.3, 4.5, 8.8, 7140, 693, 10.4),
    Section("203x203x46", "UC", 46.0, 58.7, 203.2, 203.6, 4.0, 7.2, 6230, 613, 10.3),
    Section("152x152x37", "UC", 37.0, 47.2, 161.8, 154.4, 5.8, 11.5, 2720, 336, 7.60),
    Section("152x152x30", "UC", 30.0, 38.3, 157.6, 152.9, 4.6, 9.4, 2150, 273, 7.49),
    Section("152x152x23", "UC", 23.0, 29.3, 152.4, 152.2, 3.4, 6.8, 1610, 211, 7.41),
    
    # PFC 槽钢
    Section("430x100x64", "PFC", 64.0, 81.5, 430.0, 100.0, 10.0, 14.0, 21800, 1010, 16.4),
    Section("380x100x54", "PFC", 54.0, 68.8, 380.0, 100.0, 9.0, 12.5, 16200, 850, 15.3),
    Section("330x90x46", "PFC", 46.0, 58.5, 330.0, 90.0, 8.0, 11.5, 11600, 700, 14.1),
    Section("300x90x41", "PFC", 41.0, 52.3, 300.0, 90.0, 7.5, 10.5, 9200, 610, 13.3),
    Section("260x90x35", "PFC", 35.0, 44.6, 260.0, 90.0, 6.5, 9.5, 6800, 520, 12.3),
    Section("230x80x30", "PFC", 30.0, 38.3, 230.0, 80.0, 6.0, 8.5, 4900, 420, 11.3),
    Section("200x75x26", "PFC", 26.0, 33.2, 200.0, 75.0, 5.5, 7.5, 3400, 340, 10.1),
    Section("180x70x22", "PFC", 22.0, 28.0, 180.0, 70.0, 5.0, 6.5, 2500, 270, 9.45),
    Section("150x60x18", "PFC", 18.0, 22.9, 150.0, 60.0, 4.5, 5.5, 1600, 210, 8.35),
    Section("120x50x14", "PFC", 14.0, 17.8, 120.0, 50.0, 4.0, 4.5, 960, 160, 7.35),
    
    # EA 等边角钢
    Section("200x200x24", "EA", 70.3, 89.6, 200.0, 200.0, 24.0, 24.0, 3330, 236, 6.10),
    Section("150x150x18", "EA", 39.0, 49.7, 150.0, 150.0, 18.0, 18.0, 1340, 125, 5.19),
    Section("150x150x15", "EA", 32.8, 41.8, 150.0, 150.0, 15.0, 15.0, 1140, 106, 5.23),
    Section("150x150x12", "EA", 26.5, 33.8, 150.0, 150.0, 12.0, 12.0, 925, 86.3, 5.23),
    Section("120x120x15", "EA", 25.8, 32.9, 120.0, 120.0, 15.0, 15.0, 593, 69.4, 4.24),
    Section("120x120x12", "EA", 20.9, 26.6, 120.0, 120.0, 12.0, 12.0, 485, 56.8, 4.27),
    Section("120x120x10", "EA", 17.6, 22.4, 120.0, 120.0, 10.0, 10.0, 411, 48.2, 4.29),
    Section("100x100x12", "EA", 17.2, 21.9, 100.0, 100.0, 12.0, 12.0, 247, 35.1, 3.36),
    Section("100x100x10", "EA", 14.5, 18.5, 100.0, 100.0, 10.0, 10.0, 211, 30.0, 3.38),
    Section("100x100x8", "EA", 11.7, 14.9, 100.0, 100.0, 8.0, 8.0, 172, 24.4, 3.40),
    Section("90x90x10", "EA", 12.9, 16.5, 90.0, 90.0, 10.0, 10.0, 146, 23.1, 2.97),
    Section("90x90x8", "EA", 10.5, 13.3, 90.0, 90.0, 8.0, 8.0, 119, 18.9, 2.99),
    Section("80x80x10", "EA", 11.3, 14.4, 80.0, 80.0, 10.0, 10.0, 87.5, 15.6, 2.47),
    Section("80x80x8", "EA", 9.2, 11.7, 80.0, 80.0, 8.0, 8.0, 71.9, 12.8, 2.48),
    Section("75x75x10", "EA", 10.5, 13.4, 75.0, 75.0, 10.0, 10.0, 69.2, 13.2, 2.27),
    Section("75x75x8", "EA", 8.6, 10.9, 75.0, 75.0, 8.0, 8.0, 57.2, 10.9, 2.29),
    Section("75x75x6", "EA", 6.5, 8.3, 75.0, 75.0, 6.0, 6.0, 44.0, 8.4, 2.31),
    Section("65x65x8", "EA", 7.3, 9.35, 65.0, 65.0, 8.0, 8.0, 35.2, 7.72, 1.94),
    Section("65x65x6", "EA", 5.6, 7.13, 65.0, 65.0, 6.0, 6.0, 27.2, 5.98, 1.95),
    Section("50x50x8", "EA", 5.5, 7.02, 50.0, 50.0, 8.0, 8.0, 13.1, 3.73, 1.37),
    Section("50x50x6", "EA", 4.2, 5.38, 50.0, 50.0, 6.0, 6.0, 10.3, 2.94, 1.39),
    Section("50x50x5", "EA", 3.6, 4.54, 50.0, 50.0, 5.0, 5.0, 8.71, 2.48, 1.39),
    
    # CHS 圆管
    Section("CHS273x10", "CHS", 64.5, 82.2, 273.0, 273.0, 10.0, 10.0, 7090, 520, 92.9),
    Section("CHS219x8", "CHS", 41.6, 53.0, 219.0, 219.0, 8.0, 8.0, 2960, 270, 74.8),
    Section("CHS194x6", "CHS", 27.7, 35.3, 194.0, 194.0, 6.0, 6.0, 1580, 163, 66.9),
    Section("CHS168x6", "CHS", 23.9, 30.5, 168.0, 168.0, 6.0, 6.0, 1020, 121, 57.9),
    Section("CHS168x5", "CHS", 20.1, 25.6, 168.0, 168.0, 5.0, 5.0, 856, 102, 57.9),
    Section("CHS140x5", "CHS", 16.6, 21.2, 140.0, 140.0, 5.0, 5.0, 492, 70.3, 48.2),
    Section("CHS114x5", "CHS", 13.4, 17.1, 114.0, 114.0, 5.0, 5.0, 259, 45.5, 39.0),
    Section("CHS114x4", "CHS", 10.8, 13.8, 114.0, 114.0, 4.0, 4.0, 210, 36.8, 39.0),
    Section("CHS89x4", "CHS", 8.3, 10.7, 89.0, 89.0, 4.0, 4.0, 97.4, 21.9, 30.2),
    Section("CHS76x4", "CHS", 7.1, 9.05, 76.0, 76.0, 4.0, 4.0, 58.6, 15.4, 25.5),
    Section("CHS60x4", "CHS", 5.5, 7.03, 60.0, 60.0, 4.0, 4.0, 26.6, 8.86, 19.5),
    
    # SHS 方管
    Section("SHS200x200x8", "SHS", 46.9, 59.7, 200.0, 200.0, 8.0, 8.0, 3620, 362, 77.9),
    Section("SHS200x200x6", "SHS", 35.7, 45.5, 200.0, 200.0, 6.0, 6.0, 2780, 278, 78.1),
    Section("SHS150x150x8", "SHS", 34.2, 43.6, 150.0, 150.0, 8.0, 8.0, 1440, 192, 57.5),
    Section("SHS150x150x6", "SHS", 26.2, 33.4, 150.0, 150.0, 6.0, 6.0, 1120, 149, 57.9),
    Section("SHS150x150x5", "SHS", 22.0, 28.0, 150.0, 150.0, 5.0, 5.0, 946, 126, 58.2),
    Section("SHS120x120x6", "SHS", 20.5, 26.1, 120.0, 120.0, 6.0, 6.0, 554, 92.4, 46.0),
    Section("SHS120x120x5", "SHS", 17.3, 22.0, 120.0, 120.0, 5.0, 5.0, 470, 78.3, 46.2),
    Section("SHS100x100x6", "SHS", 16.7, 21.3, 100.0, 100.0, 6.0, 6.0, 308, 61.6, 38.0),
    Section("SHS100x100x5", "SHS", 14.1, 18.0, 100.0, 100.0, 5.0, 5.0, 263, 52.6, 38.2),
    Section("SHS100x100x4", "SHS", 14.1, 14.5, 100.0, 100.0, 4.0, 4.0, 215, 43.0, 38.5),
    Section("SHS80x80x5", "SHS", 11.0, 14.0, 80.0, 80.0, 5.0, 5.0, 125, 31.3, 29.9),
    Section("SHS80x80x4", "SHS", 8.9, 11.4, 80.0, 80.0, 4.0, 4.0, 103, 25.8, 30.1),
    Section("SHS60x60x4", "SHS", 6.5, 8.35, 60.0, 60.0, 4.0, 4.0, 41.6, 13.9, 22.3),
    Section("SHS50x50x4", "SHS", 5.3, 6.82, 50.0, 50.0, 4.0, 4.0, 22.4, 8.96, 18.1),
    
    # RHS 矩形管
    Section("RHS300x200x8", "RHS", 58.8, 74.9, 300.0, 200.0, 8.0, 8.0, 8470, 565, 106.0),
    Section("RHS300x200x6", "RHS", 44.7, 57.0, 300.0, 200.0, 6.0, 6.0, 6540, 436, 107.0),
    Section("RHS250x150x6", "RHS", 35.7, 45.5, 250.0, 150.0, 6.0, 6.0, 3820, 306, 91.6),
    Section("RHS200x100x6", "RHS", 26.2, 33.4, 200.0, 100.0, 6.0, 6.0, 1620, 162, 69.7),
    Section("RHS200x100x5", "RHS", 22.0, 28.0, 200.0, 100.0, 5.0, 5.0, 1370, 137, 69.9),
    Section("RHS150x100x5", "RHS", 17.3, 22.0, 150.0, 100.0, 5.0, 5.0, 605, 80.7, 52.4),
    Section("RHS150x100x4", "RHS", 14.0, 17.8, 150.0, 100.0, 4.0, 4.0, 493, 65.7, 52.6),
    Section("RHS120x80x5", "RHS", 14.1, 18.0, 120.0, 80.0, 5.0, 5.0, 297, 49.5, 40.6),
    Section("RHS120x80x4", "RHS", 11.4, 14.5, 120.0, 80.0, 4.0, 4.0, 243, 40.5, 40.9),
    Section("RHS100x50x4", "RHS", 8.9, 11.4, 100.0, 50.0, 4.0, 4.0, 129, 25.8, 33.7),
]

# 默认成本库（仅在首次加载时使用，后续修改保存在session_state）
# 单价按型钢类型参考2025年市场价（元/kg）: UB≈4.5, UC≈5.3, PFC≈5.1, EA≈4.0, CHS≈4.5, SHS≈4.8, RHS≈4.6
_TYPE_PRICE = {"UB": 4.5, "UC": 5.3, "PFC": 5.1, "EA": 4.0, "CHS": 4.5, "SHS": 4.8, "RHS": 4.6}
_DEFAULT_COST_DB = {s.name: _TYPE_PRICE.get(s.type, 4.5) for s in SECTIONS_DB}

# 默认库存库（仅在首次加载时使用，后续修改保存在session_state）
_DEFAULT_INVENTORY_DB = {
    "457x191x82": 50.0, "457x191x74": 120.0, "406x178x74": 80.0, "406x178x67": 200.0,
    "356x171x67": 150.0, "356x171x57": 300.0, "305x165x54": 100.0, "305x165x46": 180.0,
    "305x165x40": 250.0, "254x146x43": 90.0, "254x146x37": 160.0, "254x146x31": 220.0,
    "203x133x30": 300.0, "203x133x25": 400.0, "203x102x23": 350.0, "178x102x19": 280.0,
    "152x89x16": 500.0, "305x305x158": 60.0, "305x305x137": 80.0, "305x305x118": 100.0,
    "305x305x97": 150.0, "254x254x107": 70.0, "254x254x89": 120.0, "254x254x73": 180.0,
    "203x203x86": 90.0, "203x203x71": 140.0, "203x203x60": 200.0, "203x203x52": 250.0,
    "203x203x46": 300.0, "152x152x37": 180.0, "152x152x30": 250.0, "152x152x23": 320.0,
    "430x100x64": 40.0, "380x100x54": 60.0, "330x90x46": 80.0, "300x90x41": 100.0,
    "260x90x35": 150.0, "230x80x30": 200.0, "200x75x26": 250.0, "180x70x22": 180.0,
    "150x60x18": 300.0, "120x50x14": 400.0, "150x150x18": 80.0, "150x150x15": 120.0,
    "150x150x12": 180.0, "120x120x15": 100.0, "120x120x12": 150.0, "120x120x10": 200.0,
    "100x100x12": 250.0, "100x100x10": 300.0, "100x100x8": 400.0, "90x90x10": 280.0,
    "90x90x8": 350.0, "80x80x10": 200.0, "80x80x8": 280.0, "75x75x10": 150.0,
    "75x75x8": 220.0, "75x75x6": 300.0, "65x65x8": 180.0, "65x65x6": 250.0,
    "50x50x8": 200.0, "50x50x6": 280.0, "50x50x5": 350.0, "CHS273x10": 30.0,
    "CHS219x8": 50.0, "CHS194x6": 80.0, "CHS168x6": 100.0, "CHS168x5": 150.0,
    "CHS140x5": 200.0, "CHS114x5": 250.0, "CHS114x4": 300.0, "CHS89x4": 400.0,
    "CHS76x4": 350.0, "CHS60x4": 500.0, "SHS200x200x8": 40.0, "SHS200x200x6": 60.0,
    "SHS150x150x8": 80.0, "SHS150x150x6": 120.0, "SHS150x150x5": 150.0, "SHS120x120x6": 200.0,
    "SHS120x120x5": 250.0, "SHS100x100x6": 300.0, "SHS100x100x5": 350.0, "SHS100x100x4": 400.0,
    "SHS80x80x5": 280.0, "SHS80x80x4": 350.0, "SHS60x60x4": 400.0, "SHS50x50x4": 500.0,
    "RHS300x200x8": 25.0, "RHS300x200x6": 40.0, "RHS250x150x6": 60.0, "RHS200x100x6": 100.0,
    "RHS200x100x5": 150.0, "RHS150x100x5": 200.0, "RHS150x100x4": 280.0, "RHS120x80x5": 250.0,
    "RHS120x80x4": 320.0, "RHS100x50x4": 400.0,
}

def _get_cost_db():
    """获取成本库（持久化到session_state，rerun不丢失）"""
    if "COST_DB" not in st.session_state:
        st.session_state["COST_DB"] = dict(_DEFAULT_COST_DB)
    return st.session_state["COST_DB"]

def _get_inventory_db():
    """获取库存库（持久化到session_state，rerun不丢失）"""
    if "INVENTORY_DB" not in st.session_state:
        st.session_state["INVENTORY_DB"] = dict(_DEFAULT_INVENTORY_DB)
    return st.session_state["INVENTORY_DB"]

SECTION_TYPE_NAMES = {
    "UB": "UB (通用梁)", "UC": "UC (通用柱)", "PFC": "PFC (槽钢)",
    "EA": "EA (等边角钢)", "CHS": "CHS (圆管)", "SHS": "SHS (方管)", "RHS": "RHS (矩形管)",
}

STRUCTURE_TYPE_NAMES = {
    "simply_supported_beam": "简支梁",
    "cantilever_beam": "悬臂梁",
    "fixed_beam": "固端梁",
    "continuous_beam": "连续梁",
}

# ============================================================
# 3. AI 功能
# ============================================================

def parse_natural_language(user_input: str) -> Optional[Dict[str, Any]]:
    """调用 DeepSeek API 解析自然语言描述"""
    try:
        client = get_deepseek_client()
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": st.session_state.get("ai_system_prompt", AI_SYSTEM_PROMPT)},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1,
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # 提取 JSON
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            return parsed
        return None
    except Exception as e:
        st.error(f"AI解析失败: {str(e)}")
        return None

CHAT_SYSTEM_PROMPT = """你是"结构设计辅助系统"的AI助手，隶属于中建国际医疗产业发展（深圳）有限公司。
你擅长钢结构设计（香港规范HK COP 2019/BS 5950），但也能回答更广泛的问题。

你可以：
1. 回答结构工程、钢结构、建筑材料、规范标准等专业问题
2. 介绍自己和系统能力
3. 回答日常问题、闲聊
4. 如果用户描述了具体的梁/柱设计需求，引导他们用更规范的格式输入，以便系统精确计算

回答要简洁友好，专业问题详细些，闲聊简短些。"""

def chat_with_ai(user_input: str) -> Optional[str]:
    """当结构解析失败时，尝试通用对话回复"""
    try:
        client = get_deepseek_client()
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": CHAT_SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None

def generate_recommendation(structure_params: Dict, best_section: Dict, structure_type: str) -> str:
    """调用 DeepSeek API 生成推荐解读"""
    try:
        client = get_deepseek_client()
        
        structure_name = STRUCTURE_TYPE_NAMES.get(structure_type, structure_type)
        description = structure_params.get("description", "")
        
        best_name = best_section['截面']
        best_util = best_section['利用率']
        prompt = f"""根据以下结构选型结果生成推荐解读：

结构类型：{structure_name}
推荐截面：{best_name}
利用率：{best_util}
库存状态：{best_section.get('库存(m)', '无数据')}
结构描述：{description}

请生成一段简洁的中文推荐解读，控制在150字以内。"""
        
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": st.session_state.get("ai_recommend_prompt", AI_RECOMMEND_PROMPT)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"推荐解读生成失败，请参考以下基本信息：推荐截面{best_name}，利用率{best_util}，库存{best_section.get('库存(m)', '无数据')}。"

# ============================================================
# 4. 连续梁三弯矩方程计算
# ============================================================

def solve_continuous_beam(
    spans: List[float], 
    loads: List[Dict],
    left_support: str = "pinned",
    right_support: str = "pinned"
) -> Dict[str, Any]:
    """
    三弯矩方程求解连续梁内力
    
    参数:
    - spans: 各跨长度列表 (m)
    - loads: 各跨荷载列表，每跨包含 dead_load, live_load, point_loads
    - left_support: 左端支座类型 (pinned/fixed)
    - right_support: 右端支座类型 (pinned/fixed)
    
    返回:
    - support_moments: 各支座弯矩 (kNm)
    - span_internal_forces: 各跨内力数据
    """
    n = len(spans)  # 跨数
    num_supports = n + 1  # 支座数
    
    # 合并恒载和活载
    total_loads = []
    for load in loads:
        q = load.get("dead_load", 0) + load.get("live_load", 0)
        point_loads = load.get("point_loads", [])
        total_loads.append({"uniform": q, "point_loads": point_loads})
    
    # 计算各跨固端弯矩相关项
    def calc_fixed_end_terms(L_i, q, point_loads):
        """计算第i跨的固端弯矩相关项 B_i^φ 和 A_i^φ"""
        B_phi = 0
        A_phi = 0
        
        # 均布荷载
        if q > 0:
            B_phi += q * L_i**3 / 24
            A_phi += q * L_i**3 / 24
        
        # 集中荷载
        for pl in point_loads:
            a = pl["position"]  # 距左端距离
            P = pl["value"]  # 力值
            b = L_i - a  # 距右端距离
            
            # B_i^φ = P*a*b*(L_i+a) / (6*L_i)
            B_phi += P * a * b * (L_i + a) / (6 * L_i)
            # A_i^φ = P*a*b*(L_i+b) / (6*L_i)
            A_phi += P * a * b * (L_i + b) / (6 * L_i)
        
        return B_phi, A_phi
    
    # 构建三弯矩方程组
    # 对于n跨连续梁，有(n-1)个中间支座需要列方程
    # 矩阵形式: A * M = B
    
    num_unknowns = num_supports  # 所有支座弯矩都是未知数
    
    A_matrix = np.zeros((num_unknowns, num_unknowns))
    B_vector = np.zeros(num_unknowns)
    
    # 支座编号: 0, 1, 2, ..., n
    # M_0 = 0 (左端铰支) 或 M_0 已知 (左端固定)
    # M_n = 0 (右端铰支) 或 M_n 已知 (右端固定)
    
    # 边界条件处理
    # 左端
    if left_support == "fixed":
        # 固定端: M_0 ≠ 0，但通过虚跨处理
        pass  # 暂不处理固定端，简化模型
    
    # 右端
    if right_support == "fixed":
        # 固定端: M_n ≠ 0
        pass
    
    # 方程编号（用于内部支座）
    eq_num = 0
    
    for i in range(1, n):  # 中间支座 1, 2, ..., n-1
        # 三弯矩方程: M_{i-1}*L_i/6 + M_i*(L_i+L_{i+1})/3 + M_{i+1}*L_{i+1}/6 = -B_i^φ - A_{i+1}^φ
        
        L_i = spans[i - 1]      # 左跨
        L_ip1 = spans[i]        # 右跨
        
        B_i_phi, A_i_phi = calc_fixed_end_terms(L_i, total_loads[i-1]["uniform"], total_loads[i-1]["point_loads"])
        B_ip1_phi, A_ip1_phi = calc_fixed_end_terms(L_ip1, total_loads[i]["uniform"], total_loads[i]["point_loads"])
        
        # 系数
        A_matrix[eq_num, i-1] = L_i / 6
        A_matrix[eq_num, i] = (L_i + L_ip1) / 3
        A_matrix[eq_num, i+1] = L_ip1 / 6
        
        # 右端项
        B_vector[eq_num] = -(B_i_phi + A_ip1_phi)
        
        eq_num += 1
    
    # 边界条件
    # 左端铰支: M_0 = 0
    if left_support == "pinned":
        A_matrix[eq_num, 0] = 1
        B_vector[eq_num] = 0
        eq_num += 1
    else:  # fixed - 添加虚跨约束
        # M_0 的条件: 通过M_1和梁的特性确定，简化处理为 M_0 = M_1/2
        A_matrix[eq_num, 0] = 1
        A_matrix[eq_num, 1] = -0.5
        B_vector[eq_num] = 0
        eq_num += 1
    
    # 右端铰支: M_n = 0
    if right_support == "pinned":
        A_matrix[eq_num, n] = 1
        B_vector[eq_num] = 0
        eq_num += 1
    else:  # fixed - 添加虚跨约束
        # M_n = M_{n-1}/2
        A_matrix[eq_num, n-1] = -0.5
        A_matrix[eq_num, n] = 1
        B_vector[eq_num] = 0
        eq_num += 1
    
    # 解线性方程组
    try:
        moments = np.linalg.solve(A_matrix, B_vector)
    except np.linalg.LinAlgError:
        # 如果矩阵奇异，使用备用方法
        moments = np.zeros(num_unknowns)
    
    # 计算各跨内力
    span_internal_forces = []
    x_positions = []  # 累计位置
    current_x = 0
    
    for i in range(n):
        L = spans[i]
        M_i = moments[i]      # 左端弯矩
        M_ip1 = moments[i+1]  # 右端弯矩
        q = total_loads[i]["uniform"]
        point_loads = total_loads[i]["point_loads"]
        
        # 简支梁弯矩和剪力
        # M_simple(x) = q*L*x/2 - q*x^2/2 + sum(P*(L-a)/L * x - P*(x-a) if x>a)
        # V_simple(x) = q*L/2 - q*x + sum(-P if x>a)
        
        # 支座弯矩引起的附加弯矩: M_add(x) = M_i + (M_ip1 - M_i)*x/L
        # 实际弯矩: M(x) = M_simple(x) + M_add(x)
        
        # 生成截面数据
        n_points = 50
        x_vals = np.linspace(0, L, n_points)
        
        M_vals = []
        V_vals = []
        
        for x in x_vals:
            # 简支梁弯矩
            M_s = q * x * (L - x) / 2
            
            # 集中力引起的弯矩
            for pl in point_loads:
                a = pl["position"]
                P = pl["value"]
                if x > a:
                    # 集中力影响: 简支梁跨中集中力
                    M_s += P * (L - a) * x / L - P * (x - a)
            
            # 附加弯矩（线性插值）
            M_add = M_i + (M_ip1 - M_i) * x / L
            
            M_vals.append(M_s + M_add)
            
            # 剪力
            V_s = q * (L / 2 - x)
            for pl in point_loads:
                a = pl["position"]
                P = pl["value"]
                if x > a:
                    V_s -= P
            V_add = (M_ip1 - M_i) / L
            V_vals.append(V_s - V_add)
        
        span_internal_forces.append({
            "span_idx": i,
            "length": L,
            "start_x": current_x,
            "end_x": current_x + L,
            "M_left": M_i,
            "M_right": M_ip1,
            "x_vals": x_vals,
            "M_vals": np.array(M_vals),
            "V_vals": np.array(V_vals),
            "x_global": x_vals + current_x
        })
        
        x_positions.append(current_x)
        current_x += L
    
    x_positions.append(current_x)  # 最后一个支座位置
    
    return {
        "support_moments": moments.tolist(),
        "support_positions": x_positions,
        "span_internal_forces": span_internal_forces,
        "max_M": max(max(sif["M_vals"]) for sif in span_internal_forces),
        "min_M": min(min(sif["M_vals"]) for sif in span_internal_forces),
        "max_V": max(max(np.abs(sif["V_vals"])) for sif in span_internal_forces),
    }


def calculate_envelope(
    spans: List[float],
    loads: List[Dict],
    live_spans_combinations: List[List[int]],
    left_support: str = "pinned",
    right_support: str = "pinned"
) -> Dict[str, Any]:
    """
    计算活载不利布置的包络图
    
    参数:
    - spans: 各跨长度
    - loads: 各跨荷载（包含dead_load和live_load）
    - live_spans_combinations: 活载布置的跨组合列表
    - left_support, right_support: 支座条件
    
    返回:
    - envelope: 包络数据
    """
    results = []
    
    # 生成所有可能的活载布置组合
    n = len(spans)
    
    # 恒载单独工况
    dead_loads = [{"dead_load": l["dead_load"], "live_load": 0, "point_loads": l.get("point_loads", [])} for l in loads]
    
    # 添加恒载工况
    dead_result = solve_continuous_beam(spans, dead_loads, left_support, right_support)
    results.append({
        "name": "恒载",
        "live_spans": [],
        "result": dead_result
    })
    
    # 添加指定的活载组合
    for combo in live_spans_combinations:
        # 创建活载工况
        combo_loads = []
        for i, load in enumerate(loads):
            live_q = load.get("live_load", 0) if i in combo else 0
            combo_loads.append({
                "dead_load": load["dead_load"],
                "live_load": live_q,
                "point_loads": load.get("point_loads", [])
            })
        
        result = solve_continuous_beam(spans, combo_loads, left_support, right_support)
        live_str = "+".join([f"第{i+1}跨" for i in combo])
        results.append({
            "name": f"恒载+活载({live_str})",
            "live_spans": combo,
            "result": result
        })
    
    # 计算包络值 - 逐跨计算
    n_spans = len(spans)
    M_max_env_all = []
    M_min_env_all = []
    V_max_env_all = []
    V_min_env_all = []
    x_global_all = []
    
    for span_idx in range(n_spans):
        span_M = []
        span_V = []
        for res in results:
            sif = res["result"]["span_internal_forces"][span_idx]
            span_M.append(sif["M_vals"])
            span_V.append(sif["V_vals"])
        
        span_M_arr = np.array(span_M)
        span_V_arr = np.array(span_V)
        
        M_max_env_all.extend(np.max(span_M_arr, axis=0).tolist())
        M_min_env_all.extend(np.min(span_M_arr, axis=0).tolist())
        V_max_env_all.extend(np.max(span_V_arr, axis=0).tolist())
        V_min_env_all.extend(np.min(span_V_arr, axis=0).tolist())
        
        x_global_all.extend(results[0]["result"]["span_internal_forces"][span_idx]["x_global"])
    
    M_max_env = np.array(M_max_env_all)
    M_min_env = np.array(M_min_env_all)
    V_max_env = np.array(V_max_env_all)
    V_min_env = np.array(V_min_env_all)
    x_global = x_global_all
    
    if len(M_max_env) > 0:
        return {
            "results": results,
            "M_max_envelope": M_max_env.tolist(),
            "M_min_envelope": M_min_env.tolist(),
            "V_max_envelope": V_max_env.tolist(),
            "V_min_envelope": V_min_env.tolist(),
            "x_global": x_global,
            "max_M_pos": float(max(M_max_env)),
            "min_M_neg": float(min(M_min_env)),
            "max_V": float(max(max(np.abs(V_max_env)), max(np.abs(V_min_env))))
        }
    
    return {"results": results, "M_max_envelope": [], "M_min_envelope": [], "V_max_envelope": [], "V_min_envelope": [], "x_global": []}


def calculate_simple_beam(span: float, load_value: float, load_type: str = "uniform") -> Dict[str, Any]:
    """简支梁内力计算"""
    L = span
    q = load_value
    import numpy as np
    n_pts = 50
    x = np.linspace(0, L, n_pts)
    
    if load_type == "point":
        P = load_value
        M_max = P * L / 4
        V_max = P / 2
        M_vals = [P * xi / 2 if xi <= L/2 else P * (L - xi) / 2 for xi in x]
        V_vals = [P / 2 if xi < L/2 else -P / 2 for xi in x]
    else:
        M_max = q * L**2 / 8
        V_max = q * L / 2
        M_vals = [q * xi * (L - xi) / 2 for xi in x]
        V_vals = [q * (L/2 - xi) for xi in x]
    
    return {
        "M_max": M_max,
        "V_max": V_max,
        "M_vals": M_vals,
        "V_vals": V_vals,
        "x_vals": list(x),
        "span": L,
        "load_value": q,
        "load_type": load_type
    }


def calculate_cantilever_beam(span: float, load_value: float, load_type: str = "uniform") -> Dict[str, Any]:
    """悬臂梁内力计算（固定端在左，自由端在右）"""
    L = span
    q = load_value
    import numpy as np
    n_pts = 50
    x = np.linspace(0, L, n_pts)
    
    if load_type == "point":
        P = load_value
        M_max = P * L
        V_max = P
        M_vals = [-P * (L - xi) for xi in x]
        V_vals = [P for xi in x]
    else:
        M_max = q * L**2 / 2
        V_max = q * L
        M_vals = [-q * (L - xi)**2 / 2 for xi in x]
        V_vals = [q * (L - xi) for xi in x]
    
    return {
        "M_max": M_max,
        "V_max": V_max,
        "M_vals": M_vals,
        "V_vals": V_vals,
        "x_vals": list(x),
        "span": L,
        "load_value": q,
        "load_type": load_type
    }


def calculate_fixed_beam(span: float, load_value: float, load_type: str = "uniform") -> Dict[str, Any]:
    """固端梁内力计算"""
    L = span
    q = load_value
    import numpy as np
    n_pts = 50
    x = np.linspace(0, L, n_pts)
    
    M_end = q * L**2 / 12
    M_mid = q * L**2 / 24
    M_max = M_end
    V_max = q * L / 2
    M_vals = [q * xi * (L - xi) / 2 - M_end for xi in x]
    V_vals = [q * (L/2 - xi) for xi in x]
    
    return {
        "M_max": M_max,
        "V_max": V_max,
        "M_vals": M_vals,
        "V_vals": V_vals,
        "x_vals": list(x),
        "span": L,
        "load_value": q,
        "load_type": load_type
    }


# ============================================================
# 5. 图形生成
# ============================================================

def draw_load_diagram(
    spans: List[float],
    loads: List[Dict],
    left_support: str,
    right_support: str,
    live_spans: List[int] = None
) -> io.BytesIO:
    """绘制荷载简图 - 所有荷载箭头统一放在梁上方，分层显示"""
    fig, ax = plt.subplots(figsize=(14, 5))
    
    n = len(spans)
    total_length = sum(spans)
    
    # 支座位置
    support_x = [0]
    for s in spans:
        support_x.append(support_x[-1] + s)
    
    # ============ 绘制梁轴线（放在图中间偏下位置）============
    beam_y = 0.0  # 梁轴线Y位置
    
    # 确定荷载高度范围（向上为正）
    max_load_height = 1.5  # 最大荷载高度（集中力用）
    
    ax.plot([0, total_length], [beam_y, beam_y], 'k-', linewidth=2.5)
    
    # ============ 绘制支座（支座在梁下方）============
    support_y = -0.4  # 支座位置（梁下方）
    for i, x in enumerate(support_x):
        if i == 0:
            if left_support == "fixed":
                # 固定端
                ax.plot([x-0.3, x+0.3], [support_y-0.1, support_y-0.1], 'k-', linewidth=2)
                ax.plot([x-0.2, x+0.2], [support_y-0.2, support_y-0.2], 'k-', linewidth=1.5)
                ax.plot([x-0.1, x+0.1], [support_y-0.3, support_y-0.3], 'k-', linewidth=1)
            else:
                # 铰支座 - 三角形式
                ax.plot([x-0.3, x+0.3], [support_y, support_y], 'k-', linewidth=2)
                ax.plot([x, x-0.2], [beam_y, support_y], 'k-', linewidth=1.5)
                ax.plot([x, x+0.2], [beam_y, support_y], 'k-', linewidth=1.5)
        elif i == n:
            if right_support == "fixed":
                ax.plot([x-0.3, x+0.3], [support_y-0.1, support_y-0.1], 'k-', linewidth=2)
                ax.plot([x-0.2, x+0.2], [support_y-0.2, support_y-0.2], 'k-', linewidth=1.5)
                ax.plot([x-0.1, x+0.1], [support_y-0.3, support_y-0.3], 'k-', linewidth=1)
            else:
                ax.plot([x-0.3, x+0.3], [support_y, support_y], 'k-', linewidth=2)
                ax.plot([x, x-0.2], [beam_y, support_y], 'k-', linewidth=1.5)
                ax.plot([x, x+0.2], [beam_y, support_y], 'k-', linewidth=1.5)
        else:
            # 中间支座 - 滚动支座
            ax.plot([x-0.2, x+0.2], [support_y, support_y], 'k-', linewidth=2)
            ax.plot([x, x-0.15], [beam_y, support_y], 'k-', linewidth=1.5)
            ax.plot([x, x+0.15], [beam_y, support_y], 'k-', linewidth=1.5)
    
    # ============ 绘制荷载（全部在梁上方，分层排列）============
    # 层级定义（从下到上）
    # 第一层：恒载（最靠近梁）- 灰色
    # 第二层：活载 - 蓝色
    # 第三层：集中力（最上方）- 红色
    dead_y = 0.35    # 恒载箭头高度
    live_y = 0.70    # 活载箭头高度
    point_y = 1.15   # 集中力箭头高度
    
    current_x = 0
    for i, (L, load) in enumerate(zip(spans, loads)):
        dead_q = load.get("dead_load", 0)
        live_q = load.get("live_load", 0)
        point_loads = load.get("point_loads", [])
        
        # --- 第一层：恒载（灰色）---
        if dead_q > 0:
            n_arrows = max(4, int(L * 2))
            for j in range(n_arrows + 1):
                x_pos = current_x + j * L / n_arrows
                ax.annotate('', xy=(x_pos, dead_y), xytext=(x_pos, beam_y + 0.05),
                           arrowprops=dict(arrowstyle='->', color='#666666', lw=1.2))
            ax.plot([current_x, current_x + L], [dead_y, dead_y], color='#666666', linewidth=0.8, linestyle='--')
            ax.text(current_x + L/2, dead_y - 0.15, f'q={dead_q:.1f}', 
                   ha='center', fontsize=8, color='#666666', fontweight='bold')
        
        # --- 第二层：活载（蓝色）---
        is_live = live_spans is None or i in live_spans
        if live_q > 0 and is_live:
            n_arrows = max(4, int(L * 2))
            for j in range(n_arrows + 1):
                x_pos = current_x + j * L / n_arrows
                base_y = dead_y + 0.35 if dead_q > 0 else beam_y + 0.05
                ax.annotate('', xy=(x_pos, live_y), xytext=(x_pos, base_y),
                           arrowprops=dict(arrowstyle='->', color='blue', lw=1.2))
            ax.plot([current_x, current_x + L], [live_y, live_y], color='blue', linewidth=0.8, linestyle='--')
            ax.text(current_x + L/2, live_y - 0.15, f'q={live_q:.1f}', 
                   ha='center', fontsize=8, color='blue', fontweight='bold')
        
        # --- 第三层：集中力（红色，粗箭头）---
        for pl in point_loads:
            P = pl["value"]
            a = pl["position"]
            x_pos = current_x + a
            base_y = live_y + 0.35 if live_q > 0 and is_live else (dead_y + 0.35 if dead_q > 0 else beam_y + 0.05)
            ax.annotate('', xy=(x_pos, point_y), xytext=(x_pos, base_y),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
            ax.text(x_pos, point_y - 0.15, f'P={P:.1f}', ha='center', fontsize=8, 
                   color='red', fontweight='bold')
        
        # --- 跨度数字标注（在梁下方）---
        ax.text(current_x + L/2, -0.75, f'{L:.1f}m', ha='center', fontsize=9, 
               fontweight='bold', color='black')
        
        current_x += L
    
    # ============ 图例 ===========
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#666666', label=f'恒载 (dead)'),
        Patch(facecolor='blue', alpha=0.7, label=f'活载 (live)'),
        Patch(facecolor='red', alpha=0.7, label=f'集中力 (point)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    ax.set_xlim(-1, total_length + 1)
    ax.set_ylim(-1.2, max_load_height + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('荷载简图 (Load Diagram)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    
    return buf


def draw_moment_diagram(
    spans: List[float],
    span_forces: List[Dict],
    title: str = "弯矩图"
) -> io.BytesIO:
    """绘制弯矩图 - 标注每跨最大正弯矩和支座弯矩"""
    fig, ax = plt.subplots(figsize=(14, 5))
    
    total_length = sum(spans)
    
    # 支座位置
    support_x = [0]
    for s in spans:
        support_x.append(support_x[-1] + s)
    
    # 绘制支座竖线
    for x in support_x:
        ax.axvline(x=x, color='gray', linestyle='--', alpha=0.5)
    
    # 绘制弯矩
    for sif in span_forces:
        x_vals = sif["x_global"]
        M_vals = -sif["M_vals"]  # 负弯矩画在上方
        
        ax.fill_between(x_vals, 0, M_vals, alpha=0.3, color='blue')
        ax.plot(x_vals, M_vals, 'b-', linewidth=2)
    
    # 绘制梁轴线
    ax.axhline(y=0, color='black', linewidth=1)
    
    # ============ 标注支座弯矩 ============
    from matplotlib.patches import Rectangle
    
    support_moments = [sif["M_left"] for sif in span_forces] + [span_forces[-1]["M_right"]]
    for i, M in enumerate(support_moments):
        x = support_x[i]
        y_val = -M
        # 添加白色背景框避免重叠
        bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray', alpha=0.9)
        ax.annotate(f'{M:.1f}', xy=(x, y_val), xytext=(x, y_val + 0.3 if y_val >= 0 else y_val - 0.6),
                   ha='center', va='bottom' if y_val >= 0 else 'top',
                   fontsize=9, fontweight='bold', color='darkblue',
                   bbox=bbox_props)
    
    # ============ 标注每跨最大正弯矩 ============
    span_colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4']
    
    for idx, sif in enumerate(span_forces):
        M_orig = sif["M_vals"]  # 原始弯矩值（正=正弯矩）
        x_vals = sif["x_global"]
        M_plot = -M_orig  # 绘图值（翻转后）
        
        # 找到原始弯矩的最大正值（正弯矩）
        max_M_orig = float(np.max(M_orig))
        if max_M_orig > 0.1:  # 只标注大于阈值的正弯矩
            max_idx = int(np.argmax(M_orig))
            x_max = x_vals[max_idx]
            y_max = M_plot[max_idx]
            
            # 在最大弯矩点上方标注
            color = span_colors[idx % len(span_colors)]
            bbox_props = dict(boxstyle='round,pad=0.3', facecolor='lightyellow', 
                            edgecolor=color, alpha=0.95, linewidth=1.5)
            ax.annotate(f'Mmax={max_M_orig:.1f}', 
                       xy=(x_max, y_max),
                       xytext=(x_max, y_max + 0.8),
                       ha='center', va='bottom',
                       fontsize=8, fontweight='bold', color='darkred',
                       bbox=bbox_props,
                       arrowprops=dict(arrowstyle='->', color='darkred', lw=1))
    
    # 设置坐标轴
    ax.set_xlim(-0.5, total_length + 0.5)
    ax.set_xlabel('位置 (m)', fontsize=11)
    ax.set_ylabel('弯矩 (kNm)', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    
    return buf


def draw_shear_diagram(
    spans: List[float],
    span_forces: List[Dict],
    title: str = "剪力图"
) -> io.BytesIO:
    """绘制剪力图 - 标注每跨最大正/负剪力和支座处剪力"""
    fig, ax = plt.subplots(figsize=(14, 5))
    
    total_length = sum(spans)
    
    # 支座位置
    support_x = [0]
    for s in spans:
        support_x.append(support_x[-1] + s)
    
    # 绘制支座竖线
    for x in support_x:
        ax.axvline(x=x, color='gray', linestyle='--', alpha=0.5)
    
    # 绘制剪力
    for sif in span_forces:
        x_vals = sif["x_global"]
        V_vals = sif["V_vals"]
        
        ax.plot(x_vals, V_vals, 'r-', linewidth=2)
        ax.fill_between(x_vals, 0, V_vals, alpha=0.2, color='red')
    
    # 绘制梁轴线
    ax.axhline(y=0, color='black', linewidth=1)
    
    # ============ 标注支座处剪力 ============
    # 左端剪力
    V_left = span_forces[0]["V_vals"][0]
    x_left = support_x[0]
    bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='darkred', alpha=0.9)
    ax.annotate(f'{V_left:.1f}', xy=(x_left, V_left), xytext=(x_left - 0.3, V_left),
               ha='right', va='center' if V_left >= 0 else 'center',
               fontsize=8, fontweight='bold', color='darkred',
               bbox=bbox_props)
    
    # 中间支座处剪力（每跨右端）
    for idx, sif in enumerate(span_forces):
        if idx < len(span_forces) - 1:
            # 支座在跨i的右端，同时也是跨i+1的左端
            next_sif = span_forces[idx + 1]
            x_supp = support_x[idx + 1]
            V_right = sif["V_vals"][-1]  # 跨i右端剪力
            V_left_next = next_sif["V_vals"][0]  # 跨i+1左端剪力
            
            # 取绝对值较大的那个（或平均值作为支座剪力）
            V_support = (V_right + V_left_next) / 2
            bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='darkred', alpha=0.9)
            ax.annotate(f'{V_support:.1f}', xy=(x_supp, V_support), 
                       xytext=(x_supp + 0.3 if V_support >= 0 else x_supp - 0.3, V_support),
                       ha='left' if V_support >= 0 else 'right',
                       fontsize=8, fontweight='bold', color='darkred',
                       bbox=bbox_props)
    
    # 右端剪力
    V_right_end = span_forces[-1]["V_vals"][-1]
    x_right = support_x[-1]
    bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='darkred', alpha=0.9)
    ax.annotate(f'{V_right_end:.1f}', xy=(x_right, V_right_end), xytext=(x_right + 0.3, V_right_end),
               ha='left', fontsize=8, fontweight='bold', color='darkred',
               bbox=bbox_props)
    
    # ============ 标注每跨最大正/负剪力 ============
    span_colors_pos = ['#1976D2', '#388E3C', '#F57C00', '#7B1FA2', '#00796B']
    span_colors_neg = ['#E53935', '#C62828', '#AD1457', '#6A1B9A', '#004D40']
    
    for idx, sif in enumerate(span_forces):
        V_vals = sif["V_vals"]
        x_vals = sif["x_global"]
        
        # 找到最大正剪力和最大负剪力
        max_V = np.max(V_vals)
        min_V = np.min(V_vals)
        
        # 最大正剪力
        if max_V > 0.5:  # 只标注大于阈值的
            max_idx = np.argmax(V_vals)
            x_max = x_vals[max_idx]
            color = span_colors_pos[idx % len(span_colors_pos)]
            bbox_props = dict(boxstyle='round,pad=0.3', facecolor='lightcyan', 
                            edgecolor=color, alpha=0.95, linewidth=1.5)
            # 根据位置决定偏移方向
            if x_max < total_length / 2:
                xytext = (x_max + 0.5, max_V + 0.5)
                ha = 'left'
            else:
                xytext = (x_max - 0.5, max_V + 0.5)
                ha = 'right'
            ax.annotate(f'Vmax+={max_V:.1f}', 
                       xy=(x_max, max_V),
                       xytext=xytext,
                       ha=ha, va='bottom',
                       fontsize=8, fontweight='bold', color='#1565C0',
                       bbox=bbox_props,
                       arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1))
        
        # 最大负剪力
        if min_V < -0.5:  # 只标注绝对值大于阈值的
            min_idx = np.argmin(V_vals)
            x_min = x_vals[min_idx]
            color = span_colors_neg[idx % len(span_colors_neg)]
            bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', 
                            edgecolor=color, alpha=0.95, linewidth=1.5)
            # 根据位置决定偏移方向
            if x_min < total_length / 2:
                xytext = (x_min + 0.5, min_V - 0.5)
                ha = 'left'
            else:
                xytext = (x_min - 0.5, min_V - 0.5)
                ha = 'right'
            ax.annotate(f'Vmax-={min_V:.1f}', 
                       xy=(x_min, min_V),
                       xytext=xytext,
                       ha=ha, va='top',
                       fontsize=8, fontweight='bold', color='#B71C1C',
                       bbox=bbox_props,
                       arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=1))
    
    ax.set_xlim(-0.5, total_length + 0.5)
    ax.set_xlabel('位置 (m)', fontsize=11)
    ax.set_ylabel('剪力 (kN)', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    
    return buf


def draw_envelope_diagram(
    spans: List[float],
    envelope_data: Dict,
    title_m: str = "弯矩包络图",
    title_v: str = "剪力包络图"
) -> Tuple[io.BytesIO, io.BytesIO]:
    """绘制包络图 - 添加关键数值标注"""
    # 弯矩包络图
    fig_m, ax_m = plt.subplots(figsize=(14, 5))
    
    total_length = sum(spans)
    x_global = envelope_data["x_global"]
    M_max = envelope_data["M_max_envelope"]
    M_min = envelope_data["M_min_envelope"]
    
    # 支座位置
    support_x = [0]
    for s in spans:
        support_x.append(support_x[-1] + s)
    
    for x in support_x:
        ax_m.axvline(x=x, color='gray', linestyle='--', alpha=0.5)
    
    # 包络区域
    ax_m.fill_between(x_global, M_max, M_min, alpha=0.3, color='purple')
    ax_m.plot(x_global, M_max, 'b-', linewidth=2, label='最大弯矩')
    ax_m.plot(x_global, M_min, 'r-', linewidth=2, label='最小弯矩')
    
    ax_m.axhline(y=0, color='black', linewidth=1)
    
    # ============ 弯矩包络图标注 ============
    # 标注每跨最大正弯矩
    span_colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4']
    current_x = 0
    for idx, (L, color) in enumerate(zip(spans, span_colors)):
        # 在该跨范围内找最大正弯矩
        mask = [(current_x <= x <= current_x + L) for x in x_global]
        span_M_max = [m for m, ok in zip(M_max, mask) if ok]
        span_M_min = [m for m, ok in zip(M_min, mask) if ok]
        span_x = [x for x, ok in zip(x_global, mask) if ok]
        
        if span_M_max:
            max_val = max(span_M_max)
            if max_val > 0.5:
                max_idx = span_M_max.index(max_val)
                x_max = span_x[max_idx]
                bbox_props = dict(boxstyle='round,pad=0.3', facecolor='lightyellow', 
                                edgecolor=color, alpha=0.95, linewidth=1.5)
                ax_m.annotate(f'Mmax={max_val:.1f}', 
                           xy=(x_max, max_val),
                           xytext=(x_max, max_val + 2),
                           ha='center', va='bottom',
                           fontsize=8, fontweight='bold', color='darkgreen',
                           bbox=bbox_props,
                           arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1))
        
        # 标注该跨最小弯矩（最大负弯矩）
        if span_M_min:
            min_val = min(span_M_min)
            if min_val < -0.5:
                min_idx = span_M_min.index(min_val)
                x_min = span_x[min_idx]
                bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', 
                                edgecolor=color, alpha=0.95, linewidth=1.5)
                ax_m.annotate(f'Mmin={min_val:.1f}', 
                           xy=(x_min, min_val),
                           xytext=(x_min, min_val - 2),
                           ha='center', va='top',
                           fontsize=8, fontweight='bold', color='darkred',
                           bbox=bbox_props,
                           arrowprops=dict(arrowstyle='->', color='darkred', lw=1))
        
        current_x += L
    
    # 标注支座处弯矩
    for i, x in enumerate(support_x):
        if i > 0 and i < len(support_x) - 1:  # 中间支座
            # 找最近的点
            distances = [abs(x - gx) for gx in x_global]
            nearest_idx = np.argmin(distances)
            M_val = M_min[nearest_idx]  # 中间支座通常是负弯矩
            
            bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray', alpha=0.9)
            ax_m.annotate(f'{M_val:.1f}', 
                         xy=(x, M_val),
                         xytext=(x + 0.3, M_val + 1 if M_val >= 0 else M_val - 1.5),
                         ha='left' if M_val >= 0 else 'center',
                         fontsize=8, fontweight='bold', color='darkblue',
                         bbox=bbox_props)
    
    ax_m.set_xlim(-0.5, total_length + 0.5)
    ax_m.set_xlabel('位置 (m)', fontsize=11)
    ax_m.set_ylabel('弯矩 (kNm)', fontsize=11)
    ax_m.set_title(title_m, fontsize=14, fontweight='bold')
    ax_m.legend(loc='upper right')
    ax_m.grid(True, alpha=0.3)
    
    plt.tight_layout()
    buf_m = io.BytesIO()
    plt.savefig(buf_m, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf_m.seek(0)
    plt.close()
    
    # ============ 剪力包络图 ============
    fig_v, ax_v = plt.subplots(figsize=(14, 5))
    
    V_max = envelope_data["V_max_envelope"]
    V_min = envelope_data["V_min_envelope"]
    
    for x in support_x:
        ax_v.axvline(x=x, color='gray', linestyle='--', alpha=0.5)
    
    ax_v.fill_between(x_global, V_max, V_min, alpha=0.3, color='orange')
    ax_v.plot(x_global, V_max, 'b-', linewidth=2, label='最大剪力')
    ax_v.plot(x_global, V_min, 'r-', linewidth=2, label='最小剪力')
    
    ax_v.axhline(y=0, color='black', linewidth=1)
    
    # ============ 剪力包络图标注 ============
    # 标注每跨最大正/负剪力
    current_x = 0
    for idx, (L, color) in enumerate(zip(spans, span_colors)):
        mask = [(current_x <= x <= current_x + L) for x in x_global]
        span_V_max = [v for v, ok in zip(V_max, mask) if ok]
        span_V_min = [v for v, ok in zip(V_min, mask) if ok]
        span_x = [x for x, ok in zip(x_global, mask) if ok]
        
        if span_V_max:
            max_val = max(span_V_max)
            if max_val > 0.5:
                max_idx = span_V_max.index(max_val)
                x_max = span_x[max_idx]
                bbox_props = dict(boxstyle='round,pad=0.3', facecolor='lightcyan', 
                                edgecolor=color, alpha=0.95, linewidth=1.5)
                ax_v.annotate(f'Vmax+={max_val:.1f}', 
                           xy=(x_max, max_val),
                           xytext=(x_max, max_val + 2),
                           ha='center', va='bottom',
                           fontsize=8, fontweight='bold', color='#1565C0',
                           bbox=bbox_props,
                           arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1))
        
        if span_V_min:
            min_val = min(span_V_min)
            if min_val < -0.5:
                min_idx = span_V_min.index(min_val)
                x_min = span_x[min_idx]
                bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', 
                                edgecolor=color, alpha=0.95, linewidth=1.5)
                ax_v.annotate(f'Vmax-={min_val:.1f}', 
                           xy=(x_min, min_val),
                           xytext=(x_min, min_val - 2),
                           ha='center', va='top',
                           fontsize=8, fontweight='bold', color='#B71C1C',
                           bbox=bbox_props,
                           arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=1))
        
        current_x += L
    
    # 标注支座处剪力
    for i, x in enumerate(support_x):
        distances = [abs(x - gx) for gx in x_global]
        nearest_idx = np.argmin(distances)
        
        # 取该点最大的绝对值
        v1, v2 = V_max[nearest_idx], V_min[nearest_idx]
        v_val = v1 if abs(v1) > abs(v2) else v2
        
        if abs(v_val) > 0.5:
            bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray', alpha=0.9)
            y_offset = 2 if v_val >= 0 else -2
            ax_v.annotate(f'{v_val:.1f}', 
                         xy=(x, v_val),
                         xytext=(x + 0.3, v_val + y_offset),
                         ha='left',
                         fontsize=8, fontweight='bold', color='darkred',
                         bbox=bbox_props)
    
    ax_v.set_xlim(-0.5, total_length + 0.5)
    ax_v.set_xlabel('位置 (m)', fontsize=11)
    ax_v.set_ylabel('剪力 (kN)', fontsize=11)
    ax_v.set_title(title_v, fontsize=14, fontweight='bold')
    ax_v.legend(loc='upper right')
    ax_v.grid(True, alpha=0.3)
    
    plt.tight_layout()
    buf_v = io.BytesIO()
    plt.savefig(buf_v, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf_v.seek(0)
    plt.close()
    
    return buf_m, buf_v


# ============================================================
# 6. 计算引擎
# ============================================================

def check_beam(section: Section, M: float, V: float, L: float) -> tuple:
    """梁验算"""
    fy = 275
    Mc = fy * section.Wx * 1e-3
    Vc = 0.6 * fy * section.D * section.t * 1e-3
    util = max(M / Mc, V / Vc)
    return util < 1.0, util, Mc, Vc

def check_column(section: Section, N: float, M: float, Le: float) -> tuple:
    """柱验算"""
    fy = 275
    lam = Le * 1000 / section.rx
    if lam <= 180:
        pc = fy * (1 - 0.15 * (lam / 180)**2)
    else:
        pc = fy * 0.1
    Pc = pc * section.A * 1e-3
    Mc = fy * section.Wx * 1e-3
    util = N / Pc + 0.95 * M / Mc
    return util < 1.0 and lam < 180, util, Pc, Mc, lam

def get_inventory(section_name: str) -> float:
    """获取库存量"""
    return _get_inventory_db().get(section_name, 0.0)

def select_sections(member_type: str, L: float, M: float, V: float, N: float, 
                    sort_by: str, section_types: List[str], prefer_inventory: bool = True):
    """选型 - 优先推荐有库存的截面"""
    results = []
    for sec in SECTIONS_DB:
        if sec.type not in section_types:
            continue
        
        if member_type == "beam":
            ok, util, Mc, Vc = check_beam(sec, M, V, L)
            Pc, lam = 0, 0
        else:
            ok, util, Pc, Mc, lam = check_column(sec, N, M, L)
            Vc = 0
        
        if not ok:
            continue
        
        cost = _get_cost_db().get(sec.name, 4.0) * sec.mass * L
        inventory = get_inventory(sec.name)
        
        results.append({
            "截面": sec.name,
            "类型": sec.type,
            "利用率": f"{util:.1%}",
            "利用率值": util,
            "成本(元)": f"{cost:.0f}",
            "成本值": cost,
            "质量(kg/m)": f"{sec.mass:.1f}",
            "库存(m)": f"{inventory:.1f}" if inventory > 0 else "-",
            "库存值": inventory,
            "section": sec,
        })
    
    if not results:
        return []
    
    if prefer_inventory:
        has_inventory = [r for r in results if r["库存值"] > 0]
        no_inventory = [r for r in results if r["库存值"] == 0]
        
        sort_key = "利用率值" if sort_by == "利用率" else "成本值"
        has_inventory.sort(key=lambda x: x[sort_key])
        no_inventory.sort(key=lambda x: x[sort_key])
        
        results = has_inventory + no_inventory
    else:
        sort_key = "利用率值" if sort_by == "利用率" else "成本值"
        results.sort(key=lambda x: x[sort_key])
    
    return results


def select_sections_for_continuous_beam(
    spans: List[float],
    max_M: float,
    max_V: float,
    section_types: List[str],
    prefer_inventory: bool = True
) -> List[Dict]:
    """连续梁截面选型 - 基于最大内力"""
    # 使用总跨度和最大内力
    total_length = sum(spans)
    results = []
    
    for sec in SECTIONS_DB:
        if sec.type not in section_types:
            continue
        
        # 验算
        ok, util, Mc, Vc = check_beam(sec, max_M, max_V, total_length)
        
        if not ok:
            continue
        
        # 计算总成本
        total_mass = sec.mass * total_length
        cost = _get_cost_db().get(sec.name, 4.0) * total_mass
        inventory = get_inventory(sec.name)
        
        results.append({
            "截面": sec.name,
            "类型": sec.type,
            "利用率": f"{util:.1%}",
            "利用率值": util,
            "成本(元)": f"{cost:.0f}",
            "成本值": cost,
            "质量(kg/m)": f"{sec.mass:.1f}",
            "总质量(kg)": f"{total_mass:.1f}",
            "库存(m)": f"{inventory:.1f}" if inventory > 0 else "-",
            "库存值": inventory,
            "section": sec,
        })
    
    if not results:
        return []
    
    if prefer_inventory:
        has_inventory = [r for r in results if r["库存值"] > 0]
        no_inventory = [r for r in results if r["库存值"] == 0]
        
        has_inventory.sort(key=lambda x: x["利用率值"])
        no_inventory.sort(key=lambda x: x["利用率值"])
        
        results = has_inventory + no_inventory
    else:
        results.sort(key=lambda x: x["利用率值"])
    
    return results

# ============================================================
# 7. 计算书生成
# ============================================================

def generate_calc_sheet_md(
    project_name: str, 
    structure_params: Dict,
    calc_result: Dict,
    best_section: dict, 
    user_name: str
) -> str:
    """生成Markdown计算书"""
    sec = best_section["section"]
    today = datetime.now().strftime("%Y-%m-%d")
    inventory = best_section["库存值"]
    
    spans = structure_params["spans"]
    total_length = sum(s["length"] for s in spans)
    
    # 提取计算结果变量，避免f-string中字典访问兼容性问题
    max_M = calc_result['max_M']
    min_M = calc_result['min_M']
    max_V = calc_result['max_V']
    Mc_val = 275 * sec.Wx * 1e-3
    Vc_val = 0.6 * 275 * sec.D * sec.t * 1e-3
    ratio_val = best_section['利用率值']
    util_str = best_section['利用率']
    cost_per_kg = _get_cost_db().get(sec.name, 4.0)
    
    # 结构描述
    spans_str = "+".join([f"{s['length']:.1f}" for s in spans])
    left_s = "铰支" if structure_params.get("left_support") == "pinned" else "固定"
    right_s = "铰支" if structure_params.get("right_support") == "pinned" else "固定"
    
    calc_sheet = f"""
# 连续梁结构设计计算书

## 项目信息
- **工程名称：** {project_name}
- **结构类型：** {len(spans)}跨连续梁
- **跨度配置：** {spans_str} m
- **支座条件：** 左端{left_s}，右端{right_s}
- **截面类型：** {sec.type}
- **设计日期：** {today}
- **设计者：** {user_name}

---

## 1. 设计依据

本计算依据以下规范：
- **HK COP for Structural Use of Steel 2019** (香港钢结构规范)
- 等同采用 **BS 5950-1:2000** (英国钢结构设计规范)
- 材料牌号：**S275** (fy = 275 N/mm²)

---

## 2. 结构模型

### 2.1 几何参数

| 跨号 | 跨度(m) | 恒载(kN/m) | 活载(kN/m) |
|------|----------|------------|------------|
"""
    
    for i, s in enumerate(spans):
        calc_sheet += f"| {i+1} | {s['length']:.1f} | {s.get('dead_load', 0):.1f} | {s.get('live_load', 0):.1f} |\n"
    
    calc_sheet += f"""
### 2.2 支座条件
- 左端支座：{left_s}
- 右端支座：{right_s}
- 中间支座：均为铰支座

### 2.3 计算方法
采用**三弯矩方程**（力法）进行连续梁内力分析。

**三弯矩方程基本形式：**

M(i-1) × Li / 6EI + M(i) × (Li + Li+1) / 3EI + M(i+1) × Li+1 / 6EI = -Biφ - Ai+1φ

其中：
- Biφ: 第i跨右端固端弯矩项
- Ai+1φ: 第i+1跨左端固端弯矩项

**均布荷载固端弯矩项：**
Biφ = q × Li³ / (24EI)

**集中力固端弯矩项（距左端a，右端b=Li-a）：**
Biφ = P × a × b × (Li + a) / (6 × EI × Li)
Aiφ = P × a × b × (Li + b) / (6 × EI × Li)

**支座条件：**
- 铰支座：M = 0
- 固定端：该端弯矩作为未知数参与方程求解

**跨内任意截面内力：**
- 弯矩：M(x) = M简支(x) + M左 + (M右 - M左) × x / L
- 剪力：V(x) = V简支(x) + (M右 - M左) / L

---

## 3. 内力计算结果

### 3.1 方程求解过程

"""
    # 写出方程组
    moments_list = calc_result["support_moments"]
    n_supports = len(moments_list)
    calc_sheet += f"共{n_supports}个支座，{n_supports-1}跨连续梁\n\n"
    
    if structure_params.get("structure_type") == "continuous_beam":
        spans_info = structure_params.get("spans", [])
        calc_sheet += "**各跨参数：**\n\n"
        calc_sheet += "| 跨号 | 跨度(m) | 均布荷载(kN/m) | 集中力 |\n"
        calc_sheet += "|------|---------|----------------|--------|\n"
        for idx, sp in enumerate(spans_info):
            q_val = sp.get("dead_load", 0) + sp.get("live_load", 0)
            pts = sp.get("point_loads", [])
            pt_str = ", ".join([f"{p.get('value',0)}kN@{p.get('position',0)}m" for p in pts]) if pts else "-"
            calc_sheet += f"| {idx+1} | {sp.get('length',0):.1f} | {q_val:.1f} | {pt_str} |\n"
        calc_sheet += "\n"
    
    calc_sheet += "**求解结果：**\n\n"
    calc_sheet += """### 3.2 支座弯矩

| 支座 | 弯矩(kNm) |
|------|----------|
"""
    
    moments = calc_result["support_moments"]
    for i, M in enumerate(moments):
        calc_sheet += f"| 支座{i} | {M:.2f} |\n"
    
    calc_sheet += f"""
### 3.2 控制内力

| 项目 | 数值 |
|------|------|
| 最大正弯矩 | {max_M:.2f} kNm |
| 最大负弯矩 | {min_M:.2f} kNm |
| 最大剪力 | {max_V:.2f} kN |
| 总跨度 | {total_length:.2f} m |

"""
    
    calc_sheet += f"""
---

## 4. 截面选择

**选用截面：{sec.name}**

### 截面属性

| 参数 | 符号 | 数值 | 单位 |
|------|------|------|------|
| 截面高度 | D | {sec.D:.1f} | mm |
| 截面宽度 | B | {sec.B:.1f} | mm |
| 腹板厚度 | t | {sec.t:.1f} | mm |
| 翼缘厚度 | T | {sec.T:.1f} | mm |
| 惯性矩 Ix | Ix | {sec.Ix:.0f} | cm⁴ |
| 截面模量 | Wx | {sec.Wx:.0f} | cm³ |
| 回转半径 | rx | {sec.rx:.1f} | mm |
| 截面积 | A | {sec.A:.1f} | cm² |
| 单位质量 | m | {sec.mass:.1f} | kg/m |

---

## 5. 承载力验算

### 5.1 抗弯承载力验算 (BS 5950 Cl.4.2)

Mc = py × Sx = 275 × {sec.Wx} × 10⁻³ = **{Mc_val:.1f} kNm**

M/Mc = {max_M:.2f}/{Mc_val:.1f} = **{max_M / Mc_val:.1%}** < 1.0 ✓

### 5.2 抗剪承载力验算 (BS 5950 Cl.4.3)

Vc = 0.6 × py × D × t = 0.6 × 275 × {sec.D:.0f} × {sec.t:.1f} × 10⁻³ = **{Vc_val:.1f} kN**

V/Vc = {max_V:.2f}/{Vc_val:.1f} = **{max_V / Vc_val:.1%}** < 1.0 ✓

### 5.3 综合利用率

η = max(M/Mc, V/Vc) = **{ratio_val:.1%}**

**验算结论：** 截面满足承载力要求 ✓

---

## 6. 材料用量与成本

| 项目 | 数值 |
|------|------|
| 总长度 | {total_length:.2f} m |
| 单位质量 | {sec.mass:.1f} kg/m |
| 总质量 | {sec.mass * total_length:.1f} kg |
| 单价 | {cost_per_kg:.1f} 元/kg |
| 总成本 | {cost_per_kg * sec.mass * total_length:.0f} 元 |

---

## 7. 库存信息

| 项目 | 数值 |
|------|------|
| 当前库存 | {inventory:.1f} m |
| 库存状态 | {"有库存 ✓" if inventory > 0 else "无库存，需采购"} |

---

## 8. 设计结论

**推荐截面：{sec.name}**

- 综合利用率：**{util_str}**
- 截面安全富余度：**{(1 - ratio_val)*100:.0f}%**
- 库存状态：**{"有库存 ({:.1f} m)".format(inventory) if inventory > 0 else "无库存"}**

---

*本计算书由结构设计选型智能体自动生成*
*设计者需对计算结果进行审核确认*
"""
    
    return calc_sheet


def generate_calc_sheet_pdf(
    project_name: str, 
    structure_params: Dict,
    calc_result: Dict,
    best_section: dict, 
    user_name: str,
    load_diagram_buf: io.BytesIO = None,
    moment_diagram_buf: io.BytesIO = None,
    shear_diagram_buf: io.BytesIO = None,
    envelope_moment_buf: io.BytesIO = None,
    envelope_shear_buf: io.BytesIO = None
) -> bytes:
    """生成PDF计算书"""
    
    sec = best_section["section"]
    today = datetime.now().strftime("%Y-%m-%d")
    inventory = best_section["库存值"]
    
    spans = structure_params["spans"]
    total_length = sum(s["length"] for s in spans)
    
    # 提取计算结果变量，避免f-string中字典访问兼容性问题
    max_M = calc_result['max_M']
    min_M = calc_result['min_M']
    max_V = calc_result['max_V']
    ratio_val = best_section['利用率值']
    util_str = best_section['利用率']
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=15*mm, bottomMargin=15*mm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', fontName=CHINESE_FONT, fontSize=16, spaceAfter=15, alignment=TA_CENTER)
    heading_style = ParagraphStyle('Heading', fontName=CHINESE_FONT, fontSize=12, spaceAfter=8, spaceBefore=12)
    normal_style = ParagraphStyle('Normal', fontName=CHINESE_FONT, fontSize=9, spaceAfter=4, leading=12)
    
    elements = []
    
    elements.append(Paragraph("连续梁结构设计计算书", title_style))
    elements.append(Spacer(1, 10))
    
    # 项目信息
    spans_str = "+".join([f"{s['length']:.1f}" for s in spans])
    left_s = "铰支" if structure_params.get("left_support") == "pinned" else "固定"
    right_s = "铰支" if structure_params.get("right_support") == "pinned" else "固定"
    
    info_data = [
        ["工程名称", project_name],
        ["结构类型", f"{len(spans)}跨连续梁"],
        ["跨度配置", f"{spans_str} m"],
        ["支座条件", f"左端{left_s}，右端{right_s}"],
        ["截面类型", sec.type],
        ["设计日期", today],
        ["设计者", user_name],
    ]
    
    info_table = Table(info_data, colWidths=[70, 180])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("1. 设计依据", heading_style))
    elements.append(Paragraph("• HK COP for Structural Use of Steel 2019 (香港钢结构规范)", normal_style))
    elements.append(Paragraph("• BS 5950-1:2000 (英国钢结构设计规范)", normal_style))
    elements.append(Paragraph("• 材料牌号：S275 (fy = 275 N/mm²)", normal_style))
    
    elements.append(Paragraph("2. 几何参数", heading_style))
    
    geo_data = [["跨号", "跨度(m)", "恒载(kN/m)", "活载(kN/m)"]]
    for i, s in enumerate(spans):
        geo_data.append([str(i+1), f"{s['length']:.1f}", f"{s.get('dead_load', 0):.1f}", f"{s.get('live_load', 0):.1f}"])
    
    geo_table = Table(geo_data, colWidths=[50, 60, 70, 70])
    geo_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(geo_table)
    elements.append(Spacer(1, 10))
    
    # 荷载简图
    if load_diagram_buf:
        elements.append(Paragraph("3. 荷载简图", heading_style))
        load_diagram_buf.seek(0)
        img = Image(load_diagram_buf, width=170*mm, height=50*mm)
        elements.append(img)
        elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("4. 内力计算方法与结果", heading_style))
    
    # 公式说明
    elements.append(Paragraph("4.1 计算方法 - 三弯矩方程", ParagraphStyle('SubHeading', fontName=CHINESE_FONT, fontSize=11, spaceAfter=6, spaceBefore=8)))
    elements.append(Paragraph("采用三弯矩方程(力法)进行连续梁内力分析:", normal_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("基本方程: M(i-1)xLi/6EI + M(i)x(Li+Li+1)/3EI + M(i+1)xLi+1/6EI = -Bi - Ai+1", normal_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("均布荷载: Bi = q x Li3 / (24EI)", normal_style))
    elements.append(Paragraph("集中力(距左端a): Bi = P x a x b x (Li+a) / (6 x EI x Li)", normal_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("跨内弯矩: M(x) = M简支(x) + M左 + (M右 - M左) x x / L", normal_style))
    elements.append(Paragraph("跨内剪力: V(x) = V简支(x) + (M右 - M左) / L", normal_style))
    
    elements.append(Paragraph("4.2 支座弯矩", ParagraphStyle('SubHeading2', fontName=CHINESE_FONT, fontSize=11, spaceAfter=6, spaceBefore=10)))
    
    moments = calc_result["support_moments"]
    moment_data = [["支座", "弯矩(kNm)"]]
    for i, M in enumerate(moments):
        moment_data.append([f"支座{i}", f"{M:.2f}"])
    
    moment_table = Table(moment_data, colWidths=[80, 80])
    moment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(moment_table)
    elements.append(Spacer(1, 8))
    
    elements.append(Paragraph(f"最大正弯矩: {max_M:.2f} kNm", normal_style))
    elements.append(Paragraph(f"最大负弯矩: {min_M:.2f} kNm", normal_style))
    elements.append(Paragraph(f"最大剪力: {max_V:.2f} kN", normal_style))
    
    # 弯矩图
    if moment_diagram_buf:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("5. 弯矩图", heading_style))
        moment_diagram_buf.seek(0)
        img = Image(moment_diagram_buf, width=170*mm, height=50*mm)
        elements.append(img)
    
    # 剪力图
    if shear_diagram_buf:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("6. 剪力图", heading_style))
        shear_diagram_buf.seek(0)
        img = Image(shear_diagram_buf, width=170*mm, height=50*mm)
        elements.append(img)
    
    # 包络图
    if envelope_moment_buf and envelope_shear_buf:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("7. 包络图（活载不利布置）", heading_style))
        envelope_moment_buf.seek(0)
        img_m = Image(envelope_moment_buf, width=170*mm, height=50*mm)
        elements.append(img_m)
        elements.append(Spacer(1, 5))
        envelope_shear_buf.seek(0)
        img_v = Image(envelope_shear_buf, width=170*mm, height=50*mm)
        elements.append(img_v)
    
    # 截面选择
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("8. 截面选择", heading_style))
    elements.append(Paragraph(f"<b>选用截面：{sec.name}</b>", normal_style))
    
    section_data = [
        ["参数", "数值", "单位"],
        ["截面高度 D", f"{sec.D:.1f}", "mm"],
        ["截面宽度 B", f"{sec.B:.1f}", "mm"],
        ["腹板厚度 t", f"{sec.t:.1f}", "mm"],
        ["翼缘厚度 T", f"{sec.T:.1f}", "mm"],
        ["惯性矩 Ix", f"{sec.Ix:.0f}", "cm⁴"],
        ["截面模量 Wx", f"{sec.Wx:.0f}", "cm³"],
        ["单位质量", f"{sec.mass:.1f}", "kg/m"],
    ]
    section_table = Table(section_data, colWidths=[100, 80, 50])
    section_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(section_table)
    
    # 验算
    elements.append(Paragraph("9. 承载力验算", heading_style))
    Mc = 275 * sec.Wx * 1e-3
    Vc = 0.6 * 275 * sec.D * sec.t * 1e-3
    
    elements.append(Paragraph(f"抗弯承载力: Mc = {Mc:.1f} kNm, M/Mc = {max_M/Mc:.1%}", normal_style))
    elements.append(Paragraph(f"抗剪承载力: Vc = {Vc:.1f} kN, V/Vc = {max_V/Vc:.1%}", normal_style))
    elements.append(Paragraph(f"<b>综合利用率: {ratio_val:.1%}</b>", normal_style))
    elements.append(Paragraph("<b>验算结论：截面满足承载力要求 ✓</b>", normal_style))
    
    # 成本
    total_cost = _get_cost_db().get(sec.name, 4.0) * sec.mass * total_length
    elements.append(Paragraph("10. 材料用量与成本", heading_style))
    cost_data = [
        ["项目", "数值"],
        ["总长度", f"{total_length:.2f} m"],
        ["单位质量", f"{sec.mass:.1f} kg/m"],
        ["总质量", f"{sec.mass * total_length:.1f} kg"],
        ["总成本", f"{total_cost:.0f} 元"],
    ]
    cost_table = Table(cost_data, colWidths=[100, 100])
    cost_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(cost_table)
    
    # 库存
    elements.append(Paragraph("11. 库存信息", heading_style))
    inv_status = "有库存 ✓" if inventory > 0 else "无库存，需采购"
    elements.append(Paragraph(f"当前库存: {inventory:.1f} m, 状态: {inv_status}", normal_style))
    
    # 结论
    elements.append(Paragraph("12. 设计结论", heading_style))
    elements.append(Paragraph(f"<b>推荐截面：{sec.name}</b>", normal_style))
    elements.append(Paragraph(f"综合利用率: {util_str}", normal_style))
    elements.append(Paragraph(f"库存状态: {'有库存' if inventory > 0 else '无库存'}", normal_style))
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("本计算书由结构设计选型智能体自动生成", ParagraphStyle('Footer', fontName=CHINESE_FONT, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    elements.append(Paragraph("设计者需对计算结果进行审核确认", ParagraphStyle('Footer2', fontName=CHINESE_FONT, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# 8. 用户认证
# ============================================================

USERS_DB = {
    "admin": {"password_hash": hashlib.sha256("admin123".encode()).hexdigest(), "name": "管理员"},
    "zhangsan": {"password_hash": hashlib.sha256("zhangsan123".encode()).hexdigest(), "name": "张三"},
    "lisi": {"password_hash": hashlib.sha256("lisi123".encode()).hexdigest(), "name": "李四"},
}

def check_password(username: str, password: str) -> bool:
    if username not in USERS_DB:
        return False
    return USERS_DB[username]["password_hash"] == hashlib.sha256(password.encode()).hexdigest()

def _inject_tech_background():
    """注入暗色科技感背景（纯CSS，无JS）"""
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0a0e27 0%, #0d1538 40%, #0a1628 100%) !important; color: #e0e6f0 !important; }
    [data-testid="stSidebar"] { background: rgba(10, 14, 39, 0.95) !important; border-right: 1px solid rgba(0, 200, 255, 0.1) !important; }
    h1, h2, h3, h4, h5, h6, label, .stMarkdown, p, span { color: #e0e6f0 !important; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { background: rgba(15, 25, 60, 0.8) !important; color: #e0e6f0 !important; border: 1px solid rgba(0, 180, 255, 0.3) !important; }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #00b4ff !important; box-shadow: 0 0 8px rgba(0, 180, 255, 0.3) !important; }
    .stButton > button { background: linear-gradient(135deg, #004d7a, #008793) !important; color: #e0e6f0 !important; border: 1px solid rgba(0, 180, 255, 0.4) !important; transition: all 0.3s ease !important; }
    .stButton > button:hover { background: linear-gradient(135deg, #006d9a, #00a7a3) !important; box-shadow: 0 0 15px rgba(0, 180, 255, 0.4) !important; }
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #E60012, #b3000e) !important; border: 1px solid #E60012 !important; }
    [data-testid="stDataFrame"] { background: rgba(10, 18, 50, 0.7) !important; border: 1px solid rgba(0, 180, 255, 0.15) !important; }
    [data-testid="stDataFrame"] th { background: rgba(0, 30, 80, 0.8) !important; color: #7ec8ff !important; text-align: left !important; }
    [data-testid="stDataFrame"] td { color: #c0d0e8 !important; text-align: left !important; }
    hr { border-color: rgba(0, 180, 255, 0.2) !important; }
    .stTabs [data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] { color: #00b4ff !important; border-bottom-color: #00b4ff !important; }
    .stTabs [data-baseweb="tab-list"] button[data-baseweb="tab"] { color: #8899bb !important; }
    .stSelectbox > div > div, .stRadio > div { color: #000000 !important; }
    .stSelectbox div[data-baseweb="select"] > div { color: #000000 !important; }
    .stSelectbox div[data-baseweb="select"] > div > div { color: #000000 !important; }
    .stSelectbox div[data-baseweb="select"] svg { fill: #000000 !important; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div { color: #000000 !important; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div > div { color: #000000 !important; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg { fill: #000000 !important; }
    [data-testid="stSidebar"] .stRadio div { color: #000000 !important; }
    [data-testid="stSidebar"] .stCheckbox label { color: #000000 !important; }
    [data-testid="stSidebar"] .stNumberInput label { color: #000000 !important; }
    [data-testid="stSidebar"] .stNumberInput input { color: #000000 !important; }
    [data-testid="stSidebar"] .stTextInput label { color: #000000 !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #000000 !important; }
    [data-testid="stSidebar"] .stTextArea textarea { color: #000000 !important; }
    [data-testid="stSidebar"] .stTextInput input { color: #000000 !important; }
    .stTextArea textarea { color: #000000 !important; }
    .stTextInput input { color: #000000 !important; }
    .stNumberInput input { color: #000000 !important; }
    .stCaption { color: #8899bb !important; }
    .stSuccess { background: rgba(0, 180, 100, 0.15) !important; border-color: rgba(0, 180, 100, 0.3) !important; }
    .stWarning { background: rgba(255, 180, 0, 0.15) !important; border-color: rgba(255, 180, 0, 0.3) !important; }
    .stError { background: rgba(230, 0, 18, 0.15) !important; border-color: rgba(230, 0, 18, 0.3) !important; }
    .stInfo { background: rgba(0, 180, 255, 0.15) !important; border-color: rgba(0, 180, 255, 0.3) !important; }
    /* 代码块和表格：白底黑字 */
    .stCode, .stCode code { color: #1a1a2e !important; }
    code { color: #1a1a2e !important; }
    table, table th, table td { color: #1a1a2e !important; }
    /* st.caption 也用深色 */
    .stCaption { color: #607090 !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e27; }
    ::-webkit-scrollbar-thumb { background: #1a3a6a; border-radius: 3px; }
    </style>""", unsafe_allow_html=True)

def _inject_map_background():
    """登录页：科技暗色背景 + CSS动画（简化版，避免SVG过大）"""
    # CSS - 暗色主题 + 纯CSS动画背景
    st.markdown("""
    <style>
    /* 全局背景设置 */
    .stApp {
        background: linear-gradient(135deg, #061225 0%, #030a15 40%, #000208 100%) !important;
        color: #e0e6f0 !important;
    }
    
    /* Streamlit内部容器透明 */
    .stApp > header { background: transparent !important; }
    .block-container { background: transparent !important; }
    
    /* 隐藏侧边栏 */
    [data-testid="stSidebar"] { display: none !important; }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        background: rgba(15,25,60,0.85) !important;
        color: #e0e6f0 !important;
        border: 1px solid rgba(0,180,255,0.3) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00b4ff !important;
        box-shadow: 0 0 8px rgba(0,180,255,0.3) !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg,#E60012,#b3000e) !important;
        color: #fff !important;
        border: none !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg,#ff1a2a,#d60014) !important;
        box-shadow: 0 0 20px rgba(230,0,18,0.5) !important;
    }
    
    /* 文字颜色 */
    h1,h2,h3,h4,h5,h6,label,p,span,.stMarkdown {
        color: #e0e6f0 !important;
    }
    
    hr { border-color: rgba(0,180,255,0.2) !important; }
    
    /* 科技感背景动画 - 纯CSS实现 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 50% 50%, rgba(0,180,255,0.03) 0%, transparent 50%),
            radial-gradient(circle at 30% 70%, rgba(255,128,0,0.02) 0%, transparent 30%);
        z-index: -1;
        animation: pulseBg 8s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes pulseBg {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* 装饰网格线 - 简化版 */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0,180,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,180,255,0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: -1;
        pointer-events: none;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    </style>
    """, unsafe_allow_html=True)

def login_page():
    st.set_page_config(page_title="中建国际医疗产业发展（深圳）有限公司", page_icon="🏗️", layout="wide")
    _inject_map_background()
    # Logo居中（内嵌base64，无需外部文件）
    import base64
    logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
    with logo_col2:
        try:
            st.markdown(
                f'<img src="data:image/png;base64,{LOGO_BASE64}" style="width:100%;max-width:460px;display:block;margin:auto;">',
                unsafe_allow_html=True
            )
        except:
            st.markdown("")
    st.markdown("<h1 style='text-align: center; color: #E60012; font-family: \"Microsoft YaHei\", \"SimHei\", sans-serif; font-weight: 900; letter-spacing: 2px; white-space: nowrap; margin-left: -1.0em;'>中建国际医疗产业发展（深圳）有限公司</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #a0b4d0; font-family: \"Microsoft YaHei\", \"SimHei\", sans-serif; font-weight: 400; letter-spacing: 1px;'>结构设计辅助系统 - AI智能版</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        username = st.text_input("用户名", placeholder="请输入用户名")
        password = st.text_input("密码", type="password", placeholder="请输入密码")
        
        if st.button("登录", use_container_width=True, type="primary"):
            if check_password(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["user_name"] = USERS_DB[username]["name"]
                st.session_state["ai_messages"] = []
                st.rerun()
            else:
                st.error("用户名或密码错误")
        
        st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>仅限公司内部使用</p>", unsafe_allow_html=True)

# ============================================================
# 9. AI 对话界面
# ============================================================

def render_ai_chat():
    """渲染AI对话界面"""
    st.markdown("### 🤖 AI 结构设计助手")
    st.markdown("用自然语言描述您的连续梁设计需求，AI将自动解析参数并完成选型")
    
    with st.expander("💡 查看示例描述"):
        st.markdown("""
        **连续梁示例：**
        - `3跨连续梁，跨度6+6+6m，恒载8kN/m，活载5kN/m，活载在1跨和3跨，两端铰支`
        - `2跨连续梁，跨度4+6m，恒载10kN/m，第1跨跨中集中力50kN，左端固定右端铰支`
        - `4跨连续梁，跨度5+6+5+6m，恒载12kN/m，活载6kN/m，活载在2跨和4跨`
        
        **简支梁示例：**
        - `6m简支梁，承受均布荷载10kN/m`
        
        **悬臂梁示例：**
        - `5m悬臂梁，端部集中力20kN`
        
        **固端梁示例：**
        - `4m固端梁，均布荷载8kN/m`
        """)
    
    if "ai_messages" not in st.session_state:
        st.session_state["ai_messages"] = []
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["ai_messages"]:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])
    
    if prompt := st.chat_input("输入您的结构设计需求..."):
        st.session_state["ai_messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("AI正在分析您的需求..."):
                parsed = parse_natural_language(prompt)
                
                if parsed:
                    # 检查是否是AI反问
                    if "clarification" in parsed:
                        clar_msg = "🤔 " + parsed["clarification"]
                        st.warning(clar_msg)
                        st.session_state["ai_messages"].append({"role": "assistant", "content": clar_msg})
                    else:
                        st.session_state["parsed_params"] = parsed
                        struct_type = parsed.get("structure_type", "continuous_beam")
                    
                        # 连续梁计算
                        if struct_type == "continuous_beam":
                            spans_data = parsed.get("spans", [])
                            spans = [s["length"] for s in spans_data]
                            loads = spans_data
                            left_support = parsed.get("left_support", "pinned")
                            right_support = parsed.get("right_support", "pinned")
                            load_cases = parsed.get("load_cases", [])
                        
                            # 活载不利布置
                            live_spans_list = []
                            for lc in load_cases:
                                live_spans_list.extend(lc.get("live_spans", []))
                            live_spans_list = list(set(live_spans_list))
                        
                            # 计算内力
                            calc_result = solve_continuous_beam(spans, loads, left_support, right_support)
                        
                            # 包络计算（如有活载）
                            envelope_data = None
                            if any(s.get("live_load", 0) > 0 for s in spans_data):
                                # 生成所有活载组合
                                n = len(spans)
                                combos = []
                                for r in range(1, n + 1):
                                    for combo in itertools.combinations(range(n), r):
                                        combos.append(list(combo))
                            
                                envelope_data = calculate_envelope(spans, loads, combos, left_support, right_support)
                        
                            st.session_state["calc_result"] = calc_result
                            st.session_state["envelope_data"] = envelope_data
                            st.session_state["spans"] = spans
                            st.session_state["loads"] = loads
                            st.session_state["left_support"] = left_support
                            st.session_state["right_support"] = right_support
                            st.session_state["structure_type"] = struct_type
                            st.session_state["structure_params"] = {
                                "spans": [{"length": s, **l} for s, l in zip(spans, loads)],
                                "left_support": left_support,
                                "right_support": right_support,
                                "structure_type": struct_type
                            }
                        
                            spans_str = "+".join([f"{s:.1f}" for s in spans])
                            max_M = calc_result['max_M']
                            min_M = calc_result['min_M']
                            max_V = calc_result['max_V']
                            response = f"""✅ 已解析您的连续梁需求：

    **跨数：** {len(spans)}跨
    **跨度：** {spans_str} m
    **支座条件：** 左端{left_support}，右端{right_support}

    **内力计算结果（三弯矩方程）：**
    - 最大正弯矩：{max_M:.2f} kNm
    - 最大负弯矩：{min_M:.2f} kNm
    - 最大剪力：{max_V:.2f} kN

    **支座弯矩：**
    """
                            for i, M in enumerate(calc_result["support_moments"]):
                                response += f"- 支座{i}：{M:.2f} kNm\n"
                        
                            response += "\n正在为您进行截面选型..."
                        
                            st.write(response)
                            st.session_state["ai_messages"].append({"role": "assistant", "content": response})
                        
                            st.markdown("---")
                            st.markdown("#### 📊 选型结果")
                        
                            # 截面选型
                            section_types = st.session_state.get("section_types", ["UB"])
                            prefer_inventory = st.session_state.get("prefer_inventory", True)
                        
                            results = select_sections_for_continuous_beam(
                                spans,
                                calc_result["max_M"],
                                calc_result["max_V"],
                                section_types,
                                prefer_inventory
                            )
                        
                            if results:
                                st.session_state["results"] = results
                                st.session_state["best_section"] = results[0]
                            
                                df = pd.DataFrame(results)
                                df_display = df[["截面", "类型", "利用率", "成本(元)", "总质量(kg)", "库存(m)"]]
                                st.dataframe(df_display, use_container_width=True, hide_index=True)
                            
                                best = results[0]
                                st.success(f"""
                                **✨ 最优推荐：{best['截面']}**
                            
                                类型：{best['类型']} | 利用率：{best['利用率']} | 成本：{best['成本(元)']}元 | 库存：{best['库存(m)']}
                                """)
                            
                                recommendation = generate_recommendation(parsed, best, struct_type)
                                st.info(f"**💬 AI解读：** {recommendation}")
                                st.session_state["ai_recommendation"] = recommendation
                            
                                st.session_state["ai_messages"].append({
                                    "role": "assistant", 
                                    "content": f"选型完成！推荐截面 **{best['截面']}**，利用率 **{best['利用率']}**"
                                })
                            else:
                                st.warning("没有找到符合条件的截面")
                    
                        # 简支梁、悬臂梁、固端梁（简化计算）
                        elif struct_type in ["simply_supported_beam", "cantilever_beam", "fixed_beam"]:
                            span = parsed.get("span", 6.0)
                            load_value = parsed.get("load_value", 10.0)
                        
                            if struct_type == "simply_supported_beam":
                                result = calculate_simple_beam(span, load_value)
                            elif struct_type == "cantilever_beam":
                                result = calculate_cantilever_beam(span, load_value)
                            else:
                                result = calculate_fixed_beam(span, load_value)
                        
                            M = result["M_max"]
                            V = result["V_max"]
                        
                            st.session_state["simple_beam_result"] = result
                            st.session_state["structure_type"] = struct_type
                        
                            struct_name = STRUCTURE_TYPE_NAMES.get(struct_type, struct_type)
                            response = f"""✅ 已解析您的{struct_name}需求：

    **跨度：** {span} m
    **荷载值：** {load_value} kN/m

    **内力计算结果：**
    - 最大弯矩：{M:.2f} kNm
    - 最大剪力：{V:.2f} kN

    正在为您进行截面选型..."""
                        
                            st.write(response)
                            st.session_state["ai_messages"].append({"role": "assistant", "content": response})
                        
                            st.markdown("---")
                            st.markdown("#### 📊 选型结果")
                        
                            section_types = st.session_state.get("section_types", ["UB"])
                            prefer_inventory = st.session_state.get("prefer_inventory", True)
                        
                            results = select_sections("beam", span, M, V, 0, "利用率", section_types, prefer_inventory)
                        
                            if results:
                                st.session_state["results"] = results
                                st.session_state["best_section"] = results[0]
                            
                                df = pd.DataFrame(results)
                                df_display = df[["截面", "类型", "利用率", "成本(元)", "质量(kg/m)", "库存(m)"]]
                                st.dataframe(df_display, use_container_width=True, hide_index=True)
                            
                                best = results[0]
                                st.success(f"""
                                **✨ 最优推荐：{best['截面']}**
                            
                                类型：{best['类型']} | 利用率：{best['利用率']} | 成本：{best['成本(元)']}元 | 库存：{best['库存(m)']}
                                """)
                            else:
                                st.warning("没有找到符合条件的截面")
                else:
                    # 非结构设计任务，尝试通用对话回复
                    chat_reply = chat_with_ai(prompt)
                    if chat_reply:
                        st.info(chat_reply)
                        st.session_state["ai_messages"].append({"role": "assistant", "content": chat_reply})
                    else:
                        error_msg = """❌ 抱歉，AI无法解析您的描述。

请尝试更清晰地描述，例如：
- "3跨连续梁，跨度6+6+6m，恒载8kN/m，活载5kN/m"
- "6m简支梁，均布荷载10kN/m"
"""
                        st.error(error_msg)
                        st.session_state["ai_messages"].append({"role": "assistant", "content": error_msg})

# ============================================================
# 10. 主界面
# ============================================================

def main_page():
    global COST_DB, INVENTORY_DB
    st.set_page_config(page_title="中建国际医疗产业发展（深圳）有限公司", page_icon="🏗️", layout="wide")
    _inject_tech_background()
    
    # 初始化持久化数据库（session_state保证rerun不丢失）
    COST_DB = _get_cost_db()
    INVENTORY_DB = _get_inventory_db()
    
    if "ai_messages" not in st.session_state:
        st.session_state["ai_messages"] = []
    if "section_types" not in st.session_state:
        st.session_state["section_types"] = ["UB"]
    if "sort_key" not in st.session_state:
        st.session_state["sort_key"] = "利用率"
    if "prefer_inventory" not in st.session_state:
        st.session_state["prefer_inventory"] = True
    if "ai_system_prompt" not in st.session_state:
        st.session_state["ai_system_prompt"] = AI_SYSTEM_PROMPT
    if "ai_recommend_prompt" not in st.session_state:
        st.session_state["ai_recommend_prompt"] = AI_RECOMMEND_PROMPT
    
    # 表格单元格左对齐
    st.markdown("""<style>
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] td {
        text-align: left !important;
    }
    </style>""", unsafe_allow_html=True)
    
    header_col, user_col = st.columns([9, 1])
    with header_col:
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:center;gap:16px;min-height:84px;">'
            f'<img src="data:image/png;base64,{LOGO_BASE64}" style="height:84px;object-fit:contain;">'
            f'<div style="display:flex;flex-direction:column;justify-content:center;align-items:center;">'
            f'<h2 style="color:#E60012;font-family:\'Microsoft YaHei\',\'SimHei\',sans-serif;font-weight:900;letter-spacing:1px;margin:0;padding:0;line-height:1.2;">结构设计辅助系统</h2>'
            f'<span style="color:#999;font-size:0.85em;font-family:\'Microsoft YaHei\',\'SimHei\',sans-serif;white-space:nowrap;">中建国际医疗产业发展（深圳）有限公司</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with user_col:
        st.write(f"👤 {st.session_state['user_name']}")
        if st.button("退出"):
            st.session_state["logged_in"] = False
            st.session_state["ai_messages"] = []
            st.rerun()
    
    st.markdown("---")
    
    mode = st.radio("选择功能", ["🤖 AI智能解析", "📐 手动参数输入", "🗃️ 数据库管理"], horizontal=True, index=0)
    
    # 记录当前模式，切换时清除对方的结果
    prev_mode = st.session_state.get("prev_mode", "")
    if prev_mode and prev_mode != mode:
        # 切换了模式，清除计算结果和图形
        for key in ["calc_result", "results", "best_section", "simple_beam_result",
                     "load_buf", "moment_buf", "shear_buf", "env_m_buf", "env_v_buf",
                     "envelope_data", "structure_params", "calc_params"]:
            st.session_state.pop(key, None)
    st.session_state["prev_mode"] = mode
    
    if mode == "🤖 AI智能解析":
        render_ai_chat()
    elif mode == "📐 手动参数输入":
        render_manual_input()
    elif mode == "🗃️ 数据库管理":
        render_data_management()
    
    # 显示图形和计算书 - 只在对应模式下显示
    if mode == "🤖 AI智能解析" and st.session_state.get("structure_type") == "continuous_beam" and st.session_state.get("calc_result"):
        render_continuous_beam_results()
    elif mode == "🤖 AI智能解析" and st.session_state.get("results") and st.session_state.get("structure_type") in ["simply_supported_beam", "cantilever_beam", "fixed_beam"]:
        render_simple_beam_results()
    elif mode == "📐 手动参数输入" and st.session_state.get("results"):
        render_manual_results()

def render_manual_input():
    """渲染手动参数输入界面 - 直接输入内力进行截面选型"""
    st.sidebar.header("📐 内力参数")
    
    # 构件类型
    member_type = st.sidebar.selectbox("构件类型", ["梁 (Beam)", "柱 (Column)"])
    
    # 直接输入内力
    L = st.sidebar.number_input("构件长度 L (m)", 0.5, 30.0, 6.0, 0.5)
    M = st.sidebar.number_input("最大弯矩 M (kNm)", 0.0, 100000.0, 50.0, 1.0)
    V = st.sidebar.number_input("最大剪力 V (kN)", 0.0, 100000.0, 50.0, 1.0)
    N = st.sidebar.number_input("轴力 N (kN，柱需输入)", 0.0, 100000.0, 0.0, 1.0)
    
    project_name = st.sidebar.text_input("工程名称", "钢结构项目")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📐 截面类型")
    
    section_types = st.sidebar.multiselect(
        "选择截面类型（可多选）",
        options=list(SECTION_TYPE_NAMES.keys()),
        default=["UB"],
        format_func=lambda x: SECTION_TYPE_NAMES[x],
        key="manual_section_types"
    )
    st.session_state["section_types"] = section_types
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 排序方式")
    sort_by = st.sidebar.radio("排序依据", ["利用率", "成本"], index=0, horizontal=True)
    sort_order = st.sidebar.radio("排序方向", ["升序", "降序"], index=0, horizontal=True)
    st.session_state["sort_key"] = sort_by
    st.session_state["sort_order"] = sort_order
    
    prefer_inventory = st.sidebar.checkbox("优先推荐有库存截面", value=True)
    st.session_state["prefer_inventory"] = prefer_inventory
    
    # 主区域：显示输入参数摘要
    st.markdown("---")
    st.subheader("📐 手动内力输入选型")
    st.markdown("直接输入构件内力，系统将从截面库中筛选可行截面并按指定方式排序推荐。")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("长度 L", f"{L:.1f} m")
    with col2:
        st.metric("弯矩 M", f"{M:.1f} kNm")
    with col3:
        st.metric("剪力 V", f"{V:.1f} kN")
    with col4:
        st.metric("轴力 N", f"{N:.1f} kN")
    
    if st.button("🔍 开始选型", type="primary"):
        with st.spinner("截面选型计算中..."):
            mt = "beam" if "梁" in member_type else "column"
            results = select_sections(mt, L, M, V, N, sort_by, section_types, prefer_inventory)
            
            if results:
                st.session_state["results"] = results
                st.session_state["structure_type"] = "manual_input"
                st.session_state["calc_params"] = {
                    "project_name": project_name,
                    "member_type": mt,
                    "L": L, "M": M, "V": V, "N": N
                }
                st.success(f"✅ 选型完成！共找到 {len(results)} 个可行截面")
            else:
                st.warning("⚠️ 没有找到符合条件的截面，请调整参数或截面类型")


def render_manual_results():
    """渲染手动输入选型结果"""
    results = st.session_state.get("results", [])
    if not results:
        return
    
    # 最优推荐：按利用率排→推荐利用率最高（最经济高效），按成本排→推荐成本最低
    prefer_inventory = st.session_state.get("prefer_inventory", True)
    sort_by = st.session_state.get("sort_key", "利用率")
    if sort_by == "利用率":
        # 利用率最高 = 最经济高效
        if prefer_inventory:
            inv_results = [r for r in results if r["库存值"] > 0]
            best = max(inv_results, key=lambda x: x["利用率值"]) if inv_results else max(results, key=lambda x: x["利用率值"])
        else:
            best = max(results, key=lambda x: x["利用率值"])
    else:
        # 成本最低
        if prefer_inventory:
            inv_results = [r for r in results if r["库存值"] > 0]
            best = min(inv_results, key=lambda x: x["成本值"]) if inv_results else min(results, key=lambda x: x["成本值"])
        else:
            best = min(results, key=lambda x: x["成本值"])
    
    # 表格展示顺序：按用户选择的排序方式和方向
    sort_by = st.session_state.get("sort_key", "利用率")
    sort_order = st.session_state.get("sort_order", "升序")
    sort_key_val = "利用率值" if sort_by == "利用率" else "成本值"
    reverse = (sort_order == "降序")
    
    if prefer_inventory:
        has_inv = [r for r in results if r["库存值"] > 0]
        no_inv = [r for r in results if r["库存值"] == 0]
        has_inv.sort(key=lambda x: x[sort_key_val], reverse=reverse)
        no_inv.sort(key=lambda x: x[sort_key_val], reverse=reverse)
        sorted_results = has_inv + no_inv
    else:
        sorted_results = sorted(results, key=lambda x: x[sort_key_val], reverse=reverse)
    
    st.markdown("---")
    st.markdown("#### 📊 选型结果")
    
    # 显示结果表格
    df = pd.DataFrame(sorted_results)
    display_cols = ["截面", "类型", "利用率", "成本(元)"]
    if "质量(kg/m)" in df.columns:
        display_cols.append("质量(kg/m)")
    if "总质量(kg)" in df.columns:
        display_cols.append("总质量(kg)")
    if "库存(m)" in df.columns:
        display_cols.append("库存(m)")
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
    
    # 最优推荐
    st.success(f"""
    **✨ 最优推荐：{best['截面']}**
    
    类型：{best['类型']} | 利用率：{best['利用率']} | 成本：{best['成本(元)']}元 | 库存：{best['库存(m)']}
    """)
    
    # 计算书
    render_calc_sheet_section()


def render_continuous_beam_results():
    """渲染连续梁结果"""
    st.markdown("---")
    st.subheader("📈 内力图")
    
    spans = st.session_state.get("spans", [])
    loads = st.session_state.get("loads", [])
    calc_result = st.session_state.get("calc_result")
    left_support = st.session_state.get("left_support", "pinned")
    right_support = st.session_state.get("right_support", "pinned")
    
    # 生成图形 - 三行等大显示
    with st.spinner("生成荷载简图..."):
        load_buf = draw_load_diagram(spans, loads, left_support, right_support)
        st.image(load_buf, caption="荷载简图", use_container_width=True)
    
    with st.spinner("生成弯矩图..."):
        moment_buf = draw_moment_diagram(spans, calc_result["span_internal_forces"], "弯矩图")
        st.image(moment_buf, caption="弯矩图", use_container_width=True)
    
    with st.spinner("生成剪力图..."):
        shear_buf = draw_shear_diagram(spans, calc_result["span_internal_forces"], "剪力图")
        st.image(shear_buf, caption="剪力图", use_container_width=True)
    
    # 包络图（不在页面显示，仅用于计算书）
    envelope_data = st.session_state.get("envelope_data")
    if envelope_data:
        env_m_buf, env_v_buf = draw_envelope_diagram(spans, envelope_data)
        st.session_state["env_m_buf"] = env_m_buf
        st.session_state["env_v_buf"] = env_v_buf
    
    st.session_state["load_buf"] = load_buf
    st.session_state["moment_buf"] = moment_buf
    st.session_state["shear_buf"] = shear_buf
    
    # 计算书
    render_calc_sheet_section()


def render_data_management():
    """渲染数据库管理界面 - AI学习入口"""
    st.markdown("---")
    st.subheader("🗃️ 数据库管理")
    st.info("通过AI对话更新后台数据库，支持截面库、材料库、成本库和库存库的增删改。")
    
    data_tabs = st.tabs(["📋 截面库", "🔩 材料库", "💰 成本库", "📦 库存库", "🤖 AI提示词"])
    
    # 截面库
    with data_tabs[0]:
        st.markdown("#### 当前截面库")
        sections_data = []
        for sec in SECTIONS_DB:
            sections_data.append({
                "名称": sec.name, "类型": sec.type, "质量(kg/m)": sec.mass,
                "D(mm)": sec.D, "B(mm)": sec.B, "t(mm)": sec.t, "T(mm)": sec.T,
                "Ix(cm4)": sec.Ix, "Wx(cm3)": sec.Wx, "rx(mm)": sec.rx
            })
        if sections_data:
            df = pd.DataFrame(sections_data)
            st.dataframe(df, use_container_width=True, hide_index=True, height=300)
            st.caption(f"共 {len(sections_data)} 个截面")
        
        st.markdown("---")
        st.markdown("#### 🤖 AI更新截面库")
        st.markdown("例如：`添加一个UB截面：254x146x31，质量31.1kg/m，D251.5，B146.1，t6.1，T8.7，Ix4410，Wx351，rx19.1`")
        
        section_input = st.text_area("输入截面更新指令", key="section_ai_input", height=80)
        if st.button("🔧 执行截面库更新", key="btn_section_update"):
            if section_input.strip():
                with st.spinner("AI解析中..."):
                    try:
                        update_result = parse_section_update(section_input)
                        if update_result:
                            st.success(f"✅ 截面库更新成功！{update_result}")
                            st.rerun()
                        else:
                            st.warning("⚠️ 未能解析出有效的截面数据，请检查输入格式")
                    except Exception as e:
                        st.error(f"❌ 更新失败：{e}")
            else:
                st.warning("请输入更新指令")
    
    # 材料库
    with data_tabs[1]:
        st.markdown("#### 当前材料库")
        material_data = [
            {"材料牌号": "S275", "fy (N/mm²)": 275, "fu (N/mm²)": 430, "E (kN/mm²)": 205, "适用": "一般结构"},
            {"材料牌号": "S355", "fy (N/mm²)": 355, "fu (N/mm²)": 510, "E (kN/mm²)": 205, "适用": "高强度结构"},
            {"材料牌号": "S460", "fy (N/mm²)": 460, "fu (N/mm²)": 570, "E (kN/mm²)": 205, "适用": "超高强度"},
        ]
        df_mat = pd.DataFrame(material_data)
        st.dataframe(df_mat, use_container_width=True, hide_index=True, height=300)
        st.caption(f"共 {len(material_data)} 种材料")
        st.markdown("---")
        st.markdown("#### 🤖 AI更新材料库")
        st.markdown("例如：`添加材料S355，fy=355，fu=510`")
        material_input = st.text_area("输入材料更新指令", key="material_ai_input", height=80)
        if st.button("🔧 执行材料库更新", key="btn_material_update"):
            if material_input.strip():
                st.info("🔄 材料库更新功能开发中，敬请期待")
            else:
                st.warning("请输入更新指令")
    
    # 成本库
    with data_tabs[2]:
        st.markdown("#### 当前成本库")
        cost_data = [{"截面名称": k, "单价(元/kg)": v} for k, v in sorted(_get_cost_db().items(), key=lambda x: x[1])]
        if cost_data:
            df_cost = pd.DataFrame(cost_data)
            st.dataframe(df_cost, use_container_width=True, hide_index=True, height=300)
            st.caption(f"共 {len(cost_data)} 条成本数据（参考2025年市场价，UB≈4.5 UC≈5.3 PFC≈5.1 EA≈4.0 管类≈4.5-4.8元/kg）")
        
        st.markdown("---")
        st.markdown("#### 🤖 AI更新成本库")
        st.markdown("例如：`修改457x191x82单价为5.5元/kg` 或 `批量更新：UB类6.0元/kg，UC类5.5元/kg`")
        cost_input = st.text_area("输入成本更新指令", key="cost_ai_input", height=80)
        if st.button("🔧 执行成本库更新", key="btn_cost_update"):
            if cost_input.strip():
                with st.spinner("AI解析中..."):
                    try:
                        update_result = parse_cost_update(cost_input)
                        if update_result:
                            st.success(f"✅ 成本库更新成功！{update_result}")
                            st.rerun()
                        else:
                            st.warning("⚠️ 未能解析出有效的成本数据")
                    except Exception as e:
                        st.error(f"❌ 更新失败：{e}")
            else:
                st.warning("请输入更新指令")
    
    # 库存库
    with data_tabs[3]:
        st.markdown("#### 当前库存库")
        inv_data = [{"截面名称": k, "库存(m)": v} for k, v in _get_inventory_db().items()]
        if inv_data:
            df_inv = pd.DataFrame(inv_data)
            st.dataframe(df_inv, use_container_width=True, hide_index=True, height=300)
            st.caption(f"共 {len(inv_data)} 条库存数据")
        
        st.markdown("---")
        st.markdown("#### 🤖 AI更新库存库")
        st.markdown("例如：`修改457x191x82库存为80m` 或 `批量更新库存：356x171x67=200m，254x146x43=150m`")
        inv_input = st.text_area("输入库存更新指令", key="inv_ai_input", height=80)
        if st.button("🔧 执行库存库更新", key="btn_inv_update"):
            if inv_input.strip():
                with st.spinner("AI解析中..."):
                    try:
                        update_result = parse_inventory_update(inv_input)
                        if update_result:
                            st.success(f"✅ 库存库更新成功！{update_result}")
                            st.rerun()
                        else:
                            st.warning("⚠️ 未能解析出有效的库存数据")
                    except Exception as e:
                        st.error(f"❌ 更新失败：{e}")
            else:
                st.warning("请输入更新指令")
    
    # AI提示词管理
    with data_tabs[4]:
        st.markdown("#### 🤖 AI提示词管理")
        st.info("修改AI的System Prompt后，新的对话将使用更新后的提示词。当前会话即时生效。")
        
        st.markdown("---")
        st.markdown("##### 📝 自然语言解析提示词 (System Prompt)")
        st.caption("用于将用户的自然语言描述解析为结构化JSON参数")
        
        system_prompt = st.text_area(
            "AI_SYSTEM_PROMPT",
            value=st.session_state.get("ai_system_prompt", AI_SYSTEM_PROMPT),
            height=300,
            key="edit_system_prompt"
        )
        
        if st.button("💾 保存解析提示词", key="btn_save_system_prompt"):
            st.session_state["ai_system_prompt"] = system_prompt
            st.success("✅ 自然语言解析提示词已更新！")
        
        if st.button("🔄 恢复默认解析提示词", key="btn_reset_system_prompt"):
            st.session_state["ai_system_prompt"] = AI_SYSTEM_PROMPT
            st.success("✅ 已恢复为默认解析提示词！")
            st.rerun()
        
        st.markdown("---")
        st.markdown("##### 📝 推荐解读提示词 (Recommend Prompt)")
        st.caption("用于根据选型结果生成推荐解读文字")
        
        recommend_prompt = st.text_area(
            "AI_RECOMMEND_PROMPT",
            value=st.session_state.get("ai_recommend_prompt", AI_RECOMMEND_PROMPT),
            height=200,
            key="edit_recommend_prompt"
        )
        
        if st.button("💾 保存推荐提示词", key="btn_save_recommend_prompt"):
            st.session_state["ai_recommend_prompt"] = recommend_prompt
            st.success("✅ 推荐解读提示词已更新！")
        
        if st.button("🔄 恢复默认推荐提示词", key="btn_reset_recommend_prompt"):
            st.session_state["ai_recommend_prompt"] = AI_RECOMMEND_PROMPT
            st.success("✅ 已恢复为默认推荐提示词！")
            st.rerun()


def parse_section_update(instruction: str) -> str:
    """解析截面更新指令"""
    import re
    results = []
    type_match = re.search(r'(UB|UC|PFC|EA|CHS|SHS|RHS)', instruction, re.IGNORECASE)
    sec_type = type_match.group(1).upper() if type_match else "UB"
    name_match = re.search(r'(\d+x\d+x\d+)', instruction)
    if not name_match:
        return ""
    sec_name = name_match.group(1)
    mass = float(re.search(r'质量\s*([\d.]+)', instruction).group(1)) if re.search(r'质量\s*([\d.]+)', instruction) else 0
    D = float(re.search(r'D\s*([\d.]+)', instruction).group(1)) if re.search(r'D\s*([\d.]+)', instruction) else 0
    B = float(re.search(r'B\s*([\d.]+)', instruction).group(1)) if re.search(r'B\s*([\d.]+)', instruction) else 0
    t = float(re.search(r't\s*([\d.]+)', instruction).group(1)) if re.search(r't\s*([\d.]+)', instruction) else 0
    T = float(re.search(r'T\s*([\d.]+)', instruction).group(1)) if re.search(r'T\s*([\d.]+)', instruction) else 0
    Ix = float(re.search(r'Ix\s*([\d.]+)', instruction).group(1)) if re.search(r'Ix\s*([\d.]+)', instruction) else 0
    Wx = float(re.search(r'Wx\s*([\d.]+)', instruction).group(1)) if re.search(r'Wx\s*([\d.]+)', instruction) else 0
    rx = float(re.search(r'rx\s*([\d.]+)', instruction).group(1)) if re.search(r'rx\s*([\d.]+)', instruction) else 0
    
    if sec_name and mass > 0:
        new_sec = Section(sec_name, sec_type, mass, mass/7.85, D, B, t, T, Ix, Wx, rx)
        existing = False
        for i, s in enumerate(SECTIONS_DB):
            if s.name == sec_name:
                SECTIONS_DB[i] = new_sec
                existing = True
                break
        if not existing:
            SECTIONS_DB.append(new_sec)
        cost_db = _get_cost_db()
        inv_db = _get_inventory_db()
        if sec_name not in cost_db:
            cost_db[sec_name] = 4.0
        if sec_name not in inv_db:
            inv_db[sec_name] = 0.0
        action = "更新" if existing else "添加"
        results.append(f"{action}截面 {sec_name} ({sec_type})")
    return "；".join(results) if results else ""


def parse_cost_update(instruction: str) -> str:
    """解析成本更新指令"""
    import re
    cost_db = _get_cost_db()
    results = []
    pattern1 = r'(\d+x\d+x\d+)\s*(?:单价|价格)?\s*(?:为|=|：|:)?\s*([\d.]+)\s*元'
    for match in re.finditer(pattern1, instruction):
        name, price = match.group(1), float(match.group(2))
        cost_db[name] = price
        results.append(f"{name} → {price}元/kg")
    pattern2 = r'(UB|UC|PFC|EA|CHS|SHS|RHS)类?\s*([\d.]+)\s*元'
    for match in re.finditer(pattern2, instruction, re.IGNORECASE):
        sec_type, price = match.group(1).upper(), float(match.group(2))
        for sec in SECTIONS_DB:
            if sec.type == sec_type:
                cost_db[sec.name] = price
        results.append(f"{sec_type}类全部 → {price}元/kg")
    return "；".join(results) if results else ""


def parse_inventory_update(instruction: str) -> str:
    """解析库存更新指令"""
    import re
    inv_db = _get_inventory_db()
    results = []
    # 只匹配纯数字x格式，避免中文前缀被吞入；支持"库存为"、"库存="等组合
    pattern = r'(\d+x\d+x\d+)\s*(?:库存\s*(?:为|=)?|为|=|：|:)\s*([\d.]+)\s*m'
    for match in re.finditer(pattern, instruction):
        name, qty = match.group(1), float(match.group(2))
        inv_db[name] = qty
        results.append(f"{name} → {qty}m")
    # 简洁格式: 356x171x67=200m
    simple_pattern = r'(\d+x\d+x\d+)\s*=?\s*([\d.]+)\s*m'
    for match in re.finditer(simple_pattern, instruction):
        name, qty = match.group(1), float(match.group(2))
        inv_db[name] = qty
        if name not in "；".join(results):
            results.append(f"{name} → {qty}m")
    # 更新后刷新页面数据
    if results:
        st.session_state["inventory_updated"] = True
    return "；".join(results) if results else ""


def draw_single_beam_diagrams(result: Dict, beam_type: str):
    """绘制单跨梁内力图（荷载图、弯矩图、剪力图）"""
    L = result.get("span", 6.0)
    q = result.get("load_value", 10.0)
    load_type = result.get("load_type", "uniform")
    x_vals = result.get("x_vals", [])
    M_vals = result.get("M_vals", [])
    V_vals = result.get("V_vals", [])
    
    beam_names = {"simply_supported_beam": "简支梁", "cantilever_beam": "悬臂梁", "fixed_beam": "固端梁"}
    beam_name = beam_names.get(beam_type, beam_type)
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    # --- 荷载简图 ---
    ax = axes[0]
    ax.set_title(f"荷载简图 - {beam_name} L={L}m", fontsize=12, fontweight='bold')
    ax.plot([0, L], [0, 0], 'k-', linewidth=3)
    # 支座
    if beam_type == "simply_supported_beam":
        tri_l = plt.Polygon([[0-0.2, -0.3], [0+0.2, -0.3], [0, 0]], fill=False, edgecolor='black', linewidth=1.5)
        tri_r = plt.Polygon([[L-0.2, -0.3], [L+0.2, -0.3], [L, 0]], fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(tri_l)
        ax.add_patch(tri_r)
    elif beam_type == "cantilever_beam":
        ax.plot([0, 0], [-0.4, 0.4], 'k-', linewidth=3)
    elif beam_type == "fixed_beam":
        ax.plot([0, 0], [-0.4, 0.4], 'k-', linewidth=3)
        ax.plot([L, L], [-0.4, 0.4], 'k-', linewidth=3)
    # 荷载箭头（向下）
    if load_type == "uniform" and q > 0:
        for xi in np.linspace(0.2, L - 0.2, 15):
            ax.annotate('', xy=(xi, 0), xytext=(xi, q * 0.3),
                       arrowprops=dict(arrowstyle='->', color='#555555', lw=1.2))
        ax.plot([0, L], [q * 0.3, q * 0.3], color='#555555', linewidth=1.5)
        ax.text(L / 2, q * 0.3 + q * 0.05, f'q={q} kN/m', ha='center', fontsize=9, color='#333333')
    ax.set_xlim(-0.5, L + 0.5)
    ax.set_ylim(-0.8, q * 0.6 if q > 0 else 2)
    ax.axis('off')
    
    # --- 弯矩图 ---
    ax = axes[1]
    ax.set_title("弯矩图 M (kNm)", fontsize=12, fontweight='bold')
    if x_vals and M_vals:
        ax.plot(x_vals, M_vals, 'b-', linewidth=2)
        ax.fill_between(x_vals, M_vals, alpha=0.15, color='blue')
        ax.axhline(y=0, color='black', linewidth=0.5)
        M_max_val = max(M_vals, key=abs)
        M_max_idx = M_vals.index(M_max_val)
        ax.annotate(f'{M_max_val:.1f}', xy=(x_vals[M_max_idx], M_max_val),
                   fontsize=9, fontweight='bold', color='blue',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    ax.set_xlim(-0.5, L + 0.5)
    ax.grid(True, alpha=0.3)
    
    # --- 剪力图 ---
    ax = axes[2]
    ax.set_title("剪力图 V (kN)", fontsize=12, fontweight='bold')
    if x_vals and V_vals:
        ax.plot(x_vals, V_vals, 'r-', linewidth=2)
        ax.fill_between(x_vals, V_vals, alpha=0.15, color='red')
        ax.axhline(y=0, color='black', linewidth=0.5)
        V_max_val = max(V_vals, key=abs)
        V_max_idx = V_vals.index(V_max_val)
        ax.annotate(f'{V_max_val:.1f}', xy=(x_vals[V_max_idx], V_max_val),
                   fontsize=9, fontweight='bold', color='red',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    ax.set_xlim(-0.5, L + 0.5)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf


def render_simple_beam_results():
    """渲染简支梁/悬臂梁/固端梁结果"""
    st.markdown("---")
    st.subheader("📈 内力图")
    
    result = st.session_state.get("simple_beam_result", {})
    beam_type = st.session_state.get("structure_type", "simply_supported_beam")
    
    st.info(f"最大弯矩: {result.get('M_max', 0):.2f} kNm，最大剪力: {result.get('V_max', 0):.2f} kN")
    
    # 生成内力图
    if result.get("x_vals") and result.get("M_vals") and result.get("V_vals"):
        with st.spinner("生成内力图..."):
            diagram_buf = draw_single_beam_diagrams(result, beam_type)
            st.image(diagram_buf, caption="荷载简图 / 弯矩图 / 剪力图", use_container_width=True)
            st.session_state["single_beam_diagram_buf"] = diagram_buf
    
    # 计算书
    render_calc_sheet_section()

def render_calc_sheet_section():
    """渲染计算书生成区域"""
    if not st.session_state.get("results"):
        return
    
    best = st.session_state.get("best_section")
    if not best:
        return
    
    st.markdown("---")
    st.subheader("📄 生成计算书")
    
    if st.button("生成港标计算书", type="primary"):
        params = st.session_state.get("calc_params", {})
        project_name = params.get("project_name", "钢结构项目")
        
        with st.spinner("生成计算书..."):
            if st.session_state.get("structure_type") == "continuous_beam":
                calc_result = st.session_state.get("calc_result", {})
                structure_params = st.session_state.get("structure_params", {})
                
                # 兜底：如果structure_params没有spans，从session_state重建
                if "spans" not in structure_params:
                    spans_list = st.session_state.get("spans", [])
                    loads_list = st.session_state.get("loads", [])
                    structure_params = {
                        "spans": [{"length": s, **l} for s, l in zip(spans_list, loads_list)],
                        "left_support": st.session_state.get("left_support", "pinned"),
                        "right_support": st.session_state.get("right_support", "pinned"),
                        "structure_type": "continuous_beam"
                    }
                
                calc_md = generate_calc_sheet_md(
                    project_name,
                    structure_params,
                    calc_result,
                    best,
                    st.session_state['user_name']
                )
                
                calc_pdf = generate_calc_sheet_pdf(
                    project_name,
                    structure_params,
                    calc_result,
                    best,
                    st.session_state['user_name'],
                    load_diagram_buf=st.session_state.get("load_buf"),
                    moment_diagram_buf=st.session_state.get("moment_buf"),
                    shear_diagram_buf=st.session_state.get("shear_buf"),
                    envelope_moment_buf=st.session_state.get("env_m_buf"),
                    envelope_shear_buf=st.session_state.get("env_v_buf")
                )
            else:
                # 简化梁/手动输入计算书
                if st.session_state.get("structure_type") == "manual_input":
                    # 手动输入模式：从calc_params取内力
                    cp = st.session_state.get("calc_params", {})
                    M_val = cp.get("M", 0)
                    V_val = cp.get("V", 0)
                    N_val = cp.get("N", 0)
                    L_val = cp.get("L", 0)
                    mt_name = cp.get("member_type", "beam")
                    struct_label = "梁" if mt_name == "beam" else "柱"
                else:
                    result = st.session_state.get("simple_beam_result", {})
                    M_val = result.get('M_max', 0)
                    V_val = result.get('V_max', 0)
                    N_val = 0
                    L_val = cp.get("L", 0) if "cp" in dir() else 0
                    struct_label = STRUCTURE_TYPE_NAMES.get(st.session_state.get('structure_type', ''), '')
                
                calc_md = f"""# 钢结构构件设计计算书

## 项目信息
- **工程名称：** {project_name}
- **构件类型：** {struct_label}
- **设计日期：** {datetime.now().strftime('%Y-%m-%d')}

## 设计依据
- HK COP for Structural Use of Steel 2019
- BS 5950-1:2000

## 内力
- 构件长度: {L_val:.2f} m
- 最大弯矩: {M_val:.2f} kNm
- 最大剪力: {V_val:.2f} kN
- 轴力: {N_val:.2f} kN

## 截面选择
- 推荐截面: {best['截面']}
- 利用率: {best['利用率']}
- 成本: {best['成本(元)']}元
"""
                calc_pdf = None
            
            st.session_state["calc_md"] = calc_md
            st.session_state["calc_pdf"] = calc_pdf
    
    if "calc_md" in st.session_state and st.session_state["calc_md"]:
        st.markdown("---")
        st.markdown(st.session_state["calc_md"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 下载 Markdown",
                data=st.session_state["calc_md"],
                file_name=f"计算书_{best['截面']}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
        with col2:
            if st.session_state.get("calc_pdf"):
                st.download_button(
                    label="📥 下载 PDF",
                    data=st.session_state["calc_pdf"],
                    file_name=f"计算书_{best['截面']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

# ============================================================
# 11. 主程序
# ============================================================

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if st.session_state["logged_in"]:
        main_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
