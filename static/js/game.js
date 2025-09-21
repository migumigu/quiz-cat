// 卡片交互效果
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.level-card:not(.locked)');
    
    cards.forEach(card => {
        card.addEventListener('click', function() {
            // 获取关卡ID
            const levelId = this.dataset.levelId;
            
            // 点击效果
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
                
                // 跳转到关卡题目列表页面
                window.location.href = `/level/${levelId}/questions`;
            }, 200);
        });
    });
    
    console.log('卡片闯关页面初始化完成');
});