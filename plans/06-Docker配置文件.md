# CS2 地图 Ban Pick 工具 - Docker 配置文件

## 1. Docker Compose 配置

### 1.1 生产环境配置 (docker-compose.yml)

```yaml
version: '3.8'

services:
  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    container_name: cs2_bp_postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-cs2_bp_tool}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - cs2_bp_network
    restart: unless-stopped

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: cs2_bp_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - cs2_bp_network
    restart: unless-stopped

  # FastAPI 后端
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: cs2_bp_backend
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres}@postgres:5432/${POSTGRES_DB:-cs2_bp_tool}
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY:-your-secret-key-change-this-in-production}
      CORS_ORIGINS: ${CORS_ORIGINS:-http://localhost:3000,http://localhost:5173}
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - cs2_bp_network
    restart: unless-stopped

  # Vue.js 前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: cs2_bp_frontend
    environment:
      VITE_API_BASE_URL: ${VITE_API_BASE_URL:-http://localhost:8000/api}
      VITE_WS_BASE_URL: ${VITE_WS_BASE_URL:-http://localhost:8000}
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
    depends_on:
      - backend
    networks:
      - cs2_bp_network
    restart: unless-stopped

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: cs2_bp_nginx
    ports:
      - "${NGINX_PORT:-80}:80"
      - "${NGINX_SSL_PORT:-443}:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    networks:
      - cs2_bp_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  cs2_bp_network:
    driver: bridge
```

### 1.2 开发环境配置 (docker-compose.dev.yml)

```yaml
version: '3.8'

services:
  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    container_name: cs2_bp_postgres_dev
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-cs2_bp_tool}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/scripts:/docker-entrypoint-initdb.d:ro
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - cs2_bp_network

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: cs2_bp_redis_dev
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - cs2_bp_network

  # FastAPI 后端（开发模式）
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: cs2_bp_backend_dev
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres}@postgres:5432/${POSTGRES_DB:-cs2_bp_tool}
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY:-dev-secret-key}
      CORS_ORIGINS: ${CORS_ORIGINS:-http://localhost:3000,http://localhost:5173}
      DEBUG: "true"
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - /app/__pycache__
      - /app/.pytest_cache
    networks:
      - cs2_bp_network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Vue.js 前端（开发模式）
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: cs2_bp_frontend_dev
    environment:
      VITE_API_BASE_URL: ${VITE_API_BASE_URL:-http://localhost:8000/api}
      VITE_WS_BASE_URL: ${VITE_WS_BASE_URL:-http://localhost:8000}
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/dist
    networks:
      - cs2_bp_network
    command: npm run dev -- --host 0.0.0.0

volumes:
  postgres_data:

networks:
  cs2_bp_network:
    driver: bridge
```

## 2. 后端 Dockerfile

### 2.1 生产环境 (backend/Dockerfile)

```dockerfile
# 构建阶段
FROM python:3.11-slim as builder

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.11-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制依赖
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 开发环境 (backend/Dockerfile.dev)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt requirements-dev.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## 3. 前端 Dockerfile

### 3.1 生产环境 (frontend/Dockerfile)

```dockerfile
# 构建阶段
FROM node:18-alpine as builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 运行阶段
FROM node:18-alpine

WORKDIR /app

# 复制构建产物
COPY --from=builder /app/dist ./dist
COPY package*.json ./

# 安装生产依赖
RUN npm ci --only=production

# 暴露端口
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# 启动应用
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
```

### 3.2 开发环境 (frontend/Dockerfile.dev)

```dockerfile
FROM node:18-alpine

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 暴露端口
EXPOSE 3000

# 启动开发服务器
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

## 4. Nginx 配置

### 4.1 Nginx 主配置 (nginx/nginx.conf)

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    # HTTP 服务器
    server {
        listen 80;
        server_name localhost;

        # 前端静态文件
        location / {
            proxy_pass http://frontend:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # 后端 API
        location /api/ {
            proxy_pass http://backend:8000/api/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket
        location /socket.io/ {
            proxy_pass http://backend:8000/socket.io/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 健康检查
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }

    # HTTPS 服务器（生产环境）
    # server {
    #     listen 443 ssl http2;
    #     server_name your-domain.com;
    #
    #     ssl_certificate /etc/nginx/ssl/cert.pem;
    #     ssl_certificate_key /etc/nginx/ssl/key.pem;
    #
    #     ssl_protocols TLSv1.2 TLSv1.3;
    #     ssl_ciphers HIGH:!aNULL:!MD5;
    #     ssl_prefer_server_ciphers on;
    #
    #     # 前端静态文件
    #     location / {
    #         proxy_pass http://frontend:3000;
    #         proxy_http_version 1.1;
    #         proxy_set_header Upgrade $http_upgrade;
    #         proxy_set_header Connection 'upgrade';
    #         proxy_set_header Host $host;
    #         proxy_cache_bypass $http_upgrade;
    #     }
    #
    #     # 后端 API
    #     location /api/ {
    #         proxy_pass http://backend:8000/api/;
    #         proxy_http_version 1.1;
    #         proxy_set_header Host $host;
    #         proxy_set_header X-Real-IP $remote_addr;
    #         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #         proxy_set_header X-Forwarded-Proto $scheme;
    #     }
    #
    #     # WebSocket
    #     location /socket.io/ {
    #         proxy_pass http://backend:8000/socket.io/;
    #         proxy_http_version 1.1;
    #         proxy_set_header Upgrade $http_upgrade;
    #         proxy_set_header Connection "upgrade";
    #         proxy_set_header Host $host;
    #         proxy_set_header X-Real-IP $remote_addr;
    #         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #         proxy_set_header X-Forwarded-Proto $scheme;
    #     }
    # }
}
```

## 5. 环境变量文件 (.env)

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=cs2_bp_tool

# 后端
BACKEND_PORT=8000
SECRET_KEY=your-secret-key-change-this-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 前端
FRONTEND_PORT=3000
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=http://localhost:8000

# Nginx
NGINX_PORT=80
NGINX_SSL_PORT=443
```

## 6. Docker 命令

### 6.1 启动服务

```bash
# 开发环境
docker-compose -f docker-compose.dev.yml up

# 生产环境
docker-compose up -d
```

### 6.2 停止服务

```bash
# 开发环境
docker-compose -f docker-compose.dev.yml down

# 生产环境
docker-compose down
```

### 6.3 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 6.4 重新构建

```bash
# 重新构建所有服务
docker-compose build

# 重新构建特定服务
docker-compose build backend
```

### 6.5 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 进入数据库容器
docker-compose exec postgres psql -U postgres -d cs2_bp_tool
```

### 6.6 数据库备份

```bash
# 备份数据库
docker-compose exec postgres pg_dump -U postgres cs2_bp_tool > backup.sql

# 恢复数据库
docker-compose exec -T postgres psql -U postgres cs2_bp_tool < backup.sql
```

## 7. 部署流程

### 7.1 本地开发

```bash
# 1. 克隆代码
git clone <repository-url>
cd CS2-Map-Ban-Pick-Tool

# 2. 复制环境变量文件
cp .env.example .env

# 3. 启动开发环境
docker-compose -f docker-compose.dev.yml up

# 4. 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 7.2 生产部署

```bash
# 1. 构建生产镜像
docker-compose build

# 2. 配置环境变量
vim .env

# 3. 启动服务
docker-compose up -d

# 4. 配置 SSL 证书（可选）
# 将证书文件放到 nginx/ssl/ 目录
# 取消 nginx.conf 中 HTTPS 配置的注释
# 重启 nginx 服务
docker-compose restart nginx
```
