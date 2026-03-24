# SmartHr 智能人力资源管理系统

## 项目简介
SmartHr是一个智能化的人力资源招聘管理平台，连接求职者、企业和平台管理者三方，通过AI技术赋能招聘全流程，提升求职效率和招聘质量。
<video src="./docs/20260323-140229.mp4" controls></video>

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

## 生产环境部署

### 环境要求
- 服务器配置：2核4G及以上
- 操作系统：CentOS 7+/Ubuntu 18.04+/Windows Server 2016+
- 数据库：SQLite 3/MySQL 5.7+
- Node.js 16+
- Python 3.11+

### 后端部署
1. **代码下载**
```bash
git clone https://github.com/zhangyifei1/SmartHr.git
cd SmartHr/backend
```

2. **环境配置**
```bash
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境（Linux/Mac）
source venv/bin/activate
# 激活虚拟环境（Windows）
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库连接、JWT密钥、火山引擎API密钥等
```

3. **数据库初始化**
```bash
# 执行数据库迁移
alembic upgrade head

# 初始化基础数据
python scripts/init_data.py
```

4. **启动服务**
```bash
# 使用Gunicorn启动（推荐生产环境）
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### 前端部署
1. **构建项目**
```bash
cd ../frontend
# 安装依赖
npm install
# 构建生产版本
npm run build
```

2. **Nginx配置**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/SmartHr/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 文件上传代理
    location /uploads {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

### Docker部署（推荐）
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 核心功能

### 求职者端
- **智能简历中心**
  - 支持在线创建和编辑简历，多模板可选
  - PDF/Word格式简历自动解析，智能提取信息
  - AI简历评测：提供简历优化建议、技能匹配分析
  - 简历版本管理，支持多份简历维护
- **机会发现**
  - 智能岗位推荐：基于个人简历和求职意向精准匹配
  - 多维度职位搜索：按行业、薪资、地区、工作经验等筛选
  - 企业主页浏览：查看企业详细信息、在招职位、公司评价
  - 职位收藏功能，随时关注意向岗位
- **AI求职助手**
  - 匹配度分析：投递前查看简历与岗位的匹配分数和差距分析
  - 面试准备：AI生成常见面试问题和参考答案
  - 技能图谱：分析个人技能优势和短板，提供学习建议
  - 求职路线规划：基于目标岗位定制能力提升路径
- **申请管理**
  - 投递记录：查看所有投递职位的状态和进展
  - 沟通记录：与企业HR的消息沟通历史
  - 面试日程：面试安排日历提醒，避免错过面试
  - Offer管理：收到的Offer对比和管理

### 企业端
- **企业主页管理**
  - 企业信息维护：公司介绍、发展历程、福利体系等信息管理
  - 岗位管理：职位发布、编辑、下架、刷新全流程管理
  - 品牌展示：企业风采、工作环境展示，提升雇主品牌形象
- **人才筛选与匹配**
  - 简历收件箱：统一管理所有岗位收到的简历
  - AI智能排序：基于岗位要求自动对简历进行匹配度排序
  - 高级人才搜索：多维度筛选条件，精准查找合适人才
  - 简历批量处理：支持批量标记、下载、导出简历
- **人才库与CRM**
  - 人才库建设：分类管理优秀候选人，建立企业人才资产
  - 候选人关系管理：跟踪候选人状态，定期维护人才关系
  - 人才标签系统：自定义标签对候选人进行分类管理
  - 人才动态跟踪：关注候选人的职业发展动态
- **流程协同**
  - 面试流程管理：自定义面试流程，跟踪面试全流程进展
  - 团队协作：支持多面试官协同评价，面试反馈共享
  - 面试日程：自动发送面试邀请，日程同步和提醒
  - Offer管理：Offer模板定制、发送和状态跟踪
- **数据看板**
  - 招聘效率分析：招聘周期、转化率、渠道效果等数据分析
  - 人才画像：分析招聘人才的特征，优化招聘标准
  - 团队绩效：招聘团队的工作效率和成果统计
  - 成本分析：招聘渠道投入产出比分析

### 管理端
- **用户与权限管理**
  - 用户管理：平台所有用户的账号管理、状态控制
  - 企业认证审核：企业资质审核，保障平台企业真实性
  - 角色权限管理：自定义角色和权限，细粒度访问控制
  - 操作日志：记录所有管理员的操作行为，便于审计
- **平台运营**
  - 内容审核：职位信息、企业信息、简历内容的审核管理
  - 投诉处理：处理用户投诉和纠纷，维护平台秩序
  - 基础数据维护：行业、职位、地区等基础数据管理
  - 公告管理：平台公告的发布和管理
- **AI模型管理**
  - 匹配效果监控：监控AI匹配算法的准确性和效果
  - 模型迭代：支持AI模型的版本管理和灰度发布
  - 偏见检测：检测AI算法中的潜在偏见，保障招聘公平性
  - 效果分析：AI功能的使用率和用户满意度分析
- **全局数据看板**
  - 核心指标：平台用户数、职位数、投递量等核心业务指标
  - 业务健康度：平台整体运营情况分析，增长趋势预测
  - 系统监控：服务器性能、接口响应时间等系统监控数据
  - 财务统计：平台收入、支出等财务数据统计

## 开发进度
当前版本：v1.0.0-beta

- ✅ 需求分析文档
- ✅ 产品设计文档
- ✅ 开发设计文档
- ✅ 后端基础框架搭建
- ✅ 核心数据模型开发
- ✅ 公共接口开发（注册、登录、文件上传）
- ✅ 求职者端核心接口开发（100%完成）
- ✅ 企业端核心接口开发（100%完成）
- ✅ 管理端核心接口开发（100%完成）
- ✅ AI服务模块开发（火山引擎对接，简历解析、智能匹配、AI评测功能）
- ✅ 前端基础框架搭建
- ✅ 前端公共页面开发（登录、注册、404等）
- ✅ 求职者端页面开发（首页、简历管理、职位搜索、申请管理）
- ✅ 企业端页面开发（首页、职位管理、简历管理、企业信息）
- ✅ 管理端页面开发（仪表盘、用户管理、企业认证、系统设置）
- 🔄 功能优化和Bug修复中
- 🔄 测试和文档完善中

## 常见问题 FAQ

### Q: 如何获取火山引擎API密钥？
A: 访问[火山引擎官网](https://www.volcengine.com/)，注册账号后，在控制台中创建API密钥，确保开通了大模型相关服务权限。

### Q: 数据库如何从SQLite切换到MySQL？
A: 在`.env`文件中修改数据库连接配置为MySQL格式：
```
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```
然后重新执行数据库迁移即可。

### Q: 前端页面访问时接口报错怎么办？
A: 1. 确认后端服务是否正常启动
2. 检查前端`.env`文件中的`VITE_API_BASE_URL`配置是否正确
3. 查看浏览器控制台和后端日志定位具体错误信息

### Q: 简历上传解析失败怎么办？
A: 1. 确认简历格式为PDF或Word（.docx）
2. 简历大小不超过10MB
3. 检查火山引擎API密钥配置是否正确
4. 确认系统已安装Poppler库（用于PDF解析）

### Q: 如何开启HTTPS访问？
A: 可以使用Nginx配置SSL证书，推荐使用Let's Encrypt免费证书，配置参考：
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    # 其他配置同上...
}

# HTTP跳转HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### Q: 系统支持高并发吗？
A: 系统架构支持水平扩展，可以通过以下方式提升并发能力：
1. 增加后端服务节点，使用负载均衡分发请求
2. 使用Redis缓存热点数据，减轻数据库压力
3. 数据库采用主从复制、分库分表等方案
4. 静态资源使用CDN加速

## 许可证

本项目采用 [MIT 许可证](LICENSE) 开源，您可以自由使用、修改和分发本项目代码，但需要保留原作者版权声明。

```
MIT License

Copyright (c) 2026 SmartHr Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 贡献指南

我们欢迎任何形式的贡献，包括但不限于提交Issue、修复Bug、新增功能、完善文档等。

### 贡献流程

1. **Fork 本仓库**
   - 点击页面右上角的Fork按钮，将项目仓库复制到自己的账号下

2. **Clone 仓库到本地**
   ```bash
   git clone https://github.com/your-username/SmartHr.git
   cd SmartHr
   ```

3. **创建功能分支**
   ```bash
   # 新功能开发
   git checkout -b feature/your-feature-name

   # Bug修复
   git checkout -b fix/your-bug-fix
   ```

4. **提交代码**
   - 代码提交信息请遵循约定式提交规范：
     - `feat: 新功能描述`
     - `fix: Bug修复描述`
     - `docs: 文档更新`
     - `style: 代码格式调整（不影响逻辑）`
     - `refactor: 代码重构`
     - `test: 测试相关修改`
     - `chore: 构建/工具链等辅助工具的变动`

5. **推送分支到远程**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **提交 Pull Request**
   - 在GitHub页面提交Pull Request，详细描述修改内容和目的
   - 等待代码审核，根据审核意见进行修改

### 代码规范

- **后端（Python）**：遵循PEP 8规范，使用Black进行代码格式化
- **前端（Vue/JavaScript）**：遵循ESLint规范，使用Prettier进行代码格式化
- 提交前请确保代码通过所有测试
- 新增功能请补充相应的单元测试和文档

### 提交Issue

- 提交Issue前请先搜索是否已有相关问题
- 详细描述问题重现步骤、环境信息和期望结果
- 功能建议请说明使用场景和预期收益

### 社区交流

- 如有问题可以在Issue区提问
- 欢迎加入开发者交流群共同讨论项目发展
