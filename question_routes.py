from flask import render_template, request, redirect, url_for, session, jsonify
from models import db, Question, MultipleChoiceQuestion, TrueFalseQuestion, UserAnswer, Level, User

def register_question_routes(app):
    @app.route('/level/<int:level_id>/questions')
    def level_questions(level_id):
        """显示关卡的所有题目列表"""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        level = Level.query.get_or_404(level_id)
        questions = Question.query.filter_by(level_id=level_id).all()
        
        # 获取用户已答题记录
        user_id = session['user_id']
        answered_questions = {
            ua.question_id: ua 
            for ua in UserAnswer.query.filter_by(user_id=user_id).filter(
                UserAnswer.question_id.in_([q.id for q in questions])
            ).all()
        }
        
        return render_template('question_list.html', 
                              level=level, 
                              questions=questions,
                              answered_questions=answered_questions)
    
    @app.route('/question/<int:question_id>')
    def show_question(question_id):
        """显示单个题目"""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        question = Question.query.get_or_404(question_id)
        
        # 根据题目类型加载不同的模板
        if question.question_type == 'multiple_choice':
            question = MultipleChoiceQuestion.query.get(question_id)
            template = 'multiple_choice_question.html'
        elif question.question_type == 'true_false':
            question = TrueFalseQuestion.query.get(question_id)
            template = 'true_false_question.html'
        else:
            return "不支持的题目类型", 400
        
        # 获取用户之前的答题记录
        user_id = session['user_id']
        user_answer = UserAnswer.query.filter_by(
            user_id=user_id, 
            question_id=question_id
        ).first()
        
        return render_template(template, 
                              question=question, 
                              user_answer=user_answer,
                              level=question.level)
    
    @app.route('/question/<int:question_id>/answer', methods=['POST'])
    def answer_question(question_id):
        """提交题目答案"""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        question = Question.query.get_or_404(question_id)
        
        # 获取用户答案
        answer_content = None
        is_correct = False
        score = 0
        
        if question.question_type == 'multiple_choice':
            question = MultipleChoiceQuestion.query.get(question_id)
            # 获取用户选择的选项
            selected_options = request.form.getlist('option')
            answer_content = selected_options
            
            # 判断答案是否正确
            is_correct = set(selected_options) == set(question.correct_answer)
            score = question.score if is_correct else 0
            
        elif question.question_type == 'true_false':
            question = TrueFalseQuestion.query.get(question_id)
            # 获取用户的判断
            user_answer_value = request.form.get('answer') == 'true'
            answer_content = user_answer_value
            
            # 判断答案是否正确
            is_correct = user_answer_value == question.correct_answer
            score = question.score if is_correct else 0
        
        # 保存用户答题记录
        existing_answer = UserAnswer.query.filter_by(
            user_id=user_id, 
            question_id=question_id
        ).first()
        
        if existing_answer:
            # 更新现有记录
            existing_answer.answer_content = answer_content
            existing_answer.is_correct = is_correct
            existing_answer.score = score
        else:
            # 创建新记录
            new_answer = UserAnswer(
                user_id=user_id,
                question_id=question_id,
                answer_content=answer_content,
                is_correct=is_correct,
                score=score,
                time_spent=request.form.get('time_spent', 0, type=int)
            )
            db.session.add(new_answer)
        
        db.session.commit()
        
        # 检查是否完成了所有题目
        level_id = question.level_id
        total_questions = Question.query.filter_by(level_id=level_id).count()
        answered_questions = UserAnswer.query.filter_by(user_id=user_id).filter(
            UserAnswer.question_id.in_([
                q.id for q in Question.query.filter_by(level_id=level_id).all()
            ])
        ).count()
        
        if answered_questions >= total_questions:
            # 如果所有题目都已回答，更新关卡状态为已完成
            from update_progress import update_level_progress
            update_level_progress(user_id, level_id, 'completed')
        
        # 返回结果
        return render_template('question_result.html',
                              question=question,
                              is_correct=is_correct,
                              score=score,
                              answer_content=answer_content,
                              level_id=level_id,
                              all_completed=(answered_questions >= total_questions))
    
    @app.route('/level/<int:level_id>/result')
    def level_result(level_id):
        """显示关卡的答题结果"""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        level = Level.query.get_or_404(level_id)
        questions = Question.query.filter_by(level_id=level_id).all()
        
        # 获取用户在此关卡的所有答题记录
        user_answers = {
            ua.question_id: ua 
            for ua in UserAnswer.query.filter_by(user_id=user_id).filter(
                UserAnswer.question_id.in_([q.id for q in questions])
            ).all()
        }
        
        # 计算得分和正确率
        total_score = sum(q.score for q in questions)
        user_score = sum(ua.score for ua in user_answers.values())
        correct_count = sum(1 for ua in user_answers.values() if ua.is_correct)
        accuracy = correct_count / len(questions) * 100 if questions else 0
        
        # 按知识点分类统计
        knowledge_points = {}
        for q in questions:
            for kp in q.knowledge_points:
                if kp.name not in knowledge_points:
                    knowledge_points[kp.name] = {
                        'total': 0,
                        'correct': 0,
                        'accuracy': 0
                    }
                knowledge_points[kp.name]['total'] += 1
                if q.id in user_answers and user_answers[q.id].is_correct:
                    knowledge_points[kp.name]['correct'] += 1
        
        # 计算每个知识点的正确率
        for kp in knowledge_points:
            knowledge_points[kp]['accuracy'] = (
                knowledge_points[kp]['correct'] / knowledge_points[kp]['total'] * 100
                if knowledge_points[kp]['total'] > 0 else 0
            )
        
        return render_template('level_result.html',
                              level=level,
                              questions=questions,
                              user_answers=user_answers,
                              total_score=total_score,
                              user_score=user_score,
                              accuracy=accuracy,
                              knowledge_points=knowledge_points)