/**
 * 连线题特定JavaScript
 * 处理连线题特有的交互逻辑
 */

function initQuestionType() {
    // 连线题特定初始化
    const leftItems = document.querySelectorAll('.left-item');
    const rightItems = document.querySelectorAll('.right-item');
    const linesContainer = document.getElementById('matching-lines');
    const resultInput = document.getElementById('matching-result');
    const submitBtn = document.getElementById('submit-btn');
    
    let selectedLeftItem = null;
    let matches = [];
    
    // 绘制连线
    function drawLines() {
        linesContainer.innerHTML = '';
        
        matches.forEach(match => {
            const leftItem = document.querySelector(`.left-item[data-id="${match.left}"]`);
            const rightItem = document.querySelector(`.right-item[data-id="${match.right}"]`);
            
            if (leftItem && rightItem) {
                const leftRect = leftItem.getBoundingClientRect();
                const rightRect = rightItem.getBoundingClientRect();
                const containerRect = linesContainer.getBoundingClientRect();
                
                const startX = leftRect.right - containerRect.left;
                const startY = leftRect.top + leftRect.height/2 - containerRect.top;
                const endX = rightRect.left - containerRect.left;
                const endY = rightRect.top + rightRect.height/2 - containerRect.top;
                
                const length = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2));
                const angle = Math.atan2(endY - startY, endX - startX);
                
                const line = document.createElement('div');
                line.className = 'matching-line';
                line.style.width = `${length}px`;
                line.style.left = `${startX}px`;
                line.style.top = `${startY}px`;
                line.style.transform = `rotate(${angle}rad)`;
                
                linesContainer.appendChild(line);
            }
        });
    }
    
    // 更新匹配结果
    function updateResult() {
        resultInput.value = JSON.stringify(matches);
        submitBtn.disabled = matches.length < Math.min(leftItems.length, rightItems.length);
    }
    
    // 左侧项目点击事件
    leftItems.forEach(item => {
        item.addEventListener('click', () => {
            // 如果已经匹配，取消匹配
            const matchIndex = matches.findIndex(m => m.left === parseInt(item.dataset.id));
            if (matchIndex !== -1) {
                const match = matches[matchIndex];
                matches.splice(matchIndex, 1);
                
                item.classList.remove('matched');
                document.querySelector(`.right-item[data-id="${match.right}"]`).classList.remove('matched');
                
                drawLines();
                updateResult();
                return;
            }
            
            // 选择当前项目
            if (selectedLeftItem) {
                selectedLeftItem.classList.remove('selected');
            }
            
            item.classList.add('selected');
            selectedLeftItem = item;
        });
    });
    
    // 右侧项目点击事件
    rightItems.forEach(item => {
        item.addEventListener('click', () => {
            // 如果已经匹配，取消匹配
            const matchIndex = matches.findIndex(m => m.right === parseInt(item.dataset.id));
            if (matchIndex !== -1) {
                const match = matches[matchIndex];
                matches.splice(matchIndex, 1);
                
                item.classList.remove('matched');
                document.querySelector(`.left-item[data-id="${match.left}"]`).classList.remove('matched');
                
                drawLines();
                updateResult();
                return;
            }
            
            // 如果有选中的左侧项目，创建匹配
            if (selectedLeftItem) {
                const leftId = parseInt(selectedLeftItem.dataset.id);
                const rightId = parseInt(item.dataset.id);
                
                // 移除已有的匹配
                matches = matches.filter(m => m.left !== leftId && m.right !== rightId);
                
                // 添加新匹配
                matches.push({
                    left: leftId,
                    right: rightId
                });
                
                // 更新样式
                selectedLeftItem.classList.remove('selected');
                selectedLeftItem.classList.add('matched');
                item.classList.add('matched');
                
                selectedLeftItem = null;
                
                // 更新连线和结果
                drawLines();
                updateResult();
            }
        });
    });
    
    // 窗口大小变化时重绘连线
    window.addEventListener('resize', drawLines);
    
    // 初始化
    updateResult();
    
    // 扩展核心验证方法
    if (window.quizCore) {
        // 保存原始方法的引用
        const originalValidate = window.quizCore.validateAnswer;
        
        // 重写验证方法
        window.quizCore.validateAnswer = function(formData) {
            // 获取用户的匹配结果
            let userMatches = [];
            try {
                userMatches = JSON.parse(resultInput.value);
            } catch (e) {
                console.error('Error parsing user matches:', e);
                return false;
            }
            
            // 获取正确的匹配
            let correctMatches = [];
            try {
                // 尝试从页面数据中获取正确匹配
                const correctMatchesData = document.getElementById('correct-matches-data');
                if (correctMatchesData) {
                    correctMatches = JSON.parse(correctMatchesData.textContent);
                }
            } catch (e) {
                console.error('Error parsing correct matches:', e);
                return false;
            }
            
            // 如果匹配数量不一致，则不正确
            if (userMatches.length !== correctMatches.length) {
                return false;
            }
            
            // 检查每个匹配是否正确
            for (const correctMatch of correctMatches) {
                // 查找用户匹配中是否有对应的匹配
                const found = userMatches.some(userMatch => 
                    userMatch.left === correctMatch.left && 
                    userMatch.right === correctMatch.right
                );
                
                // 如果没有找到对应的匹配，则不正确
                if (!found) {
                    return false;
                }
            }
            
            return true;
        };
    }
}