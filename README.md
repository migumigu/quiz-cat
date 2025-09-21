# Quiz Cat - 智能学习平台

Quiz Cat是一个面向小学生的智能学习平台，通过游戏化的方式帮助学生巩固课堂知识，提高学习兴趣。

## 项目概述

Quiz Cat平台基于关卡式学习模式，将教材内容按照年级、学科、单元和关卡进行组织，学生可以通过完成不同类型的题目来解锁新的关卡，实现循序渐进的学习过程。

## 功能特点

- **多样化题型支持**：支持选择题、判断题、填空题和连线题等多种题型
- **关卡式学习**：按照教材单元划分关卡，通过完成当前关卡解锁下一关卡
- **进度追踪**：记录学生的学习进度和答题情况
- **即时反馈**：答题后立即获得结果反馈和解析
- **知识点分析**：根据答题情况分析学生对不同知识点的掌握程度
- **游戏化元素**：通过生命值、关卡挑战等游戏化元素提高学习兴趣

## 技术栈

- **后端**：Flask (Python)
- **数据库**：SQLite + SQLAlchemy ORM
- **前端**：HTML, CSS, JavaScript
- **认证**：Flask-Login
- **表单处理**：Flask-WTF

## 项目结构

```
quiz-cat/
├── app.py                  # 应用程序入口
├── forms.py                # 表单定义
├── init_db.py              # 数据库初始化
├── init_questions.py       # 题目数据初始化
├── models.py               # 数据库模型
├── question_handlers.py    # 题型处理器
├── question_routes.py      # 题目相关路由
├── requirements.txt        # 依赖包列表
├── routes.py               # 主要路由
├── update_progress.py      # 进度更新逻辑
├── instance/               # 实例文件夹（包含数据库）
├── migrations/             # 数据库迁移文件
├── static/                 # 静态资源
│   ├── css/                # 样式表
│   └── js/                 # JavaScript文件
└── templates/              # HTML模板
    └── quiz/               # 题目相关模板
        ├── components/     # 可复用组件
        └── types/          # 不同题型模板
```

## 安装指南

1. 克隆仓库
```bash
git clone https://github.com/yourusername/quiz-cat.git
cd quiz-cat
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 初始化数据库
```bash
python init_db.py
```

5. 运行应用
```bash
python app.py
```

应用将在 http://localhost:5003 上运行。

## 使用说明

1. 注册/登录账户
2. 选择年级和课程
3. 进入游戏界面，选择要学习的单元和关卡
4. 完成关卡中的题目，解锁新的关卡
5. 查看学习进度和成绩分析

## 数据模型

- **User**: 用户信息和认证
- **Course**: 课程信息（年级、学科、学期）
- **Unit**: 教学单元
- **Level**: 学习关卡
- **Question**: 题目基类
- **MultipleChoiceQuestion**: 选择题
- **TrueFalseQuestion**: 判断题
- **UserProgress**: 用户学习进度
- **UserAnswer**: 用户答题记录
- **KnowledgePoint**: 知识点

## 开发计划

- [ ] 添加更多题型支持（如排序题、组合题等）
- [ ] 实现错题本功能
- [ ] 添加家长监督功能
- [ ] 开发教师管理界面
- [ ] 支持更多学科和年级

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

[MIT](LICENSE)