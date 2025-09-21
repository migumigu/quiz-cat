/**
 * 题型核心JavaScript
 * 处理所有题型共享的功能，如提交答案、显示反馈等
 */

class QuizCore {
    constructor() {
        this.initElements();
        this.initEvents();
    }
    
    /**
     * 初始化DOM元素引用
     */
    initElements() {
        // 表单和按钮
        this.quizForm = document.getElementById('quiz-form');
        this.submitBtn = document.getElementById('submit-btn');
        
        // 反馈相关元素
        this.feedbackOverlay = document.getElementById('feedback');
        this.feedbackCard = document.getElementById('feedback-card');
        this.feedbackTitle = document.getElementById('feedback-title');
        this.feedbackMessage = document.getElementById('feedback-message');
        this.nextBtn = document.getElementById('next-btn');
        
        // 生命值和进度
        this.hearts = document.querySelectorAll('.heart');
        this.progressBar = document.querySelector('.progress');
    }
    
    /**
     * 初始化事件监听
     */
    initEvents() {
        if (this.quizForm) {
            this.quizForm.addEventListener('submit', this.handleSubmit.bind(this));
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', this.handleNext.bind(this));
        }
    }
    
    /**
     * 处理表单提交
     * @param {Event} event - 提交事件
     */
    handleSubmit(event) {
        event.preventDefault();
        
        // 获取表单数据
        const formData = new FormData(this.quizForm);
        
        // 检查答案是否正确
        const isCorrect = this.validateAnswer(formData);
        
        // 显示反馈
        this.showFeedback(isCorrect);
        
        // 更新生命值
        if (!isCorrect) {
            this.updateHearts();
        }
        
        // 发送结果到服务器
        this.sendResult(formData, isCorrect);
    }
    
    /**
     * 验证答案是否正确
     * 这是一个基础实现，具体题型会重写此方法
     * @param {FormData} formData - 表单数据
     * @returns {boolean} 是否正确
     */
    validateAnswer(formData) {
        // 基础实现：检查data-correct属性
        const selectedOption = document.querySelector('input[name="answer"]:checked');
        if (selectedOption) {
            return selectedOption.dataset.correct === '1';
        }
        return false;
    }
    
    /**
     * 显示反馈信息
     * @param {boolean} isCorrect - 是否回答正确
     */
    showFeedback(isCorrect) {
        // 设置反馈内容
        if (isCorrect) {
            this.feedbackTitle.textContent = '回答正确！';
            this.feedbackMessage.textContent = '太棒了，继续保持！';
            this.feedbackCard.className = 'feedback-card feedback-correct';
        } else {
            this.feedbackTitle.textContent = '回答错误';
            this.feedbackMessage.textContent = '再接再厉，下次一定能行！';
            this.feedbackCard.className = 'feedback-card feedback-wrong';
        }
        
        // 显示反馈
        this.feedbackOverlay.classList.add('show');
    }
    
    /**
     * 更新生命值
     */
    updateHearts() {
        // 找到第一个未失去的心
        for (let i = this.hearts.length - 1; i >= 0; i--) {
            if (!this.hearts[i].classList.contains('lost')) {
                this.hearts[i].classList.add('lost');
                
                // 发送更新生命值的请求
                fetch('/update_hearts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ hearts: i }),
                });
                
                break;
            }
        }
    }
    
    /**
     * 发送结果到服务器
     * @param {FormData} formData - 表单数据
     * @param {boolean} isCorrect - 是否回答正确
     */
    sendResult(formData, isCorrect) {
        // 添加是否正确的信息
        formData.append('is_correct', isCorrect);
        
        // 发送到服务器
        fetch(this.quizForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Result sent:', data);
            
            // 如果是最后一题或者生命值为0，则跳转到结果页面
            if (data.redirect) {
                // 设置延迟跳转
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1500); // 1.5秒后跳转
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    /**
     * 处理下一题按钮点击
     */
    handleNext() {
        this.feedbackOverlay.classList.remove('show');
        
        // 如果有下一题URL，则跳转
        const nextUrl = this.nextBtn.dataset.nextUrl;
        if (nextUrl) {
            window.location.href = nextUrl;
        }
    }
}

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 创建核心实例
    window.quizCore = new QuizCore();
    
    // 如果有题型特定的初始化函数，则调用它
    if (typeof initQuestionType === 'function') {
        initQuestionType();
    }
});