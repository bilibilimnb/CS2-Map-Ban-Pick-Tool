# CS2 地图 Ban Pick 工具 - 后端 API 接口规范

## 1. API 概述

本项目后端采用 FastAPI 框架，提供 REST API 和 WebSocket 两种通信方式。

- **REST API**：用于房间查询、用户管理、管理员操作等
- **WebSocket**：用于实时通信，包括 BP 流程、聊天、状态同步等

## 2. 通用规范

### 2.1 基础 URL

```
开发环境: http://localhost:8000
生产环境: https://your-domain.com/api
```

### 2.2 响应格式

所有 REST API 响应遵循统一格式：

**成功响应：**
```json
{
  "success": true,
  "data": { /* 响应数据 */ },
  "message": "操作成功"
}
```

**错误响应：**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

### 2.3 HTTP 状态码

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 500 | 服务器内部错误 |

### 2.4 认证方式

管理员 API 使用 JWT Token 认证：

```http
Authorization: Bearer <jwt_token>
```

## 3. REST API

### 3.1 管理员相关 API

#### 3.1.1 管理员登录

```http
POST /api/admin/login
```

**请求体：**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "admin": {
      "id": "uuid",
      "username": "admin"
    }
  }
}
```

#### 3.1.2 创建地图池配置

```http
POST /api/admin/mappools
Authorization: Bearer <jwt_token>
```

**请求体：**
```json
{
  "name": "自定义地图池",
  "map01_name": "Mirage",
  "map01_icon": "https://example.com/mirage.png",
  "map02_name": "Inferno",
  "map02_icon": "https://example.com/inferno.png",
  "map03_name": "Dust2",
  "map03_icon": "https://example.com/dust2.png",
  "map04_name": "Nuke",
  "map04_icon": "https://example.com/nuke.png",
  "map05_name": "Anubis",
  "map05_icon": "https://example.com/anubis.png",
  "map06_name": "Vertigo",
  "map06_icon": "https://example.com/vertigo.png",
  "map07_name": "Ancient",
  "map07_icon": "https://example.com/ancient.png"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "自定义地图池",
    ...
  }
}
```

#### 3.1.3 获取所有地图池配置

```http
GET /api/admin/mappools
Authorization: Bearer <jwt_token>
```

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "默认地图池",
      "map01_name": "Mirage",
      ...
    }
  ]
}
```

#### 3.1.4 创建房间

```http
POST /api/admin/rooms
Authorization: Bearer <jwt_token>
```

**请求体：**
```json
{
  "team_a_name": "Team A",
  "team_a_icon": "https://example.com/team_a.png",
  "team_b_name": "Team B",
  "team_b_icon": "https://example.com/team_b.png",
  "mappool_config_id": "uuid"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "room_code": "ABC12345",
    "team_a_name": "Team A",
    "team_b_name": "Team B",
    "status": "waiting"
  }
}
```

#### 3.1.5 获取房间列表

```http
GET /api/admin/rooms
Authorization: Bearer <jwt_token>
```

**查询参数：**
- `status`: 房间状态过滤（可选）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**响应：**
```json
{
  "success": true,
  "data": {
    "total": 100,
    "items": [
      {
        "id": "uuid",
        "room_code": "ABC12345",
        "team_a_name": "Team A",
        "team_b_name": "Team B",
        "status": "finished",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### 3.1.6 获取房间详情

```http
GET /api/admin/rooms/{room_id}
Authorization: Bearer <jwt_token>
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "room_code": "ABC12345",
    "team_a_name": "Team A",
    "team_b_name": "Team B",
    "status": "finished",
    "users": [
      {
        "id": "uuid",
        "display_name": "Player1",
        "team": "team_a"
      }
    ]
  }
}
```

#### 3.1.7 获取 BP 记录

```http
GET /api/admin/rooms/{room_id}/bp-record
Authorization: Bearer <jwt_token>
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "phase_1_ban": "map01",
    "phase_1_ban_by": "team_a",
    "phase_2_ban": "map02",
    "phase_2_ban_by": "team_b",
    "phase_3_pick": "map03",
    "phase_3_pick_by": "team_a",
    "phase_4_pick": "map04",
    "phase_4_pick_by": "team_b",
    "phase_5_ban": "map05",
    "phase_5_ban_by": "team_a",
    "phase_6_ban": "map06",
    "phase_6_ban_by": "team_b",
    "decider": "map07",
    "operation_logs": [
      {
        "phase": 1,
        "action_type": "ban",
        "map_id": "map01",
        "team": "team_a",
        "user_name": "Player1",
        "timestamp": 1704067200
      }
    ]
  }
}
```

### 3.2 房间相关 API

#### 3.2.1 通过房间码获取房间信息

```http
GET /api/rooms/{room_code}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "room_code": "ABC12345",
    "team_a_name": "Team A",
    "team_a_icon": "https://example.com/team_a.png",
    "team_b_name": "Team B",
    "team_b_icon": "https://example.com/team_b.png",
    "status": "waiting",
    "mappool": {
      "map01_name": "Mirage",
      "map01_icon": "https://example.com/mirage.png",
      ...
    }
  }
}
```

#### 3.2.2 加入房间

```http
POST /api/rooms/{room_id}/join
```

**请求体：**
```json
{
  "session_id": "session_uuid",
  "team": "team_a",
  "display_name": "Player1"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "room_id": "uuid",
    "team": "team_a",
    "display_name": "Player1"
  }
}
```

#### 3.2.3 更新用户准备状态

```http
POST /api/rooms/{room_id}/ready
```

**请求体：**
```json
{
  "session_id": "session_uuid",
  "is_ready": true
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "is_ready": true
  }
}
```

#### 3.2.4 获取房间用户列表

```http
GET /api/rooms/{room_id}/users
```

**响应：**
```json
{
  "success": true,
  "data": {
    "team_a": [
      {
        "id": "uuid",
        "display_name": "Player1",
        "is_ready": true
      }
    ],
    "team_b": [
      {
        "id": "uuid",
        "display_name": "Player2",
        "is_ready": false
      }
    ]
  }
}
```

### 3.3 BP 相关 API

#### 3.3.1 开始 BP

```http
POST /api/rooms/{room_id}/bp/start
```

**响应：**
```json
{
  "success": true,
  "data": {
    "room_id": "uuid",
    "status": "rolling",
    "roll_a": 45,
    "roll_b": 78,
    "first_pick_team": "team_b"
  }
}
```

#### 3.3.2 获取当前 BP 状态

```http
GET /api/rooms/{room_id}/bp/status
```

**响应：**
```json
{
  "success": true,
  "data": {
    "status": "ban1",
    "current_team": "team_b",
    "current_user": "Player1",
    "remaining_time": 12,
    "banned_maps": ["map01"],
    "picked_maps": ["map03"],
    "available_maps": ["map02", "map04", "map05", "map06", "map07"]
  }
}
```

## 4. WebSocket API

### 4.1 连接

```javascript
const socket = io('http://localhost:8000', {
  query: {
    room_id: 'room_uuid',
    session_id: 'session_uuid'
  }
});
```

### 4.2 客户端发送事件

#### 4.2.1 加入房间

```json
{
  "event": "join_room",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid"
  }
}
```

#### 4.2.2 选择队伍

```json
{
  "event": "select_team",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid",
    "team": "team_a"
  }
}
```

#### 4.2.3 更新用户名称

```json
{
  "event": "update_name",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid",
    "display_name": "Player1"
  }
}
```

#### 4.2.4 用户准备

```json
{
  "event": "ready",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid",
    "is_ready": true
  }
}
```

#### 4.2.5 Ban 地图

```json
{
  "event": "ban_map",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid",
    "map_id": "map01"
  }
}
```

#### 4.2.6 Pick 地图

```json
{
  "event": "pick_map",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid",
    "map_id": "map03"
  }
}
```

#### 4.2.7 发送聊天消息

```json
{
  "event": "send_chat",
  "data": {
    "room_id": "room_uuid",
    "session_id": "session_uuid",
    "content": "Hello team!"
  }
}
```

### 4.3 服务端广播事件

#### 4.3.1 用户加入

```json
{
  "event": "user_joined",
  "data": {
    "user_id": "uuid",
    "display_name": "Player1",
    "team": "team_a",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### 4.3.2 用户离开

```json
{
  "event": "user_left",
  "data": {
    "user_id": "uuid",
    "display_name": "Player1",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### 4.3.3 队伍信息更新

```json
{
  "event": "team_updated",
  "data": {
    "team": "team_a",
    "users": [
      {
        "id": "uuid",
        "display_name": "Player1",
        "is_ready": true
      }
    ]
  }
}
```

#### 4.3.4 BP 开始

```json
{
  "event": "bp_started",
  "data": {
    "room_id": "uuid",
    "roll_a": 45,
    "roll_b": 78,
    "first_pick_team": "team_b"
  }
}
```

#### 4.3.5 BP 阶段变更

```json
{
  "event": "bp_phase_changed",
  "data": {
    "phase": "ban1",
    "current_team": "team_b",
    "current_user": "Player1",
    "remaining_time": 15,
    "instruction": "禁用1张地图"
  }
}
```

#### 4.3.6 地图被 Ban

```json
{
  "event": "map_banned",
  "data": {
    "map_id": "map01",
    "banned_by": "team_a",
    "user_name": "Player1",
    "phase": 1,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### 4.3.7 地图被 Pick

```json
{
  "event": "map_picked",
  "data": {
    "map_id": "map03",
    "picked_by": "team_a",
    "user_name": "Player1",
    "phase": 3,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### 4.3.8 计时器更新

```json
{
  "event": "timer_tick",
  "data": {
    "remaining_time": 12,
    "total_time": 15
  }
}
```

#### 4.3.9 聊天消息

```json
{
  "event": "chat_message",
  "data": {
    "team": "team_a",
    "user_name": "Player1",
    "content": "Hello team!",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### 4.3.10 BP 结束

```json
{
  "event": "bp_finished",
  "data": {
    "room_id": "uuid",
    "result": {
      "phase_1_ban": {
        "map_id": "map01",
        "team": "team_a"
      },
      "phase_2_ban": {
        "map_id": "map02",
        "team": "team_b"
      },
      "phase_3_pick": {
        "map_id": "map03",
        "team": "team_a"
      },
      "phase_4_pick": {
        "map_id": "map04",
        "team": "team_b"
      },
      "phase_5_ban": {
        "map_id": "map05",
        "team": "team_a"
      },
      "phase_6_ban": {
        "map_id": "map06",
        "team": "team_b"
      },
      "decider": {
        "map_id": "map07"
      }
    }
  }
}
```

## 5. 错误码定义

| 错误码 | 说明 |
|-------|------|
| AUTH_001 | 用户名或密码错误 |
| AUTH_002 | Token 无效或已过期 |
| ROOM_001 | 房间不存在 |
| ROOM_002 | 房间已满 |
| ROOM_003 | 房间状态不允许此操作 |
| USER_001 | 用户未加入房间 |
| USER_002 | 用户已存在 |
| BP_001 | 不是当前操作人 |
| BP_002 | 地图不可选 |
| BP_003 | BP 已结束 |
| VALIDATION_001 | 请求参数错误 |
| SERVER_001 | 服务器内部错误 |

## 6. 限流策略

| API 类型 | 限制 |
|---------|------|
| 登录 API | 5 次/分钟/IP |
| 创建房间 API | 10 次/分钟/管理员 |
| 加入房间 API | 10 次/分钟/会话 |
| WebSocket 消息 | 30 条/分钟/会话 |

## 7. CORS 配置

```python
origins = [
    "http://localhost:3000",
    "https://your-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
