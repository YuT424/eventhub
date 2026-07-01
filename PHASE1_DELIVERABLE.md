# 阶段一交付说明 — 基础搭建

## 完成情况

| # | 任务 | 状态 |
|---|------|------|
| 1.1 | 解压 starter code，建立项目结构 | ✅ 完成 |
| 1.2 | 初始化 Git 仓库 + .gitignore | ✅ 完成 |
| 1.3 | 创建数据库模型（4张表） | ✅ 完成 |
| 1.4 | 配置 Flask 应用（入口、工厂函数、扩展） | ✅ 完成 |
| 1.5 | 创建路由骨架（4个 Blueprint） | ✅ 完成 |
| 1.6 | 配置导航菜单 + base.html 模板 | ✅ 完成 |
| 1.7 | 验证应用可启动并创建数据库 | ✅ 全部路由测试通过 |

---

## 项目结构

```
a3_group1/
├── main.py                      ← 应用入口
├── requirements.txt             ← Python 依赖
├── .gitignore                   ← 排除 venv/__pycache__/*.db
├── README.md                    ← 项目说明
└── eventhub/                    ← 应用模块（从 website 重命名）
    ├── __init__.py              ← Flask 工厂函数 + 扩展初始化
    ├── models.py                ← 4 张数据表定义
    ├── forms.py                 ← 5 个 WTForms 表单
    ├── views.py                 ← main 蓝图（首页）
    ├── auth.py                  ← auth 蓝图（注册/登录/登出）
    ├── event.py                 ← event 蓝图（活动 CRUD/评论）
    ├── booking.py               ← booking 蓝图（预订/历史）
    ├── static/css/style.css     ← 自定义样式
    └── templates/
        ├── base.html            ← 基础模板（含导航栏）
        ├── index.html           ← 首页
        ├── user.html            ← 登录/注册表单
        ├── 404.html             ← 404 错误页
        ├── 500.html             ← 500 错误页
        ├── event/
        │   ├── list.html        ← 活动列表
        │   ├── detail.html      ← 活动详情
        │   ├── create.html      ← 创建活动
        │   └── update.html      ← 更新活动
        └── booking/
            ├── book.html        ← 预订页面
            └── history.html     ← 预订历史
```

---

## 数据库设计

### users 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| first_name | VARCHAR(64) | 名 |
| last_name | VARCHAR(64) | 姓 |
| email | VARCHAR(120) UNIQUE | 邮箱（登录用） |
| password_hash | VARCHAR(255) | 密码哈希 |
| phone | VARCHAR(20) | 电话 |
| street_address | VARCHAR(255) | 街道地址 |

### events 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| name | VARCHAR(200) | 活动名称 |
| description | TEXT | 活动描述 |
| category | VARCHAR(64) | 分类 |
| date | DATETIME | 活动日期 |
| venue | VARCHAR(255) | 地点 |
| price | FLOAT | 票价 |
| total_tickets | INTEGER | 总票数 |
| available_tickets | INTEGER | 剩余票数 |
| status | VARCHAR(20) | 状态：Open/Inactive/Sold Out/Cancelled |
| image | VARCHAR(500) | 图片 URL |
| user_id | INTEGER FK → users.id | 创建者 |

### bookings 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| order_id | VARCHAR(36) UNIQUE | 订单号 |
| quantity | INTEGER | 购票数量 |
| total_price | FLOAT | 总价 |
| booking_date | DATETIME | 预订时间 |
| user_id | INTEGER FK → users.id | 用户 |
| event_id | INTEGER FK → events.id | 活动 |

### comments 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| content | TEXT | 评论内容 |
| created_at | DATETIME | 创建时间 |
| user_id | INTEGER FK → users.id | 评论者 |
| event_id | INTEGER FK → events.id | 关联活动 |

---

## 路由总览（14条）

| 方法 | 路径 | 蓝图 | 功能 | 需登录 |
|------|------|------|------|--------|
| GET | `/` | main | 首页 | ❌ |
| GET/POST | `/register` | auth | 注册 | ❌ |
| GET/POST | `/login` | auth | 登录 | ❌ |
| GET | `/logout` | auth | 登出 | ✅ |
| GET | `/events` | event | 活动列表 | ❌ |
| GET | `/events/<id>` | event | 活动详情 | ❌ |
| GET/POST | `/events/create` | event | 创建活动 | ✅ |
| GET/POST | `/events/<id>/update` | event | 更新活动 | ✅ |
| POST | `/events/<id>/cancel` | event | 取消活动 | ✅ |
| POST | `/events/<id>/comment` | event | 发表评论 | ✅ |
| GET/POST | `/events/<id>/book` | booking | 预订门票 | ✅ |
| GET | `/my-bookings` | booking | 预订历史 | ✅ |

---

## 运行方式

```bash
cd a3_group1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

访问 http://127.0.0.1:5000

---

## 后续阶段对接说明

阶段一的代码已为后续阶段留好接口：

- **阶段二（用户管理）**：`auth.py` 中的 `register()` 和 `login()` 函数已有框架，填入业务逻辑即可；`RegisterForm` 已包含所有要求字段
- **阶段三（活动管理）**：`event.py` 中 CRUD 路由已定义；`EventForm` 已包含所有字段；`EventStatus` 类定义了 4 种状态常量
- **阶段四（首页浏览）**：`views.py` 的 `index()` 和 `event.py` 的 `list_events()` 已就绪，填入数据库查询即可
- **阶段五（详情评论）**：`event_detail()` 和 `add_comment()` 路由已定义；`CommentForm` 已创建
- **阶段六（预订系统）**：`book_event()` 和 `booking_history()` 路由已定义；`BookingForm` 已创建；`Booking` 模型含 `order_id` 字段
- **阶段七（错误处理）**：404/500 错误页面和 handler 已在 `__init__.py` 中注册

每个路由函数内的 TODO 注释标注了需要实现的具体逻辑。
