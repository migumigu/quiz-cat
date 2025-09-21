# Quiz Cat - 智能学习平台 Docker镜像

![Docker Image Version](https://img.shields.io/docker/v/aidedaijiayang/quiz-cat/latest)
![Docker Image Size](https://img.shields.io/docker/image-size/aidedaijiayang/quiz-cat/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/aidedaijiayang/quiz-cat)

## 功能特性
- 面向小学生的智能学习平台
- 支持数学、语文等学科题库
- 游戏化学习体验
- 多架构支持（ARM/x86）

## 快速开始

### 单容器运行
```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  aidedaijiayang/quiz-cat:latest
```

### 使用Docker Compose
1. 创建`docker-compose.yml`文件
2. 启动服务：
```bash
docker-compose up -d
```
3. 访问应用：
```bash
open "http://localhost:5000"
```

## 环境变量
| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| FLASK_ENV | production | 运行环境 |
| DATABASE_URL | sqlite:///instance/quiz.db | 数据库连接 |

## 数据持久化

### 单容器方式
```bash
docker run -d -p 5000:5000 \
  -v /path/to/data:/app/instance \
  aidedaijiayang/quiz-cat:latest
```

### Compose方式
自动通过命名卷`quiz-data`持久化数据，查看数据卷位置：
```bash
docker volume inspect quiz-cat_quiz-data
```

## 技术支持
问题反馈：aidedaijia@gmail.com