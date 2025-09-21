// 关卡结果页面专用脚本
(function() {
    'use strict';
    
    // 初始化知识点图表
    function initKnowledgeChart() {
        const chartContainer = document.getElementById('knowledge-chart');
        if (!chartContainer || !window.Chart) return;
        
        // 从data属性获取图表数据
        const chartData = JSON.parse(chartContainer.dataset.chartData || '{}');
        if (!chartData.labels || !chartData.values) return;
        
        const ctx = chartContainer.getContext('2d');
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: '知识点掌握度',
                    data: chartData.values,
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
    
    // 页面加载完成后初始化
    document.addEventListener('DOMContentLoaded', function() {
        initKnowledgeChart();
    });
})();