"""
题型处理器模块
用于处理不同题型的渲染和验证逻辑
"""

from flask import render_template
import json

class QuestionHandler:
    """题型处理器基类"""
    
    def get_template(self):
        """获取题型模板"""
        raise NotImplementedError("子类必须实现此方法")
    
    def render_question(self, question, **kwargs):
        """渲染题目"""
        return render_template(self.get_template(), current_question=question, **kwargs)
    
    def validate_answer(self, question, form_data):
        """验证答案"""
        raise NotImplementedError("子类必须实现此方法")
    
    def get_js_files(self):
        """获取题型特定的JS文件"""
        return ['/static/js/quiz/core.js']


class MultipleChoiceHandler(QuestionHandler):
    """选择题处理器"""
    
    def get_template(self):
        return "quiz/types/multiple_choice.html"
    
    def validate_answer(self, question, form_data):
        selected = form_data.get('answer')
        if selected is None:
            return False
        return int(selected) == question.correct_answer
    
    def get_js_files(self):
        return super().get_js_files() + ['/static/js/quiz/types/multiple_choice.js']


class TrueFalseHandler(QuestionHandler):
    """判断题处理器"""
    
    def get_template(self):
        return "quiz/types/true_false.html"
    
    def validate_answer(self, question, form_data):
        selected = form_data.get('answer')
        if selected is None:
            return False
        return selected == question.correct_answer
    
    def get_js_files(self):
        return super().get_js_files() + ['/static/js/quiz/types/true_false.js']


class FillBlankHandler(QuestionHandler):
    """填空题处理器"""
    
    def get_template(self):
        return "quiz/types/fill_blank.html"
    
    def validate_answer(self, question, form_data):
        # 获取用户答案
        if question.blanks_count and question.blanks_count > 1:
            # 多个填空
            user_answers = []
            for i in range(question.blanks_count):
                user_answers.append(form_data.get(f'answer-{i}', '').strip().lower())
            
            # 获取正确答案
            correct_answers = question.correct_answer
            
            # 检查每个填空是否正确
            if len(user_answers) != len(correct_answers):
                return False
                
            for i, user_answer in enumerate(user_answers):
                # 如果正确答案是列表（多个可能的正确答案）
                if isinstance(correct_answers[i], list):
                    if not any(self._compare_answers(user_answer, ans) for ans in correct_answers[i]):
                        return False
                else:
                    if not self._compare_answers(user_answer, correct_answers[i]):
                        return False
            
            return True
        else:
            # 单个填空
            user_answer = form_data.get('answer', '').strip().lower()
            correct_answer = question.correct_answer
            
            # 如果正确答案是列表（多个可能的正确答案）
            if isinstance(correct_answer, list):
                return any(self._compare_answers(user_answer, ans) for ans in correct_answer)
            else:
                return self._compare_answers(user_answer, correct_answer)
    
    def _compare_answers(self, user_answer, correct_answer):
        """比较答案，支持忽略标点符号"""
        # 转换为小写并去除首尾空格
        user_answer = user_answer.lower().strip()
        correct_answer = str(correct_answer).lower().strip()
        
        # 精确匹配
        if user_answer == correct_answer:
            return True
        
        # 忽略标点符号的匹配
        user_answer_no_punct = ''.join(c for c in user_answer if c.isalnum() or c.isspace())
        correct_answer_no_punct = ''.join(c for c in correct_answer if c.isalnum() or c.isspace())
        
        return user_answer_no_punct == correct_answer_no_punct
    
    def get_js_files(self):
        return super().get_js_files() + ['/static/js/quiz/types/fill_blank.js']
    
    def render_question(self, question, **kwargs):
        """渲染题目，添加正确答案数据"""
        context = kwargs.copy()
        
        # 添加正确答案数据，用于前端验证
        context['correct_answers_json'] = json.dumps(question.correct_answer)
        
        return super().render_question(question, **context)


class MatchingHandler(QuestionHandler):
    """连线题处理器"""
    
    def get_template(self):
        return "quiz/types/matching.html"
    
    def validate_answer(self, question, form_data):
        # 获取用户匹配结果
        try:
            user_matches = json.loads(form_data.get('matching_result', '[]'))
        except json.JSONDecodeError:
            return False
        
        # 获取正确匹配
        correct_matches = question.correct_matches
        
        # 如果匹配数量不一致，则不正确
        if len(user_matches) != len(correct_matches):
            return False
        
        # 检查每个匹配是否正确
        for correct_match in correct_matches:
            # 查找用户匹配中是否有对应的匹配
            found = False
            for user_match in user_matches:
                if (user_match.get('left') == correct_match.get('left') and 
                    user_match.get('right') == correct_match.get('right')):
                    found = True
                    break
            
            # 如果没有找到对应的匹配，则不正确
            if not found:
                return False
        
        return True
    
    def get_js_files(self):
        return super().get_js_files() + ['/static/js/quiz/types/matching.js']
    
    def render_question(self, question, **kwargs):
        """渲染题目，添加正确匹配数据"""
        context = kwargs.copy()
        
        # 添加正确匹配数据，用于前端验证
        context['correct_matches_json'] = json.dumps(question.correct_matches)
        
        return super().render_question(question, **context)


class QuestionHandlerFactory:
    """题型处理器工厂"""
    
    @staticmethod
    def get_handler(question_type):
        """根据题型获取处理器"""
        handlers = {
            'multiple_choice': MultipleChoiceHandler,
            'true_false': TrueFalseHandler,
            'fill_blank': FillBlankHandler,
            'matching': MatchingHandler
        }
        
        handler_class = handlers.get(question_type)
        if handler_class:
            return handler_class()
        else:
            # 默认使用选择题处理器
            return MultipleChoiceHandler()