# AgroGuard

草地作物病虫害智能监测系统 - 基于深度学习的作物病虫害识别与管理平台。

## 项目简介

AgroGuard 是一个全栈智能监测系统，通过深度学习模型实现作物病虫害的自动识别，并提供数据管理、统计分析、智能预警等功能。系统采用前后端分离架构，支持 Docker 一键部署。

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
├── meadow-be/             # 后端服务 (Flask)
│   ├── App/               # 应用核心模块
│   ├── migrations/        # 数据库迁移
│   ├── app.py             # 入口文件
│   └── requirements.txt   # Python 依赖
└── meadow-fe/             # 前端应用 (Vue 3)
    ├── src/                # 源代码
    ├── public/             # 静态资源
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

- 病虫害图像智能识别
- 作物基础信息管理
- 免疫接种记录与预警
- 繁殖与饲养数据追踪
- 数据可视化统计分析
- AI 智能对话助手

## 开源协议

本项目仅供学习交流使用。