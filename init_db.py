import os
from models import db, User, Course, Unit, Level, UserProgress
from init_questions import init_question_data

def create_tables(app):
    with app.app_context():
        if not os.path.exists('instance'):
            os.makedirs('instance')
        try:
            db.create_all()
            init_sample_data()
            init_question_data()  # 初始化题目数据
            print("数据库初始化成功")
        except Exception as e:
            print(f"数据库初始化失败: {str(e)}")

def init_sample_data():
    if Course.query.count() > 0:
        return

    chinese_course = Course(
        grade="三年级",
        subject="语文",
        term="上册"
    )
    db.session.add(chinese_course)
    db.session.flush()

    units = [
        {
            "name": "童话世界",
            "levels": [
                {"title": "大青树下的小学", "content_ref": "第1课"},
                {"title": "花的学校", "content_ref": "第2课"},
                {"title": "不懂就要问", "content_ref": "第3课"},
                {"title": "单元挑战", "is_boss": True}
            ]
        },
        {
            "name": "金秋时节", 
            "levels": [
                {"title": "古诗三首", "content_ref": "第4课"},
                {"title": "铺满金色巴掌的水泥道", "content_ref": "第5课"},
                {"title": "秋天的雨", "content_ref": "第6课"},
                {"title": "听听，秋的声音", "content_ref": "第7课"},
                {"title": "单元挑战", "is_boss": True}
            ]
        },
        {
            "name": "童话王国",
            "levels": [
                {"title": "去年的树", "content_ref": "第8课"},
                {"title": "那一定会很好", "content_ref": "第9课"},
                {"title": "在牛肚子里旅行", "content_ref": "第10课"},
                {"title": "单元挑战", "is_boss": True}
            ]
        },
        {
            "name": "期中综合挑战",
            "levels": [
                {"title": "期中大挑战", "is_midterm": True}
            ]
        },
        {
            "name": "预测与推理",
            "levels": [
                {"title": "总也倒不了的老屋", "content_ref": "第12课"},
                {"title": "胡萝卜先生的长胡子", "content_ref": "第13课"},
                {"title": "不会叫的狗", "content_ref": "第14课"},
                {"title": "单元挑战", "is_boss": True}
            ]
        },
        {
            "name": "观察与发现",
            "levels": [
                {"title": "搭船的鸟", "content_ref": "第15课"},
                {"title": "金色的草地", "content_ref": "第16课"},
                {"title": "单元挑战", "is_boss": True}
            ]
        },
        {
            "name": "祖国山河",
            "levels": [
                {"title": "古诗三首", "content_ref": "第17课"},
                {"title": "富饶的西沙群岛", "content_ref": "第18课"},
                {"title": "海滨小城", "content_ref": "第19课"},
                {"title": "美丽的小兴安岭", "content_ref": "第20课"},
                {"title": "单元挑战", "is_boss": True}
            ]
        },
        {
            "name": "期末综合挑战",
            "levels": [
                {"title": "期末大挑战", "is_final": True}
            ]
        }
    ]

    for unit_order, unit_data in enumerate(units, 1):
        unit = Unit(
            course_id=chinese_course.id,
            name=unit_data["name"],
            order=unit_order
        )
        db.session.add(unit)
        db.session.flush()

        for level_order, level_data in enumerate(unit_data["levels"], 1):
            level = Level(
                unit_id=unit.id,
                title=level_data["title"],
                content_ref=level_data.get("content_ref"),
                is_boss=level_data.get("is_boss", False),
                is_midterm=level_data.get("is_midterm", False),
                is_final=level_data.get("is_final", False),
                order=level_order
            )
            db.session.add(level)

    db.session.commit()
    
    test_user = User.query.filter_by(username='test').first()
    if test_user:
        first_unit = Unit.query.filter_by(order=1).first()
        if first_unit:
            levels = Level.query.filter_by(unit_id=first_unit.id).order_by(Level.order).all()
            for i, level in enumerate(levels[:2], 1):
                progress = UserProgress(
                    user_id=test_user.id,
                    level_id=level.id,
                    status='completed' if i == 1 else 'unlocked'
                )
                db.session.add(progress)
    
    db.session.commit()