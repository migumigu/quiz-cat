// 题目页面交互逻辑

document.addEventListener('DOMContentLoaded', function() {
    // 选择题处理
    setupMultipleChoiceQuestion();
    
    // 判断题处理
    setupTrueFalseQuestion();
    
    // 提交按钮处理
    setupSubmitButton();
});

/**
 * 设置选择题交互
 */
function setupMultipleChoiceQuestion() {
    const optionItems = document.querySelectorAll('.option-item');
    if (optionItems.length === 0) return;
    
    optionItems.forEach(option => {
        option.addEventListener('click', function() {
            // 移除其他选项的选中状态
            optionItems.forEach(item => {
                item.classList.remove('selected');
            });
            
            // 添加当前选项的选中状态
            this.classList.add('selected');
            
            // 启用提交按钮
            const submitButton = document.getElementById('submit-answer');
            if (submitButton) {
                submitButton.disabled = false;
            }
            
            // 更新隐藏字段的值
            const selectedOptionInput = document.getElementById('selected-option');
            if (selectedOptionInput) {
                selectedOptionInput.value = this.dataset.option;
            }
        });
    });
}

/**
 * 设置判断题交互
 */
function setupTrueFalseQuestion() {
    const trueOption = document.querySelector('.true-option');
    const falseOption = document.querySelector('.false-option');
    
    if (!trueOption || !falseOption) return;
    
    trueOption.addEventListener('click', function() {
        trueOption.classList.add('selected');
        falseOption.classList.remove('selected');
        
        // 启用提交按钮
        const submitButton = document.getElementById('submit-answer');
        if (submitButton) {
            submitButton.disabled = false;
        }
        
        // 更新隐藏字段的值
        const selectedOptionInput = document.getElementById('selected-option');
        if (selectedOptionInput) {
            selectedOptionInput.value = 'true';
        }
    });
    
    falseOption.addEventListener('click', function() {
        falseOption.classList.add('selected');
        trueOption.classList.remove('selected');
        
        // 启用提交按钮
        const submitButton = document.getElementById('submit-answer');
        if (submitButton) {
            submitButton.disabled = false;
        }
        
        // 更新隐藏字段的值
        const selectedOptionInput = document.getElementById('selected-option');
        if (selectedOptionInput) {
            selectedOptionInput.value = 'false';
        }
    });
}

/**
 * 设置提交按钮交互
 */
function setupSubmitButton() {
    const submitButton = document.getElementById('submit-answer');
    if (!submitButton) return;
    
    // 初始状态下禁用提交按钮
    submitButton.disabled = true;
    
    // 监听表单提交
    const answerForm = document.getElementById('answer-form');
    if (answerForm) {
        answerForm.addEventListener('submit', function(event) {
            // 检查是否已选择答案
            const selectedOptionInput = document.getElementById('selected-option');
            if (!selectedOptionInput || !selectedOptionInput.value) {
                event.preventDefault();
                alert('请选择一个答案');
            }
            
            // 添加提交时间
            const timeSpentInput = document.getElementById('time-spent');
            if (timeSpentInput && window.startTime) {
                const timeSpent = Math.floor((Date.now() - window.startTime) / 1000);
                timeSpentInput.value = timeSpent;
            }
        });
    }
    
    // 记录开始答题时间
    window.startTime = Date.now();
}

/**
 * 显示答题结果
 * @param {boolean} isCorrect 是否回答正确
 * @param {string} correctAnswer 正确答案
 * @param {string} explanation 解析
 */
function showResult(isCorrect, correctAnswer, explanation) {
    const resultContainer = document.getElementById('result-container');
    if (!resultContainer) return;
    
    resultContainer.style.display = 'block';
    
    const resultIcon = document.getElementById('result-icon');
    const resultMessage = document.getElementById('result-message');
    
    if (isCorrect) {
        resultIcon.innerHTML = '✓';
        resultIcon.classList.add('correct');
        resultMessage.textContent = '回答正确！';
    } else {
        resultIcon.innerHTML = '✗';
        resultIcon.classList.add('incorrect');
        resultMessage.textContent = `回答错误！正确答案是: ${correctAnswer}`;
    }
    
    const resultExplanation = document.getElementById('result-explanation');
    if (resultExplanation && explanation) {
        resultExplanation.textContent = explanation;
    }
    
    // 滚动到结果区域
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * 初始化知识点掌握度图表
 * @param {Object} data 知识点数据
 */
function initKnowledgeChart(data) {
    const chartContainer = document.getElementById('knowledge-chart');
    if (!chartContainer || !window.Chart) return;
    
    const ctx = chartContainer.getContext('2d');
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels,
            datasets: [{
                label: '知识点掌握度',
                data: data.values,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scale: {
                ticks: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}