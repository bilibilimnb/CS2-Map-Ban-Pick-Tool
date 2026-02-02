# CS2 地图 Ban Pick 工具

一个用于 Counter-Strike 2 的地图 Ban Pick 工具，支持 BO3 模式的地图禁用和选择流程。

> **项目地址**: https://github.com/bilibilimnb/CS2-Map-Ban-Pick-Tool

## 技术栈

- **前端**: Vue.js 3 + Vite + TailwindCSS + Socket.io-client
- **后端**: Python FastAPI + SQLAlchemy + Socket.io
- **数据库**: PostgreSQL 15
- **部署**: Docker + Docker Compose + Nginx

## 快速开始

### 一键部署（推荐）

```bash
# 克隆项目
git clone https://github.com/bilibilimnb/CS2-Map-Ban-Pick-Tool.git
cd CS2-Map-Ban-Pick-Tool

# 1. 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件，修改数据库密码等配置

# 2. 一键启动（生产环境）
docker-compose up -d

# 3. 访问应用
# 前端: http://localhost
# 后端API: http://localhost/api
# Swagger文档: http://localhost/api/docs
```

### 开发环境启动

```bash
# 开发环境（支持热重载）
docker-compose -f docker-compose.dev.yml up
```

### 本地开发

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

#### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### 数据库初始化

```bash
cd backend
alembic upgrade head
python scripts/init_db.py
```

### 本地开发

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

#### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### 数据库初始化

```bash
cd backend
alembic upgrade head
```

## 项目结构

```
CS2-Map-Ban-Pick-Tool/
├── plans/                    # 架构设计文档
│   ├── 01-项目整体架构设计.md
│   ├── 02-数据库模型设计.md
│   ├── 03-后端API接口规范.md
│   ├── 04-前端页面结构和组件架构.md
│   ├── 05-项目目录结构.md
│   ├── 06-Docker配置文件.md
│   └── 07-开发环境配置文件.md
├── frontend/                  # Vue.js 前端
│   ├── src/
│   │   ├── components/     # 公共组件
│   │   │   ├── BPMapPolygon/  # 七边形地图池组件
│   │   │   ├── ChatBox/       # 聊天框组件
│   │   │   ├── MapCard/       # 地图卡片组件
│   │   │   ├── ProgressBar/   # 进度条组件
│   │   │   ├── ResultGrid/    # 结果展示组件
│   │   │   ├── TeamDisplay/   # 队伍展示组件
│   │   │   ├── Timer/         # 计时器组件
│   │   │   └── common/        # 通用组件
│   │   ├── views/         # 页面视图
│   │   │   ├── JoinRoom.vue       # 加入房间页面
│   │   │   ├── SelectTeam.vue     # 选择队伍页面
│   │   │   ├── InputName.vue      # 输入昵称页面
│   │   │   ├── WaitingRoom.vue    # 等待准备页面
│   │   │   ├── BPProcess.vue      # BP 流程页面
│   │   │   ├── BPResult.vue       # BP 结果页面
│   │   │   ├── AdminLogin.vue     # 管理员登录页面
│   │   │   └── AdminDashboard.vue # 管理员后台
│   │   ├── stores/        # Pinia 状态管理
│   │   │   ├── room.ts      # 房间状态
│   │   │   ├── user.ts      # 用户状态
│   │   │   ├── bp.ts        # BP 流程状态
│   │   │   └── chat.ts      # 聊天状态
│   │   ├── services/      # API 和 WebSocket 服务
│   │   │   ├── api.ts       # REST API 客户端
│   │   │   └── socket.ts    # WebSocket 客户端
│   │   ├── types/         # TypeScript 类型定义
│   │   │   └── index.ts     # 类型定义
│   │   ├── utils/         # 工具函数
│   │   │   ├── storage.ts   # 本地存储工具
│   │   │   └── constants.ts # 常量定义
│   │   ├── router/        # 路由配置
│   │   │   └── index.ts     # 路由定义
│   │   ├── App.vue        # 根组件
│   │   └── main.ts        # 应用入口
│   ├── public/              # 静态资源
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── backend/                   # FastAPI 后端
│   ├── app/
│   │   ├── main.py        # FastAPI 应用入口
│   │   ├── api/           # API 路由
│   │   │   ├── admin.py    # 管理员相关 API
│   │   │   ├── rooms.py    # 房间管理 API
│   │   │   ├── users.py    # 用户管理 API
│   │   │   ├── bp.py       # BP 流程 API
│   │   │   └── records.py  # 记录查询 API
│   │   ├── core/          # 核心配置
│   │   │   ├── config.py   # 配置管理
│   │   │   ├── security.py # 安全相关
│   │   │   └── deps.py     # 依赖注入
│   │   ├── models/        # 数据库模型
│   │   │   ├── admin.py    # 管理员模型
│   │   │   ├── room.py     # 房间模型
│   │   │   ├── user.py     # 用户模型
│   │   │   ├── mappool.py  # 地图池模型
│   │   │   └── bp_record.py # BP 记录模型
│   │   ├── schemas/       # Pydantic 模型
│   │   │   ├── admin.py
│   │   │   ├── room.py
│   │   │   ├── bp.py
│   │   │   └── user.py
│   │   ├── services/      # 业务逻辑
│   │   ├── websocket/     # WebSocket 处理
│   │   │   ├── manager.py  # WebSocket 连接管理器
│   │   │   ├── handlers.py # WebSocket 事件处理器
│   │   │   └── events.py   # WebSocket 事件定义
│   │   └── db/           # 数据库会话
│   │       ├── base.py     # 数据库基类
│   │       └── session.py  # 会话管理
│   ├── tests/               # 测试文件
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_websocket/
│   ├── scripts/             # 脚本文件
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── alembic.ini
├── nginx/                     # Nginx 配置
│   └── nginx.conf
├── docker-compose.yml          # Docker 编排配置（生产）
├── docker-compose.dev.yml      # Docker 编排配置（开发）
├── .env                       # 环境变量
├── .gitignore
├── LICENSE
└── README.md
```

## 功能特性

### 核心功能
- ✅ 房间创建和管理
- ✅ 地图池配置（自定义地图池）
- ✅ 用户加入房间和选择队伍
- ✅ 实时聊天（队内可见）
- ✅ BO3 BP 流程
  - Roll 点决定先后手
  - 第一轮 Ban（每队各1张）
  - 第二轮 Ban（每队各1张）
  - Pick（每队各1张）
  - 决胜图自动选择
- ✅ 计时器（每操作15秒）
- ✅ BP 结果展示
- ✅ 管理员后台
  - 房间管理
  - 地图池管理
  - BP 记录查看

### UI 特性
- 🎨 正七边形地图池展示
- 📊 实时进度条
- ⏱️ 操作计时器
- 💬 队内聊天系统
- 📱 BP 结果可视化展示

## API 文档

- **前端**: `http://localhost:3000`
- **后端**: `http://localhost:8000/api`
- **Swagger**: `http://localhost:8000/docs`
- **WebSocket**: `ws://localhost:8000/ws`

## 开发计划

### 第一阶段：基础框架 ✅
- [x] 项目目录结构
- [x] 前端项目文件
- [x] 后端项目文件
- [x] Docker 配置文件
- [x] Nginx 配置文件
- [x] 前端源代码文件
- [x] 后端源代码文件

### 第二阶段：数据库集成 ✅
- [x] 实现数据库模型
- [x] 实现数据库迁移
- [x] 创建初始化脚本

### 第三阶段：API 开发 ✅
- [x] 实现管理员登录 API
- [x] 实现房间管理 API
- [x] 实现用户管理 API
- [x] 实现 BP 流程 API

### 第四阶段：WebSocket 开发 ✅
- [x] 实现 WebSocket 连接管理
- [x] 实现 BP 流程实时通信
- [x] 实现聊天功能

### 第五阶段：前端开发 ✅
- [x] 实现加入房间页面
- [x] 实现选择队伍页面
- [x] 实现等待准备页面
- [x] 实现 BP 流程页面
- [x] 实现 BP 结果页面
- [x] 实现管理员后台

### 第六阶段：测试和部署 ✅
- [x] Docker 部署
- [x] 生产环境配置

## 环境变量

### 前端环境变量 (`.env`)
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

### 后端环境变量 (`.env`)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/cs2_bp
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## 默认账户

### 管理员账户
- **用户名**: `admin`
- **密码**: `admin123`

> ⚠️ 部署后请立即修改默认密码！

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！
