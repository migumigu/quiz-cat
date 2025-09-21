import os
from models import db, Question, MultipleChoiceQuestion, TrueFalseQuestion, KnowledgePoint, Level, Unit, Course

def init_question_data():
    """初始化题目数据"""
    # 检查是否已经有题目数据
    if Question.query.count() > 0:
        print("题目数据已存在，跳过初始化")
        return
    
    print("开始初始化题目数据...")
    
    # 获取三年级语文上册第一单元
    course = Course.query.filter_by(grade="三年级", subject="语文", term="上册").first()
    if not course:
        print("未找到三年级语文上册课程")
        return
    
    unit = Unit.query.filter_by(course_id=course.id, name="童话世界").first()
    if not unit:
        print("未找到童话世界单元")
        return
    
    # 获取单元下的所有关卡
    levels = Level.query.filter_by(unit_id=unit.id).order_by(Level.order).all()
    if not levels:
        print("未找到关卡数据")
        return
    
    # 创建知识点
    knowledge_points = {
        "课文内容理解": KnowledgePoint(name="课文内容理解", category="阅读"),
        "词语理解": KnowledgePoint(name="词语理解", category="词汇"),
        "词语辨析": KnowledgePoint(name="词语辨析", category="词汇"),
        "文体特征": KnowledgePoint(name="文体特征", category="文学常识"),
        "中心思想理解": KnowledgePoint(name="中心思想理解", category="阅读"),
        "人物性格分析": KnowledgePoint(name="人物性格分析", category="阅读"),
        "主题归纳": KnowledgePoint(name="主题归纳", category="阅读"),
        "字词辨析": KnowledgePoint(name="字词辨析", category="词汇"),
        "成语运用": KnowledgePoint(name="成语运用", category="词汇"),
        "文学常识": KnowledgePoint(name="文学常识", category="文学常识")
    }
    
    for kp in knowledge_points.values():
        db.session.add(kp)
    
    db.session.flush()
    
    # 第1课：大青树下的小学
    level1 = levels[0]  # 大青树下的小学
    
    # 选择题
    q1 = MultipleChoiceQuestion(
        level_id=level1.id,
        content="课文《大青树下的小学》中，小鸟们的学校在哪里？",
        difficulty=1,
        score=5,
        options=[
            {"id": "A", "content": "大青树上"},
            {"id": "B", "content": "森林里"},
            {"id": "C", "content": "草地上"},
            {"id": "D", "content": "河边"}
        ],
        correct_answer=["A"],
        explanation="课文中描述小鸟们的学校在大青树上。"
    )
    q1.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(q1)
    
    q2 = MultipleChoiceQuestion(
        level_id=level1.id,
        content="小鸟们在学校里主要学习什么？",
        difficulty=1,
        score=5,
        options=[
            {"id": "A", "content": "写字和算术"},
            {"id": "B", "content": "唱歌和飞行"},
            {"id": "C", "content": "筑巢和捉虫"},
            {"id": "D", "content": "画画和跳舞"}
        ],
        correct_answer=["B"],
        explanation="课文中描述小鸟们在学校里学习唱歌和飞行。"
    )
    q2.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(q2)
    
    q3 = MultipleChoiceQuestion(
        level_id=level1.id,
        content="\"叽叽喳喳\"是形容什么声音的词语？",
        difficulty=1,
        score=5,
        options=[
            {"id": "A", "content": "流水的声音"},
            {"id": "B", "content": "风吹树叶的声音"},
            {"id": "C", "content": "小鸟的声音"},
            {"id": "D", "content": "虫子的声音"}
        ],
        correct_answer=["C"],
        explanation="\"叽叽喳喳\"是形容小鸟叫声的拟声词。"
    )
    q3.knowledge_points.append(knowledge_points["词语理解"])
    db.session.add(q3)
    
    q4 = MultipleChoiceQuestion(
        level_id=level1.id,
        content="下列词语中，哪一个是描写树木高大的？",
        difficulty=2,
        score=5,
        options=[
            {"id": "A", "content": "茂盛"},
            {"id": "B", "content": "挺拔"},
            {"id": "C", "content": "茂密"},
            {"id": "D", "content": "繁茂"}
        ],
        correct_answer=["B"],
        explanation="\"挺拔\"形容树木又高又直，形态挺秀。"
    )
    q4.knowledge_points.append(knowledge_points["词语辨析"])
    db.session.add(q4)
    
    # 判断题
    t1 = TrueFalseQuestion(
        level_id=level1.id,
        content="《大青树下的小学》是一篇童话故事。",
        difficulty=1,
        score=3,
        correct_answer=True,
        explanation="《大青树下的小学》是一篇童话故事，通过拟人化的手法描写小鸟学校的情景。"
    )
    t1.knowledge_points.append(knowledge_points["文体特征"])
    db.session.add(t1)
    
    t2 = TrueFalseQuestion(
        level_id=level1.id,
        content="课文中的小鸟老师教小鸟们认字和算术。",
        difficulty=1,
        score=3,
        correct_answer=False,
        explanation="课文中的小鸟老师教小鸟们唱歌和飞行，而不是认字和算术。"
    )
    t2.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(t2)
    
    t3 = TrueFalseQuestion(
        level_id=level1.id,
        content="\"婉转\"一词可以用来形容小鸟唱歌的声音好听。",
        difficulty=2,
        score=3,
        correct_answer=True,
        explanation="\"婉转\"形容声音柔和、悦耳，常用来形容小鸟的歌声。"
    )
    t3.knowledge_points.append(knowledge_points["词语理解"])
    db.session.add(t3)
    
    t4 = TrueFalseQuestion(
        level_id=level1.id,
        content="课文中的小鸟学校只在春天开课。",
        difficulty=2,
        score=3,
        correct_answer=False,
        explanation="课文中没有提到小鸟学校只在春天开课。"
    )
    t4.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(t4)
    
    # 第2课：花的学校
    level2 = levels[1]  # 花的学校
    
    # 选择题
    q5 = MultipleChoiceQuestion(
        level_id=level2.id,
        content="《花的学校》中，谁是花朵们的老师？",
        difficulty=1,
        score=5,
        options=[
            {"id": "A", "content": "春风"},
            {"id": "B", "content": "阳光"},
            {"id": "C", "content": "雨滴"},
            {"id": "D", "content": "泥土"}
        ],
        correct_answer=["A"],
        explanation="课文中描述春风是花朵们的老师。"
    )
    q5.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(q5)
    
    q6 = MultipleChoiceQuestion(
        level_id=level2.id,
        content="花朵们在学校里学习什么？",
        difficulty=1,
        score=5,
        options=[
            {"id": "A", "content": "如何开花"},
            {"id": "B", "content": "如何摇摆"},
            {"id": "C", "content": "如何唱歌"},
            {"id": "D", "content": "如何生长"}
        ],
        correct_answer=["C"],
        explanation="课文中描述花朵们在学校里学习如何唱歌。"
    )
    q6.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(q6)
    
    # 判断题
    t5 = TrueFalseQuestion(
        level_id=level2.id,
        content="《花的学校》这篇课文是印度诗人泰戈尔写的。",
        difficulty=2,
        score=3,
        correct_answer=True,
        explanation="《花的学校》是印度诗人泰戈尔的作品。"
    )
    t5.knowledge_points.append(knowledge_points["文学常识"])
    db.session.add(t5)
    
    t6 = TrueFalseQuestion(
        level_id=level2.id,
        content="课文中的花朵们在学校里学习如何结果实。",
        difficulty=1,
        score=3,
        correct_answer=False,
        explanation="课文中花朵们学习的是如何唱歌，而不是如何结果实。"
    )
    t6.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(t6)
    
    # 第3课：不懂就要问
    level3 = levels[2]  # 不懂就要问
    
    # 选择题
    q7 = MultipleChoiceQuestion(
        level_id=level3.id,
        content="《不懂就要问》中，小男孩不懂什么问题？",
        difficulty=1,
        score=5,
        options=[
            {"id": "A", "content": "为什么要上学"},
            {"id": "B", "content": "为什么天是蓝的"},
            {"id": "C", "content": "为什么要睡觉"},
            {"id": "D", "content": "为什么要吃饭"}
        ],
        correct_answer=["B"],
        explanation="课文中小男孩问的是为什么天是蓝的。"
    )
    q7.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(q7)
    
    q8 = MultipleChoiceQuestion(
        level_id=level3.id,
        content="课文告诉我们什么道理？",
        difficulty=2,
        score=5,
        options=[
            {"id": "A", "content": "天空是蓝色的"},
            {"id": "B", "content": "妈妈很聪明"},
            {"id": "C", "content": "不懂就要问"},
            {"id": "D", "content": "小孩子很可爱"}
        ],
        correct_answer=["C"],
        explanation="课文的中心思想是\"不懂就要问\"，鼓励人们勇于提问。"
    )
    q8.knowledge_points.append(knowledge_points["中心思想理解"])
    db.session.add(q8)
    
    # 判断题
    t7 = TrueFalseQuestion(
        level_id=level3.id,
        content="《不懂就要问》这篇课文主要讲述了小男孩问问题的故事。",
        difficulty=1,
        score=3,
        correct_answer=True,
        explanation="课文确实主要讲述了小男孩问问题的故事。"
    )
    t7.knowledge_points.append(knowledge_points["课文内容理解"])
    db.session.add(t7)
    
    t8 = TrueFalseQuestion(
        level_id=level3.id,
        content="课文的主要目的是告诉我们天为什么是蓝色的。",
        difficulty=2,
        score=3,
        correct_answer=False,
        explanation="课文的主要目的不是解释天为什么是蓝色的，而是告诉我们\"不懂就要问\"的道理。"
    )
    t8.knowledge_points.append(knowledge_points["中心思想理解"])
    db.session.add(t8)
    
    # 单元挑战
    level4 = levels[3]  # 单元挑战
    
    # 选择题
    q9 = MultipleChoiceQuestion(
        level_id=level4.id,
        content="下列哪篇课文不是童话故事？",
        difficulty=2,
        score=5,
        options=[
            {"id": "A", "content": "《大青树下的小学》"},
            {"id": "B", "content": "《花的学校》"},
            {"id": "C", "content": "《不懂就要问》"},
            {"id": "D", "content": "以上都是童话故事"}
        ],
        correct_answer=["C"],
        explanation="《不懂就要问》是一篇生活故事，而不是童话故事。"
    )
    q9.knowledge_points.append(knowledge_points["文体特征"])
    db.session.add(q9)
    
    q10 = MultipleChoiceQuestion(
        level_id=level4.id,
        content="第一单元的三篇课文都有一个共同点，是什么？",
        difficulty=3,
        score=5,
        options=[
            {"id": "A", "content": "都是写动物的"},
            {"id": "B", "content": "都是写植物的"},
            {"id": "C", "content": "都与学习有关"},
            {"id": "D", "content": "都发生在夏天"}
        ],
        correct_answer=["C"],
        explanation="第一单元的三篇课文《大青树下的小学》、《花的学校》和《不懂就要问》都与学习有关。"
    )
    q10.knowledge_points.append(knowledge_points["主题归纳"])
    db.session.add(q10)
    
    # 判断题
    t9 = TrueFalseQuestion(
        level_id=level4.id,
        content="第一单元的三篇课文都强调了学习的重要性。",
        difficulty=2,
        score=3,
        correct_answer=True,
        explanation="第一单元的三篇课文确实都强调了学习的重要性。"
    )
    t9.knowledge_points.append(knowledge_points["主题归纳"])
    db.session.add(t9)
    
    t10 = TrueFalseQuestion(
        level_id=level4.id,
        content="第一单元的课文告诉我们，只有在学校里才能学习知识。",
        difficulty=3,
        score=3,
        correct_answer=False,
        explanation="第一单元的课文并没有表达只有在学校里才能学习知识的观点，相反，《不懂就要问》强调了在生活中也可以学习。"
    )
    t10.knowledge_points.append(knowledge_points["中心思想理解"])
    db.session.add(t10)
    
    db.session.commit()
    print("题目数据初始化完成")

if __name__ == "__main__":
    # 避免循环导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from app import app
    with app.app_context():
        init_question_data()