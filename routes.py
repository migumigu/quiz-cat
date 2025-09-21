from flask import render_template, redirect, url_for, request, flash, session
from models import db, User, Level, Question, Course, Unit, UserProgress
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm

def question_to_dict(question):
    """将Question对象转换为可序列化的字典"""
    result = {
        'id': question.id,
        'content': question.content,
        'question_type': question.question_type,
        'score': question.score,
        'order': question.order,
        'explanation': getattr(question, 'explanation', '') or ''
    }
    
    # 使用属性方法获取选项和正确答案
    try:
        if hasattr(question, 'options'):
            result['options'] = question.options
        else:
            result['options'] = []
            
        if hasattr(question, 'correct_answer'):
            result['correct_answer'] = question.correct_answer
        else:
            result['correct_answer'] = 0
            
    except Exception as e:
        # 如果属性访问失败，使用默认值
        result['options'] = []
        result['correct_answer'] = 0
    
    return result

def init_routes(app):
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('select_course'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        # 完全禁用CSRF验证进行测试
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password:
                user = User.query.filter_by(username=username).first()
                if user:
                    print(f"Found user: {user.username}")
                    if user.check_password(password):
                        print("Password check passed")
                        login_user(user)
                        print("User logged in successfully")
                        return redirect(url_for('select_course'))
                    else:
                        print("Password check failed")
                else:
                    print("User not found")
                flash('用户名或密码错误')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/grade-selection')
    @login_required
    def grade_selection():
        return render_template('grade_selection.html')

    @app.route('/select-course')
    @login_required
    def select_course():
        # 检查用户是否有上次选择的年级和课程
        if current_user.last_grade and current_user.last_course:
            # 如果用户有上次选择的课程，直接重定向到课程信息页面
            return redirect(url_for('selected_course', 
                                  grade=current_user.last_grade, 
                                  course=current_user.last_course))
        elif current_user.last_grade:
            # 如果只有年级没有课程，显示课程选择页面
            courses = {
                '语文': ['上册', '下册'],
                '数学': ['上册', '下册'], 
                '英语': ['上册', '下册']
            }
            return render_template('course_selection.html',
                                 grade=current_user.last_grade,
                                 courses=courses)
        else:
            # 如果没有上次选择的年级，重定向到年级选择页面
            return redirect(url_for('grade_selection'))

    @app.route('/course-selection/<grade>')
    @login_required
    def course_selection(grade):
        # 显示特定年级的课程选择页面
        courses = {
            '语文': ['上册', '下册'],
            '数学': ['上册', '下册'], 
            '英语': ['上册', '下册']
        }
        return render_template('course_selection.html',
                             grade=grade,
                             courses=courses)

    @app.route('/selected-course/<grade>/<course>')
    @login_required
    def selected_course(grade, course):
        # 获取课程数据 (按年级和完整课程名称查询)
        course_obj = Course.query.filter(
            Course.grade == grade,
            db.or_(
                db.func.concat(Course.subject, Course.term) == course,
                db.func.concat(Course.subject, ' ', Course.term) == course
            )
        ).first_or_404()
        
        # 加载关联的单元和关卡数据
        units = Unit.query.filter_by(course_id=course_obj.id).order_by(Unit.order).all()
        
        # 为每个单元加载关卡
        for unit in units:
            unit.levels = Level.query.filter_by(unit_id=unit.id).order_by(Level.order).all()
        
        # 将单元数据附加到课程对象
        course_obj.units = units
        
        # 记录用户选择的课程
        current_user.last_grade = grade
        current_user.last_course = f"{course_obj.subject}{course_obj.term}"
        db.session.commit()
        
        # 渲染课程信息页面（有开始答题和切换课程按钮）
        return render_template('selected_course.html',
                             course=course_obj)

    @app.route('/quiz/<int:level_id>')
    @login_required
    def quiz(level_id):
        level = Level.query.get_or_404(level_id)
        return redirect(url_for('quiz_question', level_id=level_id, question_index=0))

    @app.route('/quiz/<int:level_id>/<int:question_index>')
    @login_required
    def quiz_question(level_id, question_index):
        level = Level.query.get_or_404(level_id)
        questions = sorted(level.questions, key=lambda q: q.order or 0)
        current_question = questions[question_index]
        
        # 获取生命值（从session或查询参数）
        hearts = request.args.get('hearts', session.get('hearts', 3), type=int)
        session['hearts'] = hearts
        
        # 准备模板数据
        correct_messages = [
            "太棒了！答对了！", "真厉害！继续加油！", "完美！答案正确！",
            "聪明！完全正确！", "优秀！继续保持！", "答对了！你真棒！"
        ]
        
        wrong_messages = [
            "再仔细想想～", "差一点点就对了", "这个有点难呢",
            "别灰心，继续努力", "再试一次吧", "加油，你可以的"
        ]
        
        return render_template('quiz.html',
                           current_question=question_to_dict(current_question),
                           questions=[question_to_dict(q) for q in questions],
                           level=level,
                           question_index=question_index,
                           total_questions=len(questions),
                           hearts=hearts,
                           correct_messages=correct_messages,
                           wrong_messages=wrong_messages)

    @app.route('/game/<int:course_id>')
    @login_required
    def game(course_id):
        course = Course.query.get_or_404(course_id)
        units = Unit.query.filter_by(course_id=course.id).order_by(Unit.order).all()
        
        # 获取所有关卡的ID
        level_ids = []
        for unit in units:
            for level in unit.levels:
                level_ids.append(level.id)

        # 获取当前用户的进度数据
        user_id = current_user.id
        progress = {
            p.level_id: p.status
            for p in UserProgress.query.filter_by(user_id=user_id).filter(
                UserProgress.level_id.in_(level_ids)
            ).all()
        }

        # 为没有进度记录的关卡创建默认的'locked'状态
        for level_id in level_ids:
            if level_id not in progress:
                progress[level_id] = 'locked'
                new_progress = UserProgress(
                    user_id=user_id,
                    level_id=level_id,
                    status='locked'
                )
                db.session.add(new_progress)

        db.session.commit()

        return render_template('game.html',
            course=course,
            units=units,
            progress=progress
        )

