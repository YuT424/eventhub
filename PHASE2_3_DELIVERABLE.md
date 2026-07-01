# 阶段二 & 三 交付说明

## 完成情况

| 阶段 | 功能 | 对应分值 | 状态 |
|------|------|----------|------|
| 二 | 用户注册 | 15分 | ✅ |
| 二 | 用户登录 | (含上方) | ✅ |
| 二 | 用户登出 | (含上方) | ✅ |
| 二 | 访问控制 (@login_required) | (含上方) | ✅ |
| 三 | 创建活动 | 30分 | ✅ |
| 三 | 更新活动（仅创建者） | (含上方) | ✅ |
| 三 | 取消活动（仅创建者） | (含上方) | ✅ |
| 三 | 活动状态自动管理 | (含上方) | ✅ |
| 三 | 活动列表 + 分类过滤 | (含上方) | ✅ |
| 三 | 活动详情页 | (含上方) | ✅ |
| 三 | 评论功能 | (含上方) | ✅ |

---

## 阶段二：用户管理（15分）

### 注册 `/register`
- 表单字段：名、姓、邮箱、密码、确认密码、电话、街道地址
- 邮箱唯一性检查
- 密码使用 flask-bcrypt 哈希存储
- 注册成功后重定向到登录页

### 登录 `/login`
- 按邮箱查找用户
- check_password_hash 验证密码
- Flask-Login login_user() 建立 Session
- 支持 `next` 参数重定向

### 登出 `/logout`
- @login_required 保护
- logout_user() 清除 Session
- 重定向到首页

### 访问控制
- 所有需登录的路由使用 @login_required
- 未登录用户自动重定向到 /login?next=...

---

## 阶段三：活动管理（30分）

### 创建活动 `/events/create`
- 完整表单：名称、描述、分类（下拉）、日期时间、地点、票价、总票数、图片URL
- available_tickets 初始 = total_tickets
- 状态初始 = Open
- 关联创建者 user_id

### 更新活动 `/events/<id>/update`
- 仅创建者可编辑（权限验证）
- 表单预填充已有数据 (obj=event)
- 不能修改状态（仅通过取消或自动管理）
- 票数变更时自动调整 available_tickets

### 取消活动 `/events/<id>/cancel` (POST)
- 仅创建者可取消
- 状态设为 Cancelled（不可逆）
- 不影响已有评论数据

### 状态自动管理 `refresh_event_status()`
| 条件 | 状态 |
|------|------|
| available_tickets = 0 | Sold Out |
| date < now() | Inactive |
| 其他（有票+未过期） | Open |
| 手动取消 | Cancelled（不会被自动覆盖） |

### 活动列表 `/events`
- 分类过滤 pills（All / Conference / Workshop / Social / Music / Sports / Other）
- 每张卡片显示：图片、名称、日期、地点、分类、状态徽章、价格、余票
- 响应式网格（col-md-6 col-lg-4）

### 活动详情 `/events/<id>`
- 左侧图片 + 右侧信息表格
- 状态徽章（颜色区分）
- 操作按钮区域：
  - 已登录 + Open → "Book Now" 绿色按钮
  - 未登录 + Open → "Login to Book" 按钮
  - Sold Out → 禁用按钮
  - 创建者 → "Edit" + "Cancel Event" 按钮
- 关于活动描述卡片
- 评论区：评论表单（已登录）+ 评论列表（所有访客可见）

### 评论 `/events/<id>/comment` (POST)
- @login_required
- 写入 Comment 表，关联 user_id + event_id
- 重定向回详情页

---

## HTTP 集成测试结果（12/12 通过）

| # | 测试项 | 预期 | 实际 |
|---|--------|------|------|
| 1 | GET / | 200 | ✅ 200 |
| 2 | POST /register | 302→/login | ✅ 302 |
| 3 | POST /login | 302→/ | ✅ 302 |
| 4 | POST /events/create | 302→/events/2 | ✅ 302 |
| 5 | GET /events | 200 | ✅ 200 |
| 5b | GET /events?category=Workshop | 200 | ✅ 200 |
| 6 | GET /events/1 | 200 | ✅ 200 |
| 6b | GET /events/999 (不存在) | 302→/events | ✅ 302 |
| 7 | POST /events/1/update | 302→/events/1 | ✅ 302 |
| 8 | POST /events/1/comment | 302→/events/1 | ✅ 302 |
| 9 | POST /events/1/cancel | 302→/events/1 | ✅ 302 |
| 10 | GET /logout | 302→/ | ✅ 302 |
| 11 | GET /events/create (未登录) | 302→/login | ✅ 302 |
| 12 | GET /nonexistent | 404 | ✅ 404 |

---

## 修改的文件

| 文件 | 变更内容 |
|------|----------|
| `eventhub/auth.py` | 完整注册、登录、登出逻辑 |
| `eventhub/event.py` | 活动 CRUD、评论、状态管理、权限验证 |
| `eventhub/views.py` | 首页查询即将举行的活动 |
| `eventhub/templates/index.html` | 活动卡片网格 + 分类侧边栏 |
| `eventhub/templates/event/list.html` | 分类过滤 pills + 活动卡片 |
| `eventhub/templates/event/detail.html` | 详情页 + 评论区 + 操作按钮 |
| `eventhub/templates/event/create.html` | Bootstrap 渲染表单 |
| `eventhub/templates/event/update.html` | 预填充表单 + 提示信息 |

---

## 运行方式

```bash
cd outputs/a3_group1
source venv/bin/activate
python main.py
```
访问 http://127.0.0.1:5000

---

## 后续阶段对接

- **阶段四（首页浏览）**：✅ 已在 views.py + index.html 中实现基本版本
- **阶段五（详情评论）**：✅ 已在 event.py + detail.html 中实现
- **阶段六（预订系统）**：`booking.py` 路由已定义，需填充预订逻辑
- **阶段七（错误处理收尾）**：404/500 已实现，需补充响应式测试和打包
