from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_grade = db.Column(db.String(20))
    last_course = db.Column(db.String(40))

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    # Flask-Login required methods
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    units = db.relationship('Unit', backref='course', lazy=True)

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    levels = db.relationship('Level', backref='unit', lazy=True)

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    title = db.Column(db.String(100), nullable=False)
    content_ref = db.Column(db.String(100))
    is_boss = db.Column(db.Boolean, default=False)
    is_midterm = db.Column(db.Boolean, default=False)
    is_final = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, nullable=False)

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    status = db.Column(db.Enum('locked', 'unlocked', 'completed'), default='locked')
    updated_at = db.Column(db.DateTime, default=db.func.now())

# 新增题目相关模型
class Question(db.Model):
    """核心题目表"""
    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'multiple_choice', 'true_false'
    content = db.Column(db.Text, nullable=False)  # 题目内容/题干
    difficulty = db.Column(db.Integer, default=1)  # 难度级别 1-5
    score = db.Column(db.Integer, default=1)  # 分值
    order = db.Column(db.Integer, default=0)  # 题目排序
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # 关系
    level = db.relationship('Level', backref=db.backref('questions', lazy=True))
    
    # 多态关系
    __mapper_args__ = {
        'polymorphic_on': question_type,
        'polymorphic_identity': 'question'
    }

class MultipleChoiceQuestion(Question):
    """选择题表"""
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    _options = db.Column('options', db.Text, nullable=False)  # JSON格式存储选项
    _correct_answer = db.Column('correct_answer', db.Text, nullable=False)  # 正确答案，可能是单个或多个
    explanation = db.Column(db.Text)  # 解析
    
    __mapper_args__ = {
        'polymorphic_identity': 'multiple_choice',
    }
    
    @property
    def options(self):
        return json.loads(self._options)
    
    @options.setter
    def options(self, value):
        self._options = json.dumps(value)
    
    @property
    def correct_answer(self):
        return json.loads(self._correct_answer)
    
    @correct_answer.setter
    def correct_answer(self, value):
        self._correct_answer = json.dumps(value)

class TrueFalseQuestion(Question):
    """判断题表"""
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    correct_answer = db.Column(db.Boolean, nullable=False)  # 正确答案
    explanation = db.Column(db.Text)  # 解析
    
    __mapper_args__ = {
        'polymorphic_identity': 'true_false',
    }

class UserAnswer(db.Model):
    """用户答题记录表"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    _answer_content = db.Column('answer_content', db.Text, nullable=False)  # JSON格式存储用户答案
    is_correct = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    attempt_time = db.Column(db.DateTime, default=db.func.now())
    time_spent = db.Column(db.Integer)  # 花费时间（秒）
    
    # 关系
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    question = db.relationship('Question', backref=db.backref('user_answers', lazy=True))
    
    @property
    def answer_content(self):
        return json.loads(self._answer_content)
    
    @answer_content.setter
    def answer_content(self, value):
        self._answer_content = json.dumps(value)

class KnowledgePoint(db.Model):
    """知识点表"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # 类别（如"汉字"、"阅读"、"写作"等）
    description = db.Column(db.Text)
    
    # 多对多关系
    questions = db.relationship('Question', secondary='question_knowledge_point', backref=db.backref('knowledge_points', lazy=True))

class QuestionKnowledgePoint(db.Model):
    """题目-知识点关联表"""
    __tablename__ = 'question_knowledge_point'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    knowledge_point_id = db.Column(db.Integer, db.ForeignKey('knowledge_point.id'), nullable=False)