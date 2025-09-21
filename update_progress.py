from models import db, User, Course, Unit, Level, UserProgress

def update_level_progress(user_id, level_id, status):
    """
    更新用户特定关卡的进度
    
    参数:
    - user_id: 用户ID
    - level_id: 关卡ID
    - status: 新状态 ('locked', 'unlocked', 'completed')
    
    返回:
    - 更新是否成功
    """
    try:
        # 更新当前关卡状态
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            level_id=level_id
        ).first()
        
        if progress:
            progress.status = status
        else:
            progress = UserProgress(
                user_id=user_id,
                level_id=level_id,
                status=status
            )
            db.session.add(progress)
        
        # 如果当前关卡已完成，解锁下一关
        if status == 'completed':
            current_level = Level.query.get(level_id)
            if current_level:
                # 获取同一单元中的下一关
                next_level = Level.query.filter_by(
                    unit_id=current_level.unit_id,
                    order=current_level.order + 1
                ).first()
                
                if next_level:
                    next_progress = UserProgress.query.filter_by(
                        user_id=user_id,
                        level_id=next_level.id
                    ).first()
                    
                    if next_progress:
                        next_progress.status = 'unlocked'
                    else:
                        next_progress = UserProgress(
                            user_id=user_id,
                            level_id=next_level.id,
                            status='unlocked'
                        )
                        db.session.add(next_progress)
                
                # 如果是单元最后一关，并且有下一个单元，解锁下一单元的第一关
                else:
                    current_unit = Unit.query.get(current_level.unit_id)
                    next_unit = Unit.query.filter_by(
                        course_id=current_unit.course_id,
                        order=current_unit.order + 1
                    ).first()
                    
                    if next_unit:
                        first_level_of_next_unit = Level.query.filter_by(
                            unit_id=next_unit.id,
                            order=1
                        ).first()
                        
                        if first_level_of_next_unit:
                            next_progress = UserProgress.query.filter_by(
                                user_id=user_id,
                                level_id=first_level_of_next_unit.id
                            ).first()
                            
                            if next_progress:
                                next_progress.status = 'unlocked'
                            else:
                                next_progress = UserProgress(
                                    user_id=user_id,
                                    level_id=first_level_of_next_unit.id,
                                    status='unlocked'
                                )
                                db.session.add(next_progress)
        
        db.session.commit()
        return True
    except Exception as e:
        print(f"更新进度失败: {str(e)}")
        db.session.rollback()
        return False

def update_progress():
    # 创建应用上下文
    with app.app_context():
        # 获取所有用户
        users = User.query.all()
        
        for user in users:
            print(f"\n=== 正在更新用户: {user.username} ===")
            
            # 获取三年级语文上册课程
            chinese_course = Course.query.filter_by(grade="三年级", subject="语文", term="上册").first()
            if not chinese_course:
                print("未找到三年级语文上册课程")
                continue
            
            # 获取该课程的所有单元和关卡
            units = Unit.query.filter_by(course_id=chinese_course.id).order_by(Unit.order).all()
            
            print("=== 更新语文进度 ===")
            for unit in units:
                levels = Level.query.filter_by(unit_id=unit.id).order_by(Level.order).all()
                
                for i, level in enumerate(levels):
                    # 特殊关卡处理（期中/期末）
                    if level.is_midterm or level.is_final:
                        status = 'unlocked'
                    # 单元第一关默认解锁
                    elif i == 0:
                        status = 'unlocked'
                    # 其他关卡基于前一关状态
                    else:
                        prev_level = Level.query.filter_by(
                            unit_id=unit.id,
                            order=level.order-1
                        ).first()
                        prev_progress = UserProgress.query.filter_by(
                            user_id=user.id,
                            level_id=prev_level.id
                        ).first() if prev_level else None
                        
                        # 如果前一关已完成则解锁当前关
                        status = 'unlocked' if (prev_progress and prev_progress.status == 'completed') else 'locked'
                    
                    # 测试用户特殊处理：第一单元前两关completed
                    if user.username == 'test' and unit.order == 1 and i < 2:
                        status = 'completed'
                    
                    # 更新或创建进度记录
                    progress = UserProgress.query.filter_by(
                        user_id=user.id,
                        level_id=level.id
                    ).first()
                    
                    if progress:
                        progress.status = status
                    else:
                        progress = UserProgress(
                            user_id=user.id,
                            level_id=level.id,
                            status=status
                        )
                        db.session.add(progress)
                    
                    print(f"关卡: {level.title}, 状态: {status}")
            
            # 提交更改
            db.session.commit()
            print(f"用户 {user.username} 进度更新完成！")
    
        # 获取课程信息
        print("=== 课程信息 ===")
        courses = Course.query.all()
        for c in courses:
            print(f"ID: {c.id}, 年级: {c.grade}, 科目: {c.subject}, 学期: {c.term}")
    
        # 获取三年级语文上册课程
        chinese_course = Course.query.filter_by(grade="三年级", subject="语文", term="上册").first()
        if not chinese_course:
            print("未找到三年级语文上册课程")
            return
        
        # 获取该课程的所有单元和关卡
        units = Unit.query.filter_by(course_id=chinese_course.id).order_by(Unit.order).all()
    
        # 更新进度 - 第一单元全部完成，第二单元部分完成
        print("\n=== 更新语文进度 ===")
        for unit in units[:2]:  # 只处理前两个单元
            levels = Level.query.filter_by(unit_id=unit.id).order_by(Level.order).all()
            
            for i, level in enumerate(levels):
                # 特殊关卡处理（期中/期末）
                if level.is_midterm or level.is_final:
                    status = 'unlocked'
                # 单元第一关默认解锁
                elif i == 0:
                    status = 'unlocked'
                # 其他关卡基于前一关状态
                else:
                    prev_level = Level.query.filter_by(
                        unit_id=unit.id,
                        order=level.order-1
                    ).first()
                    prev_progress = UserProgress.query.filter_by(
                        user_id=test_user.id,
                        level_id=prev_level.id
                    ).first() if prev_level else None
                    
                    # 如果前一关已完成则解锁当前关
                    status = 'unlocked' if (prev_progress and prev_progress.status == 'completed') else 'locked'
                
                # 测试用户特殊处理：第一单元前两关completed
                if test_user.username == 'test' and unit.order == 1 and i < 2:
                    status = 'completed'
                
                # 更新或创建进度记录
                progress = UserProgress.query.filter_by(
                    user_id=test_user.id,
                    level_id=level.id
                ).first()
                
                if progress:
                    progress.status = status
                else:
                    progress = UserProgress(
                        user_id=test_user.id,
                        level_id=level.id,
                        status=status
                    )
                    db.session.add(progress)
                
                print(f"关卡: {level.title}, 状态: {status}")
        
        # 提交更改
        db.session.commit()
        print("\n进度更新完成！")

if __name__ == "__main__":
    update_progress()