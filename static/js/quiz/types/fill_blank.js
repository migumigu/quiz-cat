/**
 * 填空题特定JavaScript
 * 处理填空题特有的交互逻辑
 */

function initQuestionType() {
    // 填空题特定初始化
    const inputs = document.querySelectorAll('.fill-blank-input');
    const submitBtn = document.getElementById('submit-btn');
    
    // 添加输入事件监听
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            // 检查是否有任何输入框有内容
            let hasContent = false;
            inputs.forEach(inp => {
                if (inp.value.trim() !== '') {
                    hasContent = true;
                }
            });
            
            // 启用或禁用提交按钮
            if (submitBtn) {
                submitBtn.disabled = !hasContent;
            }
        });
    });
    
    // 扩展核心验证方法
    if (window.quizCore) {
        // 保存原始方法的引用
        const originalValidate = window.quizCore.validateAnswer;
        
        // 重写验证方法
        window.quizCore.validateAnswer = function(formData) {
            // 获取所有填空的答案
            const answers = [];
            inputs.forEach(input => {
                answers.push(input.value.trim().toLowerCase());
            });
            
            // 获取正确答案
            let correctAnswers = [];
            try {
                // 尝试从页面数据中获取正确答案
                const correctAnswersData = document.getElementById('correct-answers-data');
                if (correctAnswersData) {
                    correctAnswers = JSON.parse(correctAnswersData.textContent);
                }
            } catch (e) {
                console.error('Error parsing correct answers:', e);
                return false;
            }
            
            // 如果只有一个填空
            if (answers.length === 1 && typeof correctAnswers === 'string') {
                return this.checkAnswer(answers[0], correctAnswers);
            }
            
            // 如果有多个填空
            if (Array.isArray(correctAnswers) && answers.length === correctAnswers.length) {
                // 检查每个填空是否正确
                for (let i = 0; i < answers.length; i++) {
                    // 如果任何一个填空不正确，则整体不正确
                    if (!this.checkAnswer(answers[i], correctAnswers[i])) {
                        return false;
                    }
                }
                return true;
            }
            
            return false;
        };
        
        // 添加答案检查方法
        window.quizCore.checkAnswer = function(userAnswer, correctAnswer) {
            // 如果正确答案是数组（多个可能的正确答案）
            if (Array.isArray(correctAnswer)) {
                return correctAnswer.some(answer => 
                    this.compareAnswers(userAnswer, answer)
                );
            }
            
            // 单个正确答案
            return this.compareAnswers(userAnswer, correctAnswer);
        };
        
        // 添加答案比较方法
        window.quizCore.compareAnswers = function(userAnswer, correctAnswer) {
            // 转换为小写并去除首尾空格
            userAnswer = userAnswer.toLowerCase().trim();
            correctAnswer = String(correctAnswer).toLowerCase().trim();
            
            // 精确匹配
            if (userAnswer === correctAnswer) {
                return true;
            }
            
            // 忽略标点符号的匹配
            const userAnswerNoPunct = userAnswer.replace(/[.,，。、；：！？""''（）【】《》\s]/g, '');
            const correctAnswerNoPunct = correctAnswer.replace(/[.,，。、；：！？""''（）【】《》\s]/g, '');
            
            return userAnswerNoPunct === correctAnswerNoPunct;
        };
    }
}