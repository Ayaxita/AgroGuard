# AgroGuard

草地作物病虫害智能监测系统 - 基于深度学习的草地作物病虫害识别与牧场信息化管理平台。

## 项目简介

AgroGuard 是一个面向草地作物种植与牧场管理的全栈智能监测系统，通过深度学习模型实现作物病虫害的自动识别，并提供作物基础信息管理、免疫接种预警、繁殖饲养追踪、数据可视化统计分析等完整的信息化管理功能，内置 AI 智能对话助手辅助决策。系统采用前后端分离架构，支持 Docker 一键部署。

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
│   │   ├── basic/         # 作物基础信息管理
│   │   ├── d_plantcare/   # 病虫害防治与植物养护
│   │   ├── e_cultivation/ # 繁殖与饲养管理
│   │   ├── g_harvest/     # 收获与销售管理
│   │   ├── h_store/       # 仓储管理
│   │   ├── analysis/      # 数据分析
│   │   ├── statistic/     # 统计报表
│   │   └── chatbox/       # AI 智能对话
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

- **病虫害图像智能识别** — 上传作物图片，AI 自动识别病虫害类型并给出防治建议
- **作物基础信息管理** — 作物个体档案、品种、定位、生长状态等全生命周期管理
- **免疫接种记录与预警** — 接种记录追踪、到期自动预警提醒
- **繁殖与饲养数据追踪** — 发情、配种、妊娠、产仔、断奶等全流程记录
- **数据可视化统计分析** — 资产、收支、饲养成本等多维度图表分析
- **AI 智能对话助手** — 基于大语言模型的智能问答，辅助牧场决策

## 开源协议

本项目仅供学习交流使用。
