# AgroGuard

草地作物病虫害智能监测系统 - 基于深度学习的草地病虫害识别与草地信息化管理平台。

## 项目简介

AgroGuard 是一个面向草地作物种植与监测管理的全栈智能系统，通过深度学习模型实现草地病虫害的自动识别，并提供草地信息管理、植物护理防护、批次栽培追踪、监测统计分析等完整的信息化管理功能，内置 AI 智能对话助手辅助决策。系统采用前后端分离架构，支持 Docker 一键部署。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Element Plus |
| 后端 | Python + Flask + SQLAlchemy + JWT |
| 数据库 | MySQL 5.7 |
| 部署 | Docker Compose + Nginx |

## 项目结构

```
AgroGuard/
├── docker-compose.yml     # Docker 编排配置
├── init-scripts/          # 数据库初始化脚本
│   └── meadow_test.sql    # 数据库建表与初始数据
├── meadow-be/             # 后端服务 (Flask)
│   ├── App/               # 应用核心模块
│   │   ├── basic/         # 草地基础信息
│   │   ├── colony/        # 监测区域管理
│   │   ├── d_plantcare/   # 植物护理
│   │   ├── e_cultivation/ # 批次栽培管理
│   │   ├── g_harvest/     # 收割销售管理
│   │   ├── h_store/       # 库存管理
│   │   ├── supply/        # 供应管理
│   │   ├── analysis/      # 病虫害监测分析
│   │   ├── statistic/     # 统计报表
│   │   ├── chatbox/       # AI 智能对话
│   │   └── w_information/ # 预警信息
│   ├── migrations/        # 数据库迁移
│   ├── app.py             # 入口文件
│   └── requirements.txt   # Python 依赖
└── meadow-fe/             # 前端应用 (Vue 3)
    ├── src/               # 源代码
    ├── public/            # 静态资源
    └── package.json       # 前端依赖
```

## 快速启动

```bash
# 克隆项目
git clone https://github.com/Ayaxita/AgroGuard.git
cd AgroGuard

# 一键启动（需安装 Docker）
docker-compose up -d
```

启动后访问：
- 前端界面：`http://localhost:5020`
- 后端 API：`http://localhost:5000`
- MySQL：`localhost:5010`

## 主要功能

- **病虫害图像智能识别** — 上传草地作物图片，AI 自动识别病虫害类型并给出防治建议
- **草地基础信息管理** — 草地档案、产地、健康状态、生长监测、养分信息等全生命周期管理
- **植物护理与防护预警** — 草地防护、检疫检验、护理记录、病虫害预警提醒
- **批次栽培数据追踪** — 生长状态、采样信息、批次管理、生长周期监测、人工养护等全流程记录
- **数据可视化统计分析** — 草地资产、收支、防护投入、健康评分等多维度图表分析
- **AI 智能对话助手** — 基于大语言模型的智能问答，辅助草地管理决策

## 开源协议

本项目仅供学习交流使用。
