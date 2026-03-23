# SmartHr 智能人力资源管理系统

## 项目简介
SmartHr是一个智能化的人力资源招聘管理平台，连接求职者、企业和平台管理者三方，通过AI技术赋能招聘全流程，提升求职效率和招聘质量。

## 技术栈
### 后端
- Python 3.11+
- FastAPI: 高性能Web框架
- SQLAlchemy 2.0: ORM框架
- SQLite3: 本地数据库（可扩展为MySQL）
- JWT: 身份认证
- 火山引擎大模型: AI能力支持

### 前端
- Vue3 + Vite
- Element Plus: UI组件库
- Pinia: 状态管理
- Vue Router: 路由管理
- Axios: HTTP请求库

## 项目结构
```
SmartHr/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API接口
│   │   ├── core/           # 核心配置（安全、数据库、异常）
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic数据结构
│   │   ├── services/       # 业务逻辑层
│   │   └── main.py         # 应用入口
│   ├── uploads/            # 文件上传目录
│   ├── requirements.txt    # Python依赖
│   └── .env                # 环境变量配置
│
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── api/            # API请求封装
│   │   ├── views/          # 页面组件
│   │   ├── layouts/        # 布局组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # 状态管理
│   │   ├── utils/          # 工具函数
│   │   └── main.js         # 入口文件
│   └── package.json        # 前端依赖
│
├── database/               # 数据库文件
│   └── smarthr.db          # SQLite数据库
│
├── docs/                   # 项目文档
│   ├── SmartHr需求分析文档.md
│   ├── SmartHr产品设计文档.md
│   └── SmartHr开发设计文档.md
└── README.md               # 项目说明
```

## 快速启动

### 后端启动
1. 进入后端目录
```bash
cd backend
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制`.env.example`为`.env`，配置火山引擎API密钥：
```
VOLCENGINE_API_KEY=your-volcengine-api-key
```

4. 启动服务
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务启动后访问：http://localhost:8000/docs 查看API文档

### 前端启动
1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务
```bash
npm run dev
```

前端服务启动后访问：http://localhost:3000

## 核心功能

### 求职者端
- 智能简历中心：简历创建、上传解析、AI评测
- 机会发现：岗位推荐、搜索、企业主页浏览
- AI求职助手：匹配度分析、面试准备、技能图谱
- 申请管理：投递记录、沟通记录、面试日程

### 企业端
- 企业主页管理：公司信息维护、岗位管理
- 人才筛选与匹配：简历收件箱、AI智能排序、人才搜索
- 人才库与CRM：人才库建设、候选人关系管理
- 流程协同：面试流程管理、团队协作、面试日程
- 数据看板：招聘效率分析、渠道效果分析、人才画像

### 管理端
- 用户与权限管理：用户管理、企业认证审核、角色权限
- 平台运营：内容审核、投诉处理、基础数据维护
- AI模型管理：匹配效果监控、模型迭代、偏见检测
- 全局数据看板：核心指标、业务健康度、系统监控

## 开发进度
- ✅ 需求分析文档
- ✅ 产品设计文档
- ✅ 开发设计文档
- ✅ 后端基础框架搭建
- ✅ 核心数据模型开发
- ✅ 公共接口开发（注册、登录、文件上传）
- ✅ 求职者端核心接口开发
- ✅ 企业端核心接口开发
- ✅ 管理端核心接口开发
- ✅ AI服务模块开发（火山引擎对接）
- ✅ 前端基础框架搭建
- 🔄 前端页面开发中
