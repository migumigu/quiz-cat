// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 添加按钮点击动画
    const buttons = document.querySelectorAll('.grade-btn, .course-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });

    // 关卡卡片点击事件
    const levelCards = document.querySelectorAll('.level-card.unlocked, .level-card.completed');
    levelCards.forEach(card => {
        card.addEventListener('click', function() {
            const levelId = this.dataset.levelId;
            if (levelId) {
                window.location.href = `/quiz/${levelId}`;
            }
        });
    });
    
    // 响应式调整
    function adjustLayout() {
        const container = document.querySelector('.container');
        if (window.innerWidth < 600) {
            container.style.padding = '10px';
        } else {
            container.style.padding = '20px';
        }
    }
    
    window.addEventListener('resize', adjustLayout);
    adjustLayout();
});