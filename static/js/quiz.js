document.addEventListener('DOMContentLoaded', function() {
    // 处理答题卡提交
    const form = document.getElementById('quiz-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // 验证所有题目是否已回答
            const unanswered = [];
            const questions = document.querySelectorAll('.question-card');
            
            questions.forEach((q, index) => {
                const inputs = q.querySelectorAll('input[type="radio"]');
                let answered = false;
                
                inputs.forEach(input => {
                    if (input.checked) answered = true;
                });
                
                if (!answered) unanswered.push(index + 1);
            });
            
            if (unanswered.length > 0) {
                e.preventDefault();
                alert(`请回答第 ${unanswered.join(', ')} 题`);
            }
        });
    }
});