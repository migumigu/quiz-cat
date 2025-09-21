/**
 * 选择题特定JavaScript
 * 处理选择题特有的交互逻辑
 */

function initQuestionType() {
    // 选择题特定初始化
    const options = document.querySelectorAll('.options label');
    
    // 添加选项点击效果
    options.forEach(option => {
        option.addEventListener('click', function() {
            // 移除所有选项的选中状态
            options.forEach(opt => opt.classList.remove('selected'));
            
            // 添加当前选项的选中状态
            this.classList.add('selected');
            
            // 确保单选按钮被选中
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                
                // 启用提交按钮
                const submitBtn = document.getElementById('submit-btn');
                if (submitBtn) {
                    submitBtn.disabled = false;
                }
            }
        });
    });
    
    // 扩展核心验证方法
    if (window.quizCore) {
        // 保存原始方法的引用
        const originalValidate = window.quizCore.validateAnswer;
        
        // 重写验证方法
        window.quizCore.validateAnswer = function(formData) {
            // 使用原始方法进行基本验证
            return originalValidate.call(this, formData);
        };
    }
}